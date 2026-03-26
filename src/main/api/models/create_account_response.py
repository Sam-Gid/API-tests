from src.main.api.models.base_module import BaseModel



class CreateAccountResponse(BaseModel):
    id: int
    number: str
    balance: float