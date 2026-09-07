from sqlalchemy import Column, String, UUID, DateTime, Integer
from backend.core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Transaction(Base):
  __tablename__ = "transactions"

  id = Column(Integer, primary_key=True, autoincrement=True)
  idempotency_key = Column(String, unique=True, nullable=False, index=True)

  reference = Column(String, unique=True, nullable=False)
  description = Column(String, nullable=True)
  created_at = Column(DateTime, default=datetime.utcnow)

  ledgers = relationship("Ledger", back_populates="transaction")