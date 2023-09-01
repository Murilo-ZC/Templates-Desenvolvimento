from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Cria um conjunto de usuários para simular um banco de dados
fake_users_db = {
    "red": {
        "username": "red",
        "full_name": "Ask Ketchum",
        "email": "pikachu@mail.com",
        "hashed_password": "charmander",
        "disabled": False,
    },
    "gary": {
        "username": "gary",
        "full_name": "Gary Oak",
        "email": "grandson@mail.com",
        "hashed_password": "eevee",
        "disabled": True,
    },
}


app = FastAPI()

# Para utilizar o validador de segurança, é necessário criar uma instância do OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Classes que definem os usuários
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str | None = None

    


def get_user(db, username: str) -> User:
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    user = get_user(fake_users_db, token)
    return user

# Funções para lidar com os usuários, todas demandam um token de autenticação
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# Função para autenticar o usuário
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user_dict = User(**fake_users_db.get(form_data.username))
    except:
        raise HTTPException(status_code=400, detail="User not found")
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not form_data.password == user_dict.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_dict.username, "token_type": "bearer"}

# Nossa API
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}