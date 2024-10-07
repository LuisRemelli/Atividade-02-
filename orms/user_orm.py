from models.user import User
from sqlalchemy.orm import Session
from utils.db_session import get_db_session

class UserORM:

    @staticmethod
    async def save(user: User):
        session: Session = get_db_session()
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    async def find_by_id(user_id: int):
        session: Session = get_db_session()
        return session.query(User).filter_by(id=user_id).first()
