from src.main.api.models.base_module import BaseModel



class User(BaseModel):
    username: str
    role: str

class LoginUserResponse(BaseModel):
    token: str
    user: User