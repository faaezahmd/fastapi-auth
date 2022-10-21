from sqlalchemy.orm import Session

import models, schemas
from fastapi.exceptions import HTTPException

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.email == user_id).first()

def check_username(db: Session, user_name: str):
     return db.query(models.User).filter(models.User.username == user_name).first()

def check_password(db: Session, user_password: str):
     return db.query(models.User).filter(models.User.password == user_password).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def add_token(db: Session, email: str, token: str):
    db.query(models.User).filter(models.User.email == email).update({models.User.token:token}, synchronize_session = False)
    db.commit()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password
    db_user = models.User(email=user.email,username=user.username, password=fake_hashed_password)
    data = get_user(db=db,user_id=user.email)
    if data == None:
        # Session.add(db_user)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    else:
        raise HTTPException(status_code=400, detail="email already taken")
        return 'email already taken'



def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
