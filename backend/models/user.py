from sqlalchemy import Column, String, UUID
from core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"

  id = Column(UUID(as_uuid=True), primary_key=True, nullable=False)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False)  
  password_hash = Column(String, nullable=False)

  #Relationship with accoutn
  account = relationship("Account", back_populates="users")