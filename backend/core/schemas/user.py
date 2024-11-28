from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    password: str
    email: str

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    email: str