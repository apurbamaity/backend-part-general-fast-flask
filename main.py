# fastapi endpoint not flask-restfull

from fastapi import FastAPI, status, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


from models.hero import Hero
from basemodels import Greetbody


from sqlalchemy import text
from sqlmodel import create_engine
from dbfunctions import insert_single_hero, insert_multiple_heroes
from asyncer import asyncify
from pydantic import BaseModel
from typing import Dict, Any

from datetime import datetime, timedelta
import jwt

from dotenv import load_dotenv
import os

import uvicorn


load_dotenv()


# pydantic model for request validation
class InsertRequest(BaseModel):
    table_name: str
    data: Dict[str, Any]


app = FastAPI()


# Allow all origins (for dev) — change in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # Or ["http://localhost:5173"] for Vite dev server
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],
)

ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_HOURS = (int)(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS"))
EXPECTED_BEARER_TOKEN = os.getenv("EXPECTED_BEARER_TOKEN")


@app.get("/")
async def home():
    return {"message": "Welcome to the Hero API"}


@app.post("/insert_single_hero")
async def root(record: InsertRequest):
    try:
        table_name = record.table_name
        data = record.data
        print("data", data)
        new_hero = await asyncify(insert_single_hero)(table_name, data)
        return {"message": "Inserted single hero", "hero": new_hero}
    except Exception as e:
        print(f"Error parsing request: {e}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"error": "Bad Gateway, please try later"},
        )


# @app.middleware("http")
# async def verify_bearer_token(request: Request, call_next):
#     print("cpming here")
#     auth_header = request.headers.get("Authorization")
#     print('auth_header', auth_header)

#     if request.method == "OPTIONS":
#         return await call_next(request)

#     if not auth_header or not auth_header.startswith("Bearer "):
#         print("here it comes no auth header")
#         return JSONResponse(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             content={"error": "Missing or invalid Authorization header"}
#         )
#     token = auth_header.replace("Bearer ", "")
#     if token != EXPECTED_BEARER_TOKEN:
#         return JSONResponse(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             content={"error": "Invalid bearer token"}
#         )
#     # Token is valid, proceed with the request
#     response = await call_next(request)
#     return response


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Sample endpoint (similar to the FastMCP greet tool)
@app.post("/greet")
async def login_func(request: Greetbody):
    # return {"result": f"Hello user welocome to the program, {request.name}!"}

    # login verification logic foes here if user registered
    if request.name != "apurba":
        return {"result": f"Hello user welocome to the program, {request.name}!"}

    token = create_access_token({"sub": request.name})
    print("token", token)
    return {"access_token": token}


def verify_jwt(token: str):
    print("********************************* HERE1")
    print(f"********************************* HERE2 token ->{token}")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"********************************* HERE2 payload ->{payload}")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )


@app.get("/protected")
def protected(request: Request):
    print("hjereer it comes ************************************************888")

    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    token = auth_header.split(" ")[1]
    try:
        payload = verify_jwt(token)  # verifies and decodes JWT
        print("payload verified", payload)
        return JSONResponse(
            status_code=201,
            content={
                "orders_new_1": [
                    {"id": 1, "item": "Laptop", "owner": payload["sub"]},
                    {"id": 2, "item": "Headphones", "owner": payload["sub"]},
                ]
            },
        )
    except:
        print("some error occured while verifying")
        return JSONResponse(
            status_code=401, content={"message": "you are unauthorized"}
        )


def verify_jwt_in_header(request: Request):
    auth_header = request.headers.get("Authorization")
    print(
        "coming in `verify_jwt_in_header` with depends method from requestbody with auth header =>",
        auth_header,
    )
    if request.method == "OPTIONS":
        return "ok"

    if not auth_header or not auth_header.startswith("Bearer "):
        print("here it comes no auth header")
        return False
    token = auth_header.replace("Bearer ", "")
    if token != EXPECTED_BEARER_TOKEN:
        return False
    return True


@app.get("/protectedmethod2")
def protected(request: Request, isAuthorised=Depends(verify_jwt_in_header)):
    print(
        "coming in `protectedmethod2` with depends method from requestbody ",
        isAuthorised,
    )
    if isAuthorised:
        return JSONResponse(
            status_code=201,
            content={
                "orders_new_1": [
                    {"id": 1, "item": "Laptop"},
                    {"id": 2, "item": "Headphones"},
                ]
            },
        )
    else:
        return JSONResponse(
            status_code=401, content={"message": "you are unauthorized"}
        )


if __name__ == "__main__":
    # Run the server on a custom port
    uvicorn.run(app, log_level="info")
