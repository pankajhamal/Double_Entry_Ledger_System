from sqlalchemy import Column, String, UUID, DateTime
from core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Transaction(Base):
  __tablename__ = "transactions"

  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
  idempotency_key = Column(String, unique=True, index=True)
  description = Column(String)
  created_at = Column(DateTime, default=datetime)