from fastapi import APIRouter, HTTPException, Body
from app.models import Client, Purchase, ClientResponse, PurchaseResponse
from app.services import register_client, process_purchase
from datetime import datetime

router = APIRouter()

@router.post(
    "/client",
    response_model=ClientResponse,
    tags=["Clientes"],
    summary="Registrar nuevo cliente",
    description="Registra un nuevo cliente en el sistema VISE con validación de datos y asignación automática de ID",
    responses={
        200: {
            "description": "Cliente registrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Cliente registrado exitosamente",
                        "clientId": 1
                    }
                }
            }
        },
        400: {
            "description": "Datos de cliente inválidos",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Datos de cliente inválidos"
                    }
                }
            }
        }
    }
)
def create_client(client: Client):
    """Registra un nuevo cliente en el sistema VISE"""
    try:
        return register_client(client)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint alias en español: acepta payloads con keys en español y los mapea al modelo Client
@router.post(
    "/clientes",
    response_model=ClientResponse,
    tags=["Clientes"],
    summary="Registrar nuevo cliente (ES)",
    description="Alias en español que acepta campos como `nombre`, `tipo_tarjeta`, `miembro_club`",
)
def create_client_es(payload: dict = Body(...)):
    try:
        client = Client(
            name=payload.get("nombre") or payload.get("name"),
            country=payload.get("pais") or payload.get("country") or "",
            monthlyIncome=payload.get("monthlyIncome") or payload.get("ingreso_mensual") or 0,
            viseClub=payload.get("miembro_club") if "miembro_club" in payload else payload.get("viseClub", False),
            cardType=payload.get("tipo_tarjeta") or payload.get("cardType") or "Classic",
        )
        return register_client(client)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/purchase",
    response_model=PurchaseResponse,
    tags=["Compras"],
    summary="Procesar compra",
    description="Procesa una nueva compra con tarjeta VISE, aplicando descuentos automáticos para miembros del VISE Club",
    responses={
        200: {
            "description": "Compra procesada exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Compra procesada exitosamente",
                        "transactionId": "TXN-2025102014301234",
                        "discountApplied": 7.5
                    }
                }
            }
        },
        400: {
            "description": "Error al procesar la compra",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Cliente no encontrado"
                    }
                }
            }
        }
    }
)
def create_purchase(purchase: Purchase):
    """Procesa una nueva compra con tarjeta VISE"""
    try:
        return process_purchase(purchase)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Endpoint alias en español: acepta payloads con keys en español y los mapea al modelo Purchase
@router.post(
    "/compras",
    response_model=PurchaseResponse,
    tags=["Compras"],
    summary="Procesar compra (ES)",
    description="Alias en español que acepta campos como `cliente_id`, `monto`, `tarjeta`",
)
def create_purchase_es(payload: dict = Body(...)):
    try:
        purchase = Purchase(
            clientId=payload.get("cliente_id") or payload.get("clientId") or 0,
            amount=payload.get("monto") or payload.get("amount") or 0.0,
            currency=payload.get("moneda") or payload.get("currency") or "USD",
            purchaseDate=payload.get("purchaseDate") or payload.get("fecha") or datetime.utcnow(),
            purchaseCountry=payload.get("pais") or payload.get("purchaseCountry") or "",
        )
        return process_purchase(purchase)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
