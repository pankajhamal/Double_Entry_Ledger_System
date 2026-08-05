from sqlalchemy import Column, String, UUID, Integer
from backend.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String, nullable=False)
  email = Column(String, nullable=False)  
  password_hash = Column(String, nullable=False)

  #Relationship with accoutn
  accounts = relationship("Account", back_populates="user")