from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

# Constantes
DB_USER = "admin"
DB_PASSWORD = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"
DB_NAME = "banco-app"

# Cria a engine de dados para o postgres
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Cria uma seção no banco
session = Session(engine)

# Cria a base para os modelos
Base = declarative_base()

#Define a tabela base
class User(Base):
    """
    Classe que representa a tabela de Usuários do sistema
    """
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, password={self.password})>"

# Cria a tabela no banco se ela já não existir
Base.metadata.create_all(engine, checkfirst=True)

app = FastAPI()

@app.get("/get_users")
def get_users():
    users = session.query(User).all()
    return {"data":users}




