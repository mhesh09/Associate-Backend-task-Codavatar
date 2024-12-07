from sql_app.database import Base
from sqlalchemy import Column, Integer, String,DATETIME,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True,index=True)
    first_name = Column(String(100),nullable=False)
    last_name = Column(String(100),nullable=False)
    email = Column(String(100),unique=True,nullable=False)
    password = Column(String(255),nullable=False)
    is_superuser = Column(Boolean,default=False)
    is_staff = Column(Boolean,default=False)
    is_active = Column(Boolean,default=True)
    created_at = Column(DATETIME,default=datetime.now(),nullable=False)
    updated_at = Column(DATETIME,default=datetime.now(),nullable=False)

    virtualphonenumber = relationship("telephone.models.VirtualPhoneNumber",back_populates="user")