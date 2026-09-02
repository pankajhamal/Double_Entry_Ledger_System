from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, Integer, Numeric
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
        nullable=True
    )

    account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )


    debit = Column(
        Numeric(18, 2),
        default=0,
        nullable=False
    )

    credit = Column(
        Numeric(18, 2),
        default=0,
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