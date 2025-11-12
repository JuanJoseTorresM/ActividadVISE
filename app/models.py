from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Client(BaseModel):
    """Modelo para representar un cliente de VISE"""
    name: str = Field(..., description="Nombre completo del cliente", example="Juan Pérez")
    country: str = Field(..., description="País de residencia del cliente", example="México")
    monthlyIncome: int = Field(..., description="Ingreso mensual en USD", example=5000, ge=0)
    viseClub: bool = Field(..., description="Indica si el cliente pertenece al VISE Club", example=True)
    cardType: str = Field(..., description="Tipo de tarjeta VISE", example="Gold", pattern="^(Classic|Gold|Platinum)$")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "country": "México",
                "monthlyIncome": 5000,
                "viseClub": True,
                "cardType": "Gold"
            }
        }

class Purchase(BaseModel):
    """Modelo para representar una compra realizada con tarjeta VISE"""
    clientId: int = Field(..., description="ID único del cliente que realiza la compra", example=1, ge=1)
    amount: float = Field(..., description="Monto de la compra", example=150.50, gt=0)
    currency: str = Field(..., description="Moneda de la transacción", example="USD", pattern="^[A-Z]{3}$")
    purchaseDate: datetime = Field(..., description="Fecha y hora de la compra")
    purchaseCountry: str = Field(..., description="País donde se realizó la compra", example="Estados Unidos")

    class Config:
        json_schema_extra = {
            "example": {
                "clientId": 1,
                "amount": 150.50,
                "currency": "USD",
                "purchaseDate": "2025-10-20T14:30:00Z",
                "purchaseCountry": "Estados Unidos"
            }
        }

class ClientResponse(BaseModel):
    """Respuesta al registrar un cliente"""
    success: bool = Field(..., description="Indica si el registro fue exitoso")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    clientId: Optional[int] = Field(None, description="ID asignado al cliente registrado")

class PurchaseResponse(BaseModel):
    """Respuesta al procesar una compra"""
    success: bool = Field(..., description="Indica si la compra fue procesada exitosamente")
    message: str = Field(..., description="Mensaje descriptivo del resultado")
    transactionId: Optional[str] = Field(None, description="ID único de la transacción")
    discountApplied: Optional[float] = Field(None, description="Descuento aplicado por ser miembro VISE Club")
