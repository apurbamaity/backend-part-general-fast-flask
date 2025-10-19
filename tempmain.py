from fastapi import FastAPI, Request, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import jwt
import uvicorn
from dotenv import load_dotenv
import os

from models import Greetbody

load_dotenv()


ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_HOURS = os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")
EXPECTED_BEARER_TOKEN = os.getenv("EXPECTED_BEARER_TOKEN")


security = HTTPBearer()


# Initialize FastAPI app
app = FastAPI(title="Secure FastAPI Server")


# Middleware for bearer token verification
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # list of allowed origins
    allow_credentials=True,  # allow cookies, authorization headers, etc.
    allow_methods=["*"],  # allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # allow all headers
)


# Helper: Create JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Helper: Verify JWT token
# JWT verification dependency
# def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     print("********************************* HERE1")
#     token = credentials.credentials
#     print(f"********************************* HERE2 token ->{token}")

#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print(f"********************************* HERE2 payload ->{payload}")
#         return payload
#     except jwt.ExpiredSignatureError:
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
#     except jwt.InvalidTokenError:
#        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


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


# Sample endpoint (similar to the FastMCP greet tool)
@app.post("/greet")
async def login_func(request: Greetbody):
    return {"result": f"Hello user welocome to the program, {request.name}!"}
    # if request.name != 'apurba':
    #     return {"result": f"Hello user welocome to the program, {request.name}!"}

    # token = create_access_token({"sub": request.name})
    # print('token', token)
    # return {'access_token' : token}


def check_auth_header(request: Request, authorization: str = Header(None)):
    auth_header = request.headers.get("Authorization")
    print("coming hwre with depends method from requestbody ", auth_header)
    if request.method == "OPTIONS":
        return "ok"

    if not auth_header or not auth_header.startswith("Bearer "):
        print("here it comes no auth header")
        return "notok"
    token = auth_header.replace("Bearer ", "")
    if token != EXPECTED_BEARER_TOKEN:
        return "notok"
    return "ok"


@app.post("/greetdepends")
async def login_func(
    request: Greetbody, authenticatedcheck: str = Depends(check_auth_header)
):
    if authenticatedcheck == "ok":
        return {"result": f"Hello user welocome to the program, {request.name}!"}
    else:
        return {"result": "invalid header token plese verify"}
    # if request.name != 'apurba':
    #     return {"result": f"Hello user welocome to the program, {request.name}!"}

    # token = create_access_token({"sub": request.name})
    # print('token', token)
    # return {'access_token' : token}


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
        print("payload", payload)
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
    # return JSONResponse(
    #     status_code =  201,
    #     content = {"orders_new_1": [
    #        {"id": 1, "item": "Laptop", "owner": payload["sub"]},
    #        {"id": 2, "item": "Headphones", "owner": payload["sub"]}
    #    ]}
    # )


# Protected endpoints
@app.get("/orders")
def get_orders(payload: dict = Depends(verify_jwt)):
    return {
        "orders_new": [
            {"id": 1, "item": "Laptop", "owner": payload["sub"]},
            {"id": 2, "item": "Headphones", "owner": payload["sub"]},
        ]
    }


if __name__ == "__main__":
    # Run the server on a custom port
    uvicorn.run(app, log_level="info")
