from pydantic import BaseModel, EmailStr
from uuid import UUID as TypeUUID


# Schema to handle the user signup
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Schema to send the response of the registered user
class UserResponse(BaseModel):
    user_id: TypeUUID
    user_email: EmailStr
    is_admin: bool

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
