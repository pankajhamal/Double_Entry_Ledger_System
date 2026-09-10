from backend.models.ledger import Ledger
from sqlalchemy import func, select
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

def get_user_balance(account_id, db: Session):

    result = db.execute(
        select(
            func.coalesce(func.sum(Ledger.debit), 0),
            func.coalesce(func.sum(Ledger.credit), 0)
        ).where(
            Ledger.account_id == account_id
        )
    ).one()

    total_debit, total_credit = result

    balance = total_debit - total_credit

    logger.info(
        "Account %s | Debit: %s | Credit: %s | Balance: %s",
        account_id,
        total_debit,
        total_credit,
        balance
    )

    return balance

def get_user_history(account_id, db: Session):

    history = db.query(Ledger).filter(Ledger.account_id == account_id).order_by(Ledger.id.desc()).all()

    return history

