from app.models import User
from sqlalchemy.orm import Session


def get_user(db: Session, login: str) -> User | None:
    return db.query(User).filter(User.login == login).first()


def create_user(db: Session, login: str) -> User:
    user = User(login=login)
    db.add(user)
    db.flush()
    return user
