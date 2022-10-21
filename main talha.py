# from typing import Union

# from fastapi import FastAPI
# import uvicorn

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

# if __name__ == '__main__':
#     uvicorn.run("main:app", host="127.0.0.1", port=5000,
#                 reload=True, log_level="info")
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.responses import JSONResponse
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
import uvicorn
# from fastapi import Request
# from sqlalchemy.orm import Session
# # import models
# from database import SessionLocal, engine

# # models.Base.metadata.create_all(bind=engine)

# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=['*'],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# @app.get('/test/{{user_id}}')

# # def get_user(db: Session, user_id: int):
# #     return db.query(models.User).filter(models.User.id == user_id).first()
# class User(BaseModel):
#     username: str
#     password: str

# class UserRegister(BaseModel):
#     username: str
#     password: str
#     email: str
# # in production you can use Settings management
# # from pydantic to get secret key from .env
# class Settings(BaseModel):
#     authjwt_secret_key: str = "secret"

# # callback to get your configuration
# @AuthJWT.load_config
# def get_config():
#     return Settings()

# # exception handler for authjwt
# # in production, you can tweak performance using orjson response
# @app.exception_handler(AuthJWTException)
# def authjwt_exception_handler(request: Request, exc: AuthJWTException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={"detail": exc.message}
#     )

# # provide a method to create access tokens. The create_access_token()
# # function is used to actually generate the token to use authorization
# # later in endpoint protected
# @app.post('/login')

# def login(user: User, Authorize: AuthJWT = Depends()):
#     if user.username != "test" or user.password != "test":
#         raise HTTPException(status_code=401,detail="Bad username or password")

#     # subject identifier for who this token is for example id or username from database
#     access_token = Authorize.create_access_token(subject=user.username)
#     return {"accessToken": access_token , "username": user.username  }

# @app.post("/signup")

# def signup(user: UserRegister):
#     return user

# # protect endpoint with function jwt_required(), which requires
# # a valid access token in the request headers to access.
# @app.get('/profile')
# def user(Authorize: AuthJWT = Depends()):
#     Authorize.jwt_required()

#     current_user = Authorize.get_jwt_subject()
#     return {"user": current_user}

# if __name__ == '__main__':
#     uvicorn.run("main:app", host="localhost", port=5000,
#                 reload=True, log_level="info")

# from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session

# from . import crud, models, schemas
# from .database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

# app = FastAPI()


# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items

