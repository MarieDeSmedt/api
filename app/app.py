from datetime import datetime, timedelta
import pickle

import sys
sys.path.insert(0,"./utils/")

from fastapi import Depends, FastAPI, HTTPException, status
from models.token import Token, TokenData
from models.user import User
from utils.auth_utils import oauth2_scheme, OAuth2PasswordRequestForm,create_access_token
from utils.user_utils import get_current_active_user, authenticate_user
from database.fake_users_db import fake_users_db
from conf.conf import ACCESS_TOKEN_EXPIRE_MINUTES





app = FastAPI()



@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]



@app.get("/{input}")
def predict(input: str, current_user: User = Depends(get_current_active_user)):
    if current_user:
        tfidf, model = pickle.load(open('model.bin', 'rb'))
        predictions = model.predict(tfidf.transform([input]))
        label = predictions[0]
        return {'text': input, 'label': label}
    else:
        return {'text': "user non active by m", 'label': 'no'}
