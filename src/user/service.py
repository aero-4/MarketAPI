import random
from datetime import timedelta

from fastapi import HTTPException
from starlette import status

from src.config import settings
from src.exceptions import NotFound, AlreadyExist
from src.models import User
from src.services.codes.email import Email
from src.services.codes.phone import Phone
from src.user.constants import ALLOWED_TYPES_PROFILE_PHOTO
from src.utils import save_media, random_string


async def edit_photo(photo, user):
    file_path = await save_media(photo, ALLOWED_TYPES_PROFILE_PHOTO)
    user.photo = file_path
    await user.save()


async def edit_phone(schema, user, background_tasks, redis):
    if user.phone == schema.phone:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This number is in use")

    random_num = random.randint(100000, 999999)

    minutes = 1
    if await redis.get(schema.phone):
        minutes *= 2

    to = schema.phone
    phone = Phone()
    background_tasks.add_task(phone.sent_code, schema.phone, random_num)
    await redis.set(to, random_num, ex=timedelta(minutes=minutes))


async def verify_code_phone(schema, user, redis) -> User:
    if await redis.get(str(schema.phone)) != str(schema.code):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not valid code or expired")

    user.phone = schema.phone
    await user.save()
    return user


async def edit_email(schema, user, background_tasks, redis):
    if schema.email == user.email:
        raise AlreadyExist(message="You must have new email address")

    check_email_in_db = await User.get_or_none(email=schema.email)
    if check_email_in_db:
        raise AlreadyExist(message="This email is in use")

    token = random_string()
    callback_url = f"{settings.DOMAIN_API}/{settings.API_V1_STR}/user/email/verify/{token}"
    to = user.email or schema.email
    email = Email()

    minutes = 1
    if await redis.get(schema.email):
        minutes *= 2

    background_tasks.add_task(email.send_mail, to=to, subject=f"{settings.TITLE} - Confirm your email", url=callback_url)
    await redis.set(token, to, ex=timedelta(minutes=minutes))


async def verify_code_email(token, user, redis) -> User:
    current_email = await redis.get(token)
    if not current_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not valid token")

    user.email = current_email
    await user.save()
    return user
