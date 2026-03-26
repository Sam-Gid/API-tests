from src.main.api.models.base_module import BaseModel



class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str