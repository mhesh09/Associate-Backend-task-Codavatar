from sqlalchemy.orm import Session
from .schemas import VirtualPhoneNumberDetail
from .models import VirtualPhoneNumber

async def create_virtual_phone(db:Session,virtual_phone_number:VirtualPhoneNumberDetail,user_id:str):
    db_telephone = VirtualPhoneNumber(
        phone_number = virtual_phone_number.phone_number,
        user_id = user_id
    )
    db.add(db_telephone)
    db.commit()
    return db_telephone