from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models import User
from backend.schema.user import UserSignupRequest
from backend.auth.auth import hash_password
from backend.core.logger import logger

router = APIRouter(
    prefix="/ledger",
    tags=["Double Entry Ledger"]
)

@router.post("/signup")
def signup(user: UserSignupRequest, db: Session = Depends(get_db)):
    logger.info(f"Password: {user.password}")
    hashed = hash_password(user.password)

    new_user = User(
        name = user.full_name,
        email=user.email,
        password_hash=hashed
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "id": new_user.id
    }