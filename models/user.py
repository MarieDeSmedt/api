

from typing import Optional
from pydantic import BaseModel


USER_SCOP= {"display": "picture" }

ADMIN_SCOP = {"database": "all", "display":"all"}

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    status: str = "user"

 

    

class UserInDB(User):
    hashed_password: str
    