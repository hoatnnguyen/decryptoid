from fastapi import Depends, FastAPI, HTTPException, Form, UploadFile, File
from typing import Annotated, Union
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .authentication import *
from .database import SessionLocal, engine
from .cipher_utils import simple_substitution_decrypt, simple_substitution_encrypt, double_transposition_decrypt, double_transposition_encrypt, rc4_decrypt, rc4_encrypt

models.Base.metadata.create_all(bind=engine)

ACCESS_TOKEN_EXPIRE_MINUTES=43200

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_by_username = crud.get_user_by_username(db, username=user.username)
    db_user_by_email = crud.get_user_by_email(db, email=user.email)
    if db_user_by_email or db_user_by_username:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=schemas.UserLoginResponse)
async def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db=db, user=user)
    if not authenticated_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = crud.get_user_by_username(db=db, username=user.username)
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, expires_delta=access_token_expires
    )

    return {
        "username": db_user.username,
        "email": db_user.email,
        "accessToken": access_token
    }

# @app.post("/cipheractivity", response_model=schemas.CipherActivityResponse)
@app.post("/cipheractivity/file")
async def cipherActivity(file: UploadFile = File(...), cipherAlgo: int = Form(...), key: str = Form(...), cipherMode: int = Form(...), user_id=Depends(RequiredLogin()), db: Session = Depends(get_db)):

    contents = ""

    # print(f"Input text: {inputText}")
    print(f"cipher algo: {cipherAlgo}")
    print(f"key: {key}")
    print(f"cipherMode : {cipherMode}")
    if file:
        print(f"File name: {file.filename}")
        content = await file.read()
        contents = content.decode('utf-8')
        print(contents)

    print(f"content: {contents}")

    cipher_algo_arr = ["Simple substitution", "Double transposition", "rc4"]
    cipher_mode_arr = ["encrypt", "decrypt"]
    
    output = ""
    if cipherAlgo == 1:
        if len(key) != 26:
            raise HTTPException(status_code=400, detail="Key length must be 26 characters for simple substitution")
        if cipherMode == 1:
            output = simple_substitution_encrypt(contents, key)
        else:
            output = simple_substitution_decrypt(contents, key)

    elif cipherAlgo == 2:
        try:
            key = int(key)
        except ValueError:
            raise HTTPException(status_code=400, detail="Key must be an integer for double transposition.")
        if cipherMode == 1:
            output = double_transposition_encrypt(contents, key)
        else:
            output = double_transposition_decrypt(contents, key)

    elif cipherAlgo == 3:
        if cipherMode == 1:
            output = rc4_encrypt(contents, key)
        else:
            output = rc4_decrypt(contents, key)

    print(f"user_id: {user_id}")
    db_cipher_activity = crud.create_cipher_activity(db, contents, cipher_algo_arr[cipherAlgo-1], cipher_mode_arr[cipherMode-1], key, user_id)
    print(f"cipher_activity: {db_cipher_activity}")

    print(f"output: {output}")
    return output

@app.post("/cipheractivity/inputText")
async def cipherActivity(inputText: str = Form(...), cipherAlgo: int = Form(...), key: str = Form(...), cipherMode: int = Form(...), user_id=Depends(RequiredLogin()), db: Session = Depends(get_db)):

    contents = ""

    # print(f"Input text: {inputText}")
    print(f"cipher algo: {cipherAlgo}")
    print(f"key: {key}")
    print(f"cipherMode : {cipherMode}")

    contents = inputText
    print(f"content: {contents}")
    print(f"content length: {len(contents)}")

    cipher_algo_arr = ["Simple substitution", "Double transposition", "rc4"]
    cipher_mode_arr = ["encrypt", "decrypt"]
    
    output = ""
    if cipherAlgo == 1:
        if len(key) != 26:
            raise HTTPException(status_code=400, detail="Key length must be 26 characters for simple substitution")
        if cipherMode == 1:
            output = simple_substitution_encrypt(contents, key)
        else:
            output = simple_substitution_decrypt(contents, key)

    elif cipherAlgo == 2:
        try:
            key = int(key)
        except ValueError:
            raise HTTPException(status_code=400, detail="Key must be an integer for double transposition.")
        if cipherMode == 1:
            output = double_transposition_encrypt(contents, key)
        else:
            output = double_transposition_decrypt(contents, key)

    elif cipherAlgo == 3:
        if cipherMode == 1:
            output = rc4_encrypt(contents, key)
        else:
            output = rc4_decrypt(contents, key)

    print(f"user_id: {user_id}")
    db_cipher_activity = crud.create_cipher_activity(db, contents, cipher_algo_arr[cipherAlgo-1], cipher_mode_arr[cipherMode-1], key, user_id)
    print(f"cipher_activity: {db_cipher_activity}")

    print(f"output: {output}")
    return output
