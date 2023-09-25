# Criando uma aplicação com Autenticação e Flask v1.0

O objetivo deste projeto é criar uma aplicação que é executada no servidor Flask, com autenticação de usuário. Ela será uma aplicação básica, com o objetivo de apresentar como criar uma aplicação com autenticação de usuário. Ela será deployada em um container Docker.

## Requisitos

- Python >= 3.8
- Flask
- Flask-SQLAlchemy
- Docker

## Recomendação de Leitura

- [Flask](https://flask.palletsprojects.com/en/2.3.x/)
- [Flask Quickstart](https://flask.palletsprojects.com/en/2.3.x/quickstart/#a-minimal-application)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)



## Instalação

As bibliotecas necessárias para a execução do projeto estão no arquivo `requirements.txt`. Para instalar, execute o comando abaixo:

```bash
python -m pip install -r requirements.txt
```

> ***ATENÇÃO:*** *É recomendado a utilização de um ambiente virtual para a instalação das bibliotecas. Para mais informações, acesse o [link](https://docs.python.org/pt-br/3/library/venv.html).*

> ***IMPORTANTE:*** A instalação do PyCaret leva um tempo considerável. Estamos trabalhando com a versão completa do pacote de instalação. Para mais informações, acesse o [link](https://pycaret.org/install/).

Para criar um ambiente virtual, execute o comando abaixo (para Windows):

```bash
python -m venv .
cd Scripts
activate
```

O que vai acontecer com a sequencia de comandos acima, um ambiente virtual será criado na pasta atual. Em sequencia, navegamos para o diretório ***Scripts***, e ativamos o ambiente virtual executando o script ***activate***. Na sequencia, vamos avaliar se o ambiente virtual foi ativado corretamente, executando o comando abaixo:

```bash
where python
```

A saída esperada é a seguinte:

```bash
C:\Users\usuario\Documents\autenticacao-flask\Scripts\python.exe
C:\Users\usuario\AppData\Local\Programs\Python\Python38\python.exe
```

Os diretórios que são criados para o ambiente virtual são:
- Include
- Lib
- Scripts

Esses diretórios e o arquivo ***pyvenv.cfg*** são criados na pasta onde o comando ***python -m venv .*** foi executado. Eles podem ser adicionados ao ***.gitignore***, pois se for necessário recriar esses diretórios, basta recriar o venv. Exemplo de gitignore:

```gitignore
Include
Lib
Scripts
pyvenv.cfg
```

Para desativar o ambiente virtual, execute o comando abaixo, dentro do diretório Scripts:

```bash
deactivate
```

## Desenvolvimento do Projeto

Depois de criado o ambiente virtual, vamos criar uma aplicação básica padrão de Flask, apenas para verificarmos a instalação do sistema. Dentro do diretório ***"src"***, crie um arquivo chamado ***"main.py"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

```

Agora vamos executar a aplicação:
    
```bash
python -m flask --app src.main run
```

Agora, utilizando o Thunber Client, vamos acessar a URL ***http://localhost:5000***. A saída esperada é a seguinte:

```html
<p>Hello, World!</p>
```

Até aqui temos o exemplo de introdução do Flask. Agora vamos criar as rotas para implementar um CRUD de usuários. Por hora, nossa aplicação vai conversar com um banco de dados SQLite. Para isso, vamos criar um diretório chamado ***"database"***, e dentro dele, vamos criar um arquivo chamado ***"database.py"***. Vamos utilizar o SQLAlchemy para fazer a conexão com o banco de dados. Para isso, vamos instalar a biblioteca SQLAlchemy, executando o comando abaixo:

```python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
```

Agora, vamos criar o arquivo ***"models.py"***, dentro do diretório ***"database"***. Dentro deste arquivo, vamos criar a classe ***"User"***, que vai representar a tabela de usuários do banco de dados. O código abaixo representa a classe ***"User"***:

```python
from sqlalchemy import Column, Integer, String
from database.database import db

class User(db.Model):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False)
  password = Column(String(50), nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, name:{self.name}, email:{self.email}, password:{self.password}]>'
```

Agora, vamos ligar nosso modelo com a aplicação Flask. Para isso, vamos alterar o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
from flask import Flask
from database.database import db

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# Verifica se o parâmetro create_db foi passado na linha de comando
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```

Agora, vamos criar o banco de dados. Para isso, vamos executar o comando abaixo:

```bash
python src/main.py create_db
```

A execução do programa vai criar as tabelas no banco de dados. O arquivo do banco de dados será criado em ***var/main-instance/project.db***. Agora, vamos criar as rotas para o CRUD de usuários. Para isso, vamos alterar o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
from flask import Flask
from database.database import db

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# Verifica se o parâmetro create_db foi passado na linha de comando
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Adicionando as rotas CRUD para a entidade User
from flask import jsonify, request
from database.models import User

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify(users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user)

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user)

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
    db.session.commit()
    return jsonify(user)

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user)
```

Agora, vamos avaliar as rotas:

- GET /users: Retorna todos os usuários cadastrados no banco de dados
- GET /users/<int:id>: Retorna o usuário com o id informado
- POST /users: Cria um novo usuário
- PUT /users/<int:id>: Atualiza o usuário com o id informado
- DELETE /users/<int:id>: Deleta o usuário com o id informado

Agora, vamos testar as rotas. Para isso, vamos executar o comando abaixo, dentro do diretório ***"src"***:

```bash
python -m flask --app src.main run
```

E testamos as rotas com o Thunber Client. Para isso, vamos acessar a URL ***http://localhost:5000/users***. A saída esperada é a seguinte:




## Docker

- TODO