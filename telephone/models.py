from datetime import datetime
from sql_app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column,Integer,ForeignKey,String,DateTime

class VirtualPhoneNumber(Base):
    __tablename__ = "virtual_phone_numbers"

    id = Column(Integer,primary_key=True,unique=True,nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"))
    phone_number = Column(String(20),unique=True,nullable=False)
    is_active = Column(Integer,default=1)

    user = relationship("user.models.User",back_populates="virtualphonenumber")
    call_log = relationship("CallLog",back_populates="virtual_phone_number")


class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer,primary_key=True,index=True)
    virtual_phone_number_id = Column(Integer,ForeignKey("virtual_phone_numbers.id"))
    caller = Column(String(20),nullable=False)
    recipient = Column(String(20),nullable=False)
    call_type = Column(String(20),nullable=False)
    duration = Column(Integer,nullable=True)
    timestamp = Column(DateTime,default=datetime.now(),nullable=False)

    virtual_phone_number = relationship("VirtualPhoneNumber",back_populates="call_log")



