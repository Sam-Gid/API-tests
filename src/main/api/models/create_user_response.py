from src.main.api.models.base_module import BaseModel



class CreateUserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: str