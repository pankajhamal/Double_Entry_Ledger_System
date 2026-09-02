from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from backend.core.database import get_db
from backend.models import User, Account, Ledger, AccountType, STATUS, Transaction
from backend.schema.user import UserSignupRequest, UserLoginRequest
from backend.auth.auth import hash_password, verify_password
from backend.core.logger import logger

router = APIRouter(
    prefix="/ledger",
    tags=["Double Entry Ledger"]
)

@router.post("/signup")
def signup(user: UserSignupRequest, db: Session = Depends(get_db)):

    #Check if user already exist
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exist"
        )
    if existing_user:
        raise HTTPException(
            status_code=401,
            detail="User already exist"
        )
    hashed = hash_password(user.password)

    new_user = User(
        name = user.full_name,
        email=user.email,
        password_hash=hashed
    )

    db.add(new_user)
    db.flush() #Get new_user.id without commiting

    #Create a new account for new user
    new_account = Account(
        user_id = new_user.id,
        currency = "NRP",
        account_type = AccountType.SAVING,
        status = STATUS.ACTIVE
    )

    db.add(new_account)
    db.flush()

    opening_transaction = Transaction(
        reference = f"OPENING-{new_account.id}",
        description = f"Initial account balance"
    )
    db.add(opening_transaction)
    db.flush()

    user_entry = Ledger(
        transaction_id = opening_transaction.id,
        account_id = new_account.id,
        debit = 10000,
        credit = 0,
    )
    system_entry = Ledger(
        transaction_id = opening_transaction.id,
        account_id = new_account.id,
        debit = 0, 
        credit = 10000
    )   

    db.add(user_entry)
    db.add(system_entry)

    db.commit()
    db.refresh(new_user)
    db.refresh(new_account)

    return {
        "message": "User created",
        "id": new_user.id,
        "account_id": new_account.id
    }

@router.post("/login")
def login(user: UserLoginRequest, db: Session = Depends(get_db)):

    result = db.execute(
        select(User).where(User.email == user.email)
    )

    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    #Verify password
    if not verify_password(user.password, existing_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    return {
        "Message": "User Login Successfull",
        "user": existing_user.name
    }
