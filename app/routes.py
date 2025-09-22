from fastapi import APIRouter
from app.models import Client, Purchase
from app.services import register_client, process_purchase

router = APIRouter()

@router.post("/client")
def create_client(client: Client):
    return register_client(client)

@router.post("/purchase")
def create_purchase(purchase: Purchase):
    return process_purchase(purchase)
