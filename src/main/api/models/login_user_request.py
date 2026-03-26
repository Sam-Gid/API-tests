from src.main.api.models.base_module import BaseModel



class LoginUserRequest(BaseModel):
    username: str
    password: str