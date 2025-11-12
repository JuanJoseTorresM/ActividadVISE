from app.models import Client, Purchase, ClientResponse, PurchaseResponse
from datetime import datetime
import uuid

# "Base de datos" simulada en memoria
clients_db = {}
client_id_counter = 1

def register_client(client: Client) -> ClientResponse:
    """Registra un nuevo cliente en el sistema con validaciones de tipo de tarjeta"""
    global client_id_counter

    # Validar restricciones según tipo de tarjeta
    if client.cardType == "Gold" and client.monthlyIncome < 500:
        return ClientResponse(
            success=False,
            message="Ingreso insuficiente para tarjeta Gold (mínimo $500 USD)",
            clientId=None
        )

    if client.cardType == "Platinum":
        if client.monthlyIncome < 1000:
            return ClientResponse(
                success=False,
                message="Ingreso insuficiente para tarjeta Platinum (mínimo $1000 USD)",
                clientId=None
            )
        if not client.viseClub:
            return ClientResponse(
                success=False,
                message="Debe ser miembro del VISE Club para tarjeta Platinum",
                clientId=None
            )

    if client.cardType == "Black":
        if client.monthlyIncome < 2000:
            return ClientResponse(
                success=False,
                message="Ingreso insuficiente para tarjeta Black (mínimo $2000 USD)",
                clientId=None
            )
        if not client.viseClub:
            return ClientResponse(
                success=False,
                message="Debe ser miembro del VISE Club para tarjeta Black",
                clientId=None
            )
        if client.country in ["China", "Vietnam", "India", "Irán"]:
            return ClientResponse(
                success=False,
                message=f"Clientes en {client.country} no pueden obtener tarjeta Black",
                clientId=None
            )

    if client.cardType == "White":
        if client.monthlyIncome < 2000 or not client.viseClub:
            return ClientResponse(
                success=False,
                message="No cumple requisitos para tarjeta White (mínimo $2000 USD y membresía VISE Club)",
                clientId=None
            )

    # Registrar cliente exitosamente
    client_id = client_id_counter
    clients_db[client_id] = client.dict()
    client_id_counter += 1

    return ClientResponse(
        success=True,
        message=f"Cliente registrado exitosamente. Apto para tarjeta {client.cardType}",
        clientId=client_id
    )

def process_purchase(purchase: Purchase) -> PurchaseResponse:
    """Procesa una compra con tarjeta VISE aplicando descuentos según membresía y tipo de tarjeta"""
    client = clients_db.get(purchase.clientId)
    if not client:
        return PurchaseResponse(
            success=False,
            message="Cliente no encontrado. Verifique el ID del cliente",
            transactionId=None,
            discountApplied=None
        )

    # Calcular descuentos y beneficios
    discount_amount = 0
    benefit_description = None
    
    # Descuento por ser miembro VISE Club
    if client["viseClub"]:
        discount_amount += purchase.amount * 0.05  # 5% descuento base
        benefit_description = "Descuento VISE Club: 5%"
    
    # Beneficios adicionales por tipo de tarjeta
    if client["cardType"] == "Gold" and purchase.amount > 100 and purchase.purchaseDate.weekday() in [0, 1, 2]:
        additional_discount = purchase.amount * 0.10  # 10% adicional lunes-miércoles
        discount_amount += additional_discount
        benefit_description = f"{benefit_description}, Gold Lunes-Miércoles: +10%" if benefit_description else "Gold Lunes-Miércoles: 10%"
    
    elif client["cardType"] == "Platinum":
        additional_discount = purchase.amount * 0.08  # 8% adicional siempre
        discount_amount += additional_discount
        benefit_description = f"{benefit_description}, Platinum: +8%" if benefit_description else "Platinum: 8%"
    
    elif client["cardType"] == "Black":
        additional_discount = purchase.amount * 0.12  # 12% adicional siempre
        discount_amount += additional_discount
        benefit_description = f"{benefit_description}, Black: +12%" if benefit_description else "Black: 12%"
    
    # Generar ID único de transacción
    transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d%H%M')}{str(uuid.uuid4())[:8].upper()}"
    
    return PurchaseResponse(
        success=True,
        message=f"Compra procesada exitosamente. {benefit_description if benefit_description else 'Sin descuentos aplicados'}",
        transactionId=transaction_id,
        discountApplied=round(discount_amount, 2) if discount_amount > 0 else None
    )
