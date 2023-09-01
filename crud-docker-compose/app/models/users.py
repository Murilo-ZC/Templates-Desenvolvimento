from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

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