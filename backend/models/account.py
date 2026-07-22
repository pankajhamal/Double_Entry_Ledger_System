from sqlalchemy import Column, String, UUID, Integer, ForeignKey, Enum
from core.database import Base
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

  id = Column(UUID(as_uuid=True), primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
  currency = Column(String, nullable=False)
  account_type = Column(Enum(AccountType), default=AccountType.SAVING, nullable=False)
  status = Column(Enum(STATUS), default=STATUS.CLOSED, nullable=False)

  #Relationship with user
  user = relationship("User", back_populates="accounts")