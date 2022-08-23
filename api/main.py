from fastapi import *
from fastapi.security import *
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel
import pyrebase

class clientesSignup(BaseModel):
    email: str
    password: str

app = FastAPI()

security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firebaseConfig = {
  "apiKey": "AIzaSyB-v5wz6EWb_ejyMaC5Bg91lb7E_pJs9Fc",
  "authDomain": "fir-auth-31388.firebaseapp.com",
  "databaseURL": "https://fir-auth-31388-default-rtdb.firebaseio.com",
  "projectId": "fir-auth-31388",
  "storageBucket": "fir-auth-31388.appspot.com",
  "messagingSenderId": "69866908125",
  "appId": "1:69866908125:web:18679f92e0592b1eb5ae34"
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()
db = firebase.database()

securityBasic = HTTPBasic()
securityBearer = HTTPBearer()

@app.get(
    "/user/validate/",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Get token for a user",
    description="Get token for a user",
    tags=["Auth"],
  )
async def get_token(credentials: HTTPBasicCredentials = Depends(securityBasic)):
    try:
      user = credentials.username
      password = credentials.password
      user = auth.sign_in_with_email_and_password(user, password)
      response = {
        "token": user['idToken'],
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@app.get(
  "/user/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Login user and get user level",
  description="Login user and get user level",
  tags=["Auth"],
)
async def login_final(credentials: HTTPAuthorizationCredentials =  Depends(securityBearer)):
    try:
      user = auth.get_account_info(credentials.credentials)
      uid = user['users'][0]['localId'] #busqeda interna de firebase     
      users_data = db.child("users").child(uid).get().val()
      response = {
        "user": users_data
      }
      return response
    except Exception as e:
      print(e)
      raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
      

@app.post(
  "/signup/",
  status_code=status.HTTP_202_ACCEPTED,
  summary="Create a user",
  description="create a user",
  tags=["Auth"],
)
async def create_user_post(cliente: clientesSignup):
    try:
      user = auth.create_user_with_email_and_password(cliente.email, cliente.password)
      userI = auth.get_account_info(user['idToken'])
      uid = userI['users'][0]['localId']
      db.child("users").child(uid).set({"email": cliente.email, "nivel": "1"})
      response = {
        "message": "User created successfully",
      }
      return response
    except Exception as e:
      print(f"Error: {e}")
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
