from sqlalchemy import Column, String, UUID, Integer, ForeignKey, Enum
from backend.core.database import Base
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

class AccountType(PyEnum):
  SAVING = "savings"
  CURRENT = "current"

class STATUS(PyEnum):
  ACTIVE =  "active"
  FROZEN = "frozen"
  CLOSED =  "closed"


class Account(Base):
  __tablename__ = "accounts"

  id = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
  currency = Column(String, nullable=False)
  account_type = Column(Enum(AccountType), default=AccountType.SAVING, nullable=False)
  status = Column(Enum(STATUS), default=STATUS.CLOSED, nullable=False)

  #Relationship with user
  user = relationship("User", back_populates="accounts")

  ledgers = relationship("Ledger", back_populates="account")