from sqlalchemy.orm import Session
from .schemas import UserRegistration
from .models import User
from .utils import get_password_hash



async def create_user(db:Session,user:UserRegistration):
    db_user = User(
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        password = get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    return db_user