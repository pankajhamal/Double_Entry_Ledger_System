from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.schema.transaction import UserTransactionRequest
from backend.service.transaction_service import TransactionService

transaction_service = TransactionService()

router = APIRouter(
    prefix="",
    tags=["User Transaction"]
)

@router.post("transaction")
async def user_transaction(payload: UserTransactionRequest, current_user: User = Depends(get_current_user)):

    return await transaction_service.payment_service(
        payload, 
        current_user
    )
