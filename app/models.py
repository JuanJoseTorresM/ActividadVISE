from pydantic import BaseModel
from datetime import datetime

class Client(BaseModel):
    name: str
    country: str
    monthlyIncome: int
    viseClub: bool
    cardType: str

class Purchase(BaseModel):
    clientId: int
    amount: float
    currency: str
    purchaseDate: datetime
    purchaseCountry: str
