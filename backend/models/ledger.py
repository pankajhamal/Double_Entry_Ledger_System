from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from backend.core.database import Base
from datetime import datetime


class Ledger(Base):
    __tablename__ = "ledger"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id"),
        nullable=False
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    amount = Column(
        BigInteger,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    transaction = relationship(
        "Transaction",
        back_populates="ledgers"
    )

    account = relationship(
        "Account",
        back_populates="ledgers"
    )