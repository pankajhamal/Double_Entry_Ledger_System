from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.schema.transaction import UserTransactionRequest
from backend.models.user import User
from backend.service.transaction_service import TransactionService
from backend.auth.security import get_current_user
from backend.core.database import get_db

transaction_service = TransactionService()

router = APIRouter(
    prefix="/user",
    tags=["User Transaction"]
)

@router.post("/payment")
async def user_transaction(payload: UserTransactionRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    return await transaction_service.payment_service(
        payload, 
        current_user,
        db
    )

