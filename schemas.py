from pydantic import BaseModel


# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None


# class ItemCreate(ItemBase):
#     pass


# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    # id: int

class UserCreate(UserBase):
    password: str

class TokenData(BaseModel):
    id : str

class PasswordReset(BaseModel):
    email : str
# class User(UserBase):
    # id: int
    # is_active: bool
    # items: list[Item] = []

    # class Config:
    #     orm_mode = True
