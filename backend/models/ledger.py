from sqlalchemy import Column, UUID, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class Ledger(Base):
  __tablename__ = "ledger"

  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
  transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"), nullable=False) 
  account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)

  amount = Column(BigInteger)
  created_at = Column(DateTime, default=datetime)

  transaction = relationship("Transaction", back_populates="ledger")

  account = relationship("Account", back_populates = "ledger")