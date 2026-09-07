from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from sqlalchemy import select
from backend.schema.transaction import UserTransactionRequest
from backend.models.user import User
from backend.models.account import Account
from backend.service.transaction_service import TransactionService
from backend.auth.security import get_current_user
from backend.core.database import get_db
from backend.core.db_adapter import get_user_balance

transaction_service = TransactionService()

router = APIRouter(
    prefix="/user",
    tags=["User Transaction"]
)

@router.post("/payment")
async def user_transaction(payload: UserTransactionRequest, current_user: User = Depends(get_current_user), idempotency_key:str = Header(...,alias="Idempotency-Key"), db: Session = Depends(get_db)):

    return await transaction_service.payment_service(
        payload, 
        current_user,
        idempotency_key,
        db
    )


#Get user balance
@router.get("/balance")
def check_user_balance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    account = db.query(Account).filter(Account.user_id == current_user.id).first()

    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    user_balance = get_user_balance(account.id, db)

    return{
        user_balance
    }