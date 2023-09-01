from fastapi import FastAPI, Body
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.users import Base, User

# Constantes
DB_USER = "admin"
DB_PASSWORD = "postgres"
# DB_HOST = "172.17.0.3"
DB_HOST = "compose-banco-container"
DB_PORT = "5432"
DB_NAME = "banco-app"

# Cria a engine de dados para o postgres
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Cria uma seção no banco
session = Session(engine)

# Cria a tabela no banco se ela já não existir
Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI()

@app.get("/get_users")
def get_users():
    users = session.query(User).all()
    return {"data":users}

@app.get("/get_user/{id}")
def get_user(id: int):
    user = session.query(User).filter(User.id == id).first()
    return {"data":user}

@app.post("/create_user")
def create_user(data: dict = Body()):
    usuario = User(name = data['name'], email = data['email'], password = data['password'])
    session.add(usuario)
    session.commit()
    return {"data": "Usuário criado com sucesso!"}

@app.put("/update_user")
def update_user(data: dict = Body()):
    usuario = session.query(User).filter(User.id == data['id']).first()
    usuario.name = data['name']
    usuario.email = data['email']
    usuario.password = data['password']
    session.commit()
    return {"data": "Usuário atualizado com sucesso!"}

@app.delete("/delete_user")
def delete_user(data: dict = Body()):
    usuario = session.query(User).filter(User.id == data['id']).first()
    session.delete(usuario)
    session.commit()
    return {"data": "Usuário deletado com sucesso!"}
