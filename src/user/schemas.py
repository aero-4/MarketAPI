from pydantic import BaseModel, Field, EmailStr


class EditPhoneSchema(BaseModel):
    phone: int = Field(..., )


class AddressSchema(BaseModel):
    address: str = Field(..., max_length=256)


class ConfirmEmail(BaseModel):
    email: EmailStr
    token: str