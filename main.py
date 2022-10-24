from fastapi import Depends, FastAPI, HTTPException, Request, APIRouter
from sqlalchemy.orm import Session
import uuid
import crud, models, schemas
from database import SessionLocal, engine
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = [
    "http://localhost:8080",
    "https://analytics-api.traderverse.io"
    "https://analytics-dev.traderverse.io/"
    "http://localhost",
    "http://localhost:8081",
    "https://vue-auth-front-end.herokuapp.com/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows all origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(BaseModel):
    username: str
    password: str

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Disable CSRF Protection for this example. default is True
    authjwt_cookie_csrf_protect: bool = False
    # authjwt_cookie_samesite: str = "none"
    # authjwt_cookie_secure: bool = True

@AuthJWT.load_config
def get_config():
    return Settings()

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
class UserInDB(User):
    password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


@app.post('/login')
async def login(user: User, Authorize: AuthJWT = Depends(),db: Session = Depends(get_db) ):
    user_dict = crud.check_username(db=db, user_name=user.username)
    if user_dict is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    password = crud.check_password(db=db, user_password=user.password)
    if password is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = Authorize.create_access_token(subject=user.username)
    # refresh_token = Authorize.create_refresh_token(subject=user.username)

     # Set the JWT cookies in the response
    # Authorize.set_access_cookies(access_token)
    # Authorize.set_refresh_cookies(refresh_token)

    token = jsonable_encoder(access_token)
    content = {"message": "You've sucessfully logged in"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="None",
        secure=True,
    )

    return response

@app.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    # Set the JWT cookies in the response
    Authorize.set_access_cookies(new_access_token)
    return {"msg":"The token has been refresh"}

@app.post("/signup")
def create_item_for_user(
     item: schemas.UserCreate, db: Session = Depends(get_db)
):
    return crud.create_user(db=db, user=item)

@app.post('/logout')
def logout(Authorize: AuthJWT = Depends()):
    """
    Because the JWT are stored in an httponly cookie now, we cannot
    log the user out by simply deleting the cookies in the frontend.
    We need the backend to send us a response to delete the cookies.
    """
    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}
# @app.get("/items/", response_model=list[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
@app.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    """
    We do not need to make any changes to our protected endpoints. They
    will all still function the exact same as they do when sending the
    JWT in via a headers instead of a cookies
    """
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}
# router = APIRouter(
#     prefix = "/password",
#     tags = ["password reset"]
# )

@app.post("/forgotPassword")
async def reset_request(user_email: schemas.PasswordReset , db: Session = Depends(get_db)):
    user =   crud.get_user_by_email(db= db, email= user_email.email)

    if user is not None:
        token = str(uuid.uuid4())
        # print(" TYPE ",type(token))
        reset_link = f"http://localhost:5000/token?{token}"
        crud.add_token(db=db, email=user_email.email,token=token)
        return reset_link
    else:
         raise HTTPException(status_code=400, detail="This email not found")

# import uvicorn

# if __name__ == '__main__':
#     uvicorn.run("main:app", host="localhost", port=8008,
#                 reload=True, log_level="info")
