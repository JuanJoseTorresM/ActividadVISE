from app.models import Client, Purchase

# "Base de datos" simulada en memoria
clients_db = {}
client_id_counter = 1

def register_client(client: Client):
    global client_id_counter

    # Validar restricciones según tipo de tarjeta
    if client.cardType == "Gold" and client.monthlyIncome < 500:
        return {"status": "Rejected", "error": "Ingreso insuficiente para Gold"}

    if client.cardType == "Platinum":
        if client.monthlyIncome < 1000:
            return {"status": "Rejected", "error": "Ingreso insuficiente para Platinum"}
        if not client.viseClub:
            return {"status": "Rejected", "error": "Debe tener VISE CLUB para Platinum"}

    if client.cardType == "Black":
        if client.monthlyIncome < 2000:
            return {"status": "Rejected", "error": "Ingreso insuficiente para Black"}
        if not client.viseClub:
            return {"status": "Rejected", "error": "Debe tener VISE CLUB para Black"}
        if client.country in ["China", "Vietnam", "India", "Irán"]:
            return {"status": "Rejected", "error": f"Clientes en {client.country} no pueden tener Black"}

    if client.cardType == "White":
        if client.monthlyIncome < 2000 or not client.viseClub:
            return {"status": "Rejected", "error": "No cumple requisitos para White"}

    # Registrar cliente
    client_id = client_id_counter
    clients_db[client_id] = client.dict()
    client_id_counter += 1

    return {
        "clientId": client_id,
        "name": client.name,
        "cardType": client.cardType,
        "status": "Registered",
        "message": f"Cliente apto para tarjeta {client.cardType}"
    }

def process_purchase(purchase: Purchase):
    client = clients_db.get(purchase.clientId)
    if not client:
        return {"status": "Rejected", "error": "Cliente no registrado"}

    # Aquí puedes implementar los beneficios según tarjeta
    final_amount = purchase.amount
    discount = 0
    benefit = None

    if client["cardType"] == "Gold" and purchase.amount > 100 and purchase.purchaseDate.weekday() in [0, 1, 2]:
        discount = purchase.amount * 0.15
        final_amount -= discount
        benefit = "Lunes-Miércoles: 15% descuento"

    return {
        "status": "Approved",
        "purchase": {
            "clientId": purchase.clientId,
            "originalAmount": purchase.amount,
            "discountApplied": discount,
            "finalAmount": final_amount,
            "benefit": benefit
        }
    }
