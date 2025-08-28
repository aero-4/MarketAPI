from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException, BackgroundTasks
from src.auth.schemas import UserSchema, SentCodeSchema, LoginSchema, SentEmailSchema
from src.config import get_settings
from src.middlewares.ratelimit import rate_limit, get_redis
from src.session.depends import validate_access_token
from src.models import User
from src.user.schemas import AddressSchema
from src.user.service import edit_photo, edit_phone, verify_code_phone, edit_email, verify_code_email
from src.utils import response

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/info")
async def user_info_handler(user: User = Depends(validate_access_token)):
    return UserSchema(
        id=user.id,
        role=user.role,
        first_name=user.first_name,
        full_name=user.full_name,
        photo=user.photo,
        email=user.email,
        date_at=user.date_at,
        phone=user.phone,
        balance=user.balance
    ).model_dump()


@user_router.patch("/photo/edit")
async def edit_photo_handler(
        photo: UploadFile = File(...),
        user: User = Depends(validate_access_token)
):
    user_changed = await edit_photo(photo, user)
    return response(status.HTTP_200_OK,
                    data={"photo": user_changed.photo})


@user_router.post("/phone/edit")
@rate_limit(limit=3, window=6, prefix="ph", key_func=lambda request, *a, **kw: kw["user"].id, error_msg="Try again later to edit phone")
async def edit_phone_handler(schema: SentCodeSchema, background_tasks: BackgroundTasks, user: User = Depends(validate_access_token), redis=Depends(get_redis), settings=Depends(get_settings), ):
    await edit_phone(schema, user, background_tasks, redis)
    return response(status.HTTP_200_OK,
                    message=f"Sent code to {schema.phone}")


@user_router.post("/phone/verify")
async def verify_phone_code_handler(schema: LoginSchema, user: User = Depends(validate_access_token), redis=Depends(get_redis)):
    changed_user = await verify_code_phone(schema, user, redis)
    return response(status.HTTP_200_OK,
                    data={"phone": changed_user.phone})


@user_router.post("/email/sent-code")
@rate_limit(limit=3, window=6, prefix="em", key_func=lambda request, *a, **kw: kw["user"].id, error_msg="Try again later to edit email")
async def send_code_email_handler(schema: SentEmailSchema, background_tasks: BackgroundTasks, user: User = Depends(validate_access_token), settings=Depends(get_settings), redis=Depends(get_redis)):
    await edit_email(schema, user, background_tasks, redis)
    return response(status.HTTP_200_OK,
                    message=f"Sent code to {schema.email}")


@rate_limit(limit=3, window=6, prefix="em", key_func=lambda request, *a, **kw: kw["user"].id, error_msg="Try again later")
@user_router.get("/email/verify/{token}")
async def verify_code_email_handler(token: str, user: User = Depends(validate_access_token), redis=Depends(get_redis)):
    user_changed = await verify_code_email(token, user, redis)
    return response(status.HTTP_200_OK,
                    data={"email": user_changed.email})
