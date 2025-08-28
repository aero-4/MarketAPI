import datetime
import logging
import mimetypes
import random
import re
import string
import uuid
from typing import Any, Dict

import aiofiles
import hashlib
import jwt

from fastapi import UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from jwt import ExpiredSignatureError, PyJWTError
from starlette import status
from pathlib import Path

from starlette.responses import JSONResponse
from src.auth.config import auth_settings
from src.config import DEFAULT_MEDIA_ALLOWED_MIMES, DEFAULT_MEDIA_MAX_FILE_SIZE
from src.models import Attachment


def encode_jwt(payload: dict, private_key: str = auth_settings.JWT_PRIVATE_KEY, algorithm: str = auth_settings.JWT_ALG, expire_minutes: int = auth_settings.ACCESS_TOKEN_EXP,
               expire_timedelta: datetime.timedelta | None = None) -> str:
    now = datetime.datetime.now(datetime.UTC)
    expire = now + expire_timedelta if expire_timedelta else now + datetime.timedelta(minutes=expire_minutes)
    payload.update(
        exp=expire,
        iat=now
    )
    encoded = jwt.encode(
        payload, private_key, algorithm,
    )
    return encoded


def decode_jwt(token: str, public_key: str = auth_settings.JWT_PUBLIC_KEY, algorithm: str = auth_settings.JWT_ALG) -> dict:
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired",
        )
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate token",
        )


def get_hash_string(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def random_string(length: int = 32) -> str:
    return "".join(random.sample(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=length))


def create_slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'[^\w\-]', '', text)
    text = re.sub(r'--+', '-', text)
    text = text.strip('-')
    return text


async def save_media(
        file: UploadFile,
        dest_dir: str = "files",
        max_size: int = DEFAULT_MEDIA_MAX_FILE_SIZE,
        allowed_types: list[str] = DEFAULT_MEDIA_ALLOWED_MIMES
) -> str:
    if not file.content_type or file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File must have type: {', '.join(allowed_types)}"
        )

    Path(dest_dir).mkdir(parents=True, exist_ok=True)

    ext = mimetypes.guess_extension(file.content_type) or f".{file.content_type.split('/')[-1]}"
    ext = ext.lstrip(".")
    file_name = f"{uuid.uuid4()}.{ext}"
    file_path = Path(dest_dir) / file_name

    chunk_size = 1024 * 1024
    total = 0
    try:
        async with aiofiles.open(file_path, "wb") as out:
            while True:
                chunk = await file.read(chunk_size)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_size:
                    raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                        detail=f"File too large (limit {max_size} bytes)")
                await out.write(chunk)
    except HTTPException:
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass
        raise
    finally:
        try:
            await file.close()
        except Exception:
            pass
    return str(file_path)


def response(status: int = 200, **kwargs) -> JSONResponse:
    result: Dict[str, Any] = {}
    success = 200 <= (status or 0) < 400

    if status:
        result.update(success=bool(status))

    if kwargs:
        result.update(jsonable_encoder(kwargs))

    result['success'] = success
    logging.debug(f"Response - %s", result)

    return JSONResponse(status_code=status, content=result)


async def update_object_media(objects: list, key: str = "id") -> list:
    for object in objects:
        object = object.__dict__
        medias = []
        attach = await Attachment.filter(object_id_int=object[key])

        for at in attach:
            if at.media:
                media = await at.media
                medias.append(media.url)

        object["media"] = medias
    return objects
