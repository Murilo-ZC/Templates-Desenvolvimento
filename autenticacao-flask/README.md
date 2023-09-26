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
- [Data Management With Python, SQLite, and SQLAlchemy](https://realpython.com/python-sqlite-sqlalchemy/#working-with-sqlalchemy-and-python-objects)



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

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False)
  password = Column(String(50), nullable=False)

  def __repr__(self):
    return f'<User:[id:{self.id}, name:{self.name}, email:{self.email}, password:{self.password}]>'
  
  def serialize(self):
    return {
      "id": self.id,
      "name": self.name,
      "email": self.email,
      "password": self.password}
```

Agora, vamos ligar nosso modelo com a aplicação Flask. Para isso, vamos alterar o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
from flask import Flask
from database.database import db
from flask import jsonify, request
from database.models import User

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

> ***IMPORTANTE:*** Para que a criação das tabelas possa ser executada com sucesso, é necessário importar todas as classes que implementam a classe base no programa. Caso contrário, as demais tabelas não serão criadas.

A execução do programa vai criar as tabelas no banco de dados. O arquivo do banco de dados será criado em ***var/main-instance/project.db***. Agora, vamos criar as rotas para o CRUD de usuários. Para isso, vamos alterar o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
from flask import Flask
from database.database import db
from flask import jsonify, request
from database.models import User

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
@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return_users = []
    for user in users:
        return_users.append(user.serialize())
    return jsonify(return_users)

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    return jsonify(user.serialize())

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(name=data["name"], email=data["email"], password=data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.json
    user = User.query.get(id)
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
    db.session.commit()
    return jsonify(user.serialize())

@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify(user.serialize())
```

Agora, vamos avaliar as rotas:

- GET /users: Retorna todos os usuários cadastrados no banco de dados
- GET /users/<int:id>: Retorna o usuário com o id informado
- POST /users: Cria um novo usuário
- PUT /users/<int:id>: Atualiza o usuário com o id informado
- DELETE /users/<int:id>: Deleta o usuário com o id informado

Agora, vamos testar as rotas. Para isso, vamos executar o comando abaixo, dentro do diretório ***"src"***:

```bash
python -m flask --app main run
```

E testamos as rotas com o Thunber Client. Para isso, vamos acessar a URL ***http://localhost:5000/users***. Cada vez que o método **POST** for utilizado, um novo registro será criado no banco de dados. Para testar o método **POST**, vamos utilizar o Thunber Client. Para isso, vamos acessar a URL ***http://localhost:5000/users***, e vamos inserir o seguinte JSON:

```json
{
  "name": "Teste",
  "email": "mail@mail.com",
    "password": "123456"
}
```

Agora vamos adicionar nossa página de login, onde o usuário vai informar o email e a senha. Para isso, vamos criar o arquivo ***"login.html"***, dentro do diretório ***"templates"***. Dentro deste arquivo, vamos inserir o código abaixo:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Auth</title>
</head>
<body>
    <h1>Login</h1>
    <form action="http://localhost:5000/login" method="POST">
        <label for="username">Username</label>
        <input type="text" name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <input type="submit" value="Login">
    </form>
    <p>Don't have an account? <a href="http://localhost:5000/user-register">Register</a></p>    
</body>
</html>
```

E vamos alterar o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
from flask import Flask
from database.database import db
from flask import jsonify, request, render_template
from database.models import User

app = Flask(__name__, template_folder="templates")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# Código anterior suprimido para facilitar a localização nos códigos

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")
```

Agora nossa página de login está pronta. Vamos criar a página de registro. Para isso, vamos criar o arquivo ***"register.html"***, dentro do diretório ***"templates"***. Dentro deste arquivo, vamos inserir o código abaixo:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register User</title>
</head>
<body>
    <h1>Register User</h1>
    <form action="http://localhost:5000/register" method="POST">
        <label for="username">Username</label>
        <input type="text" name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required>
        <input type="submit" value="Register">
    </form>
    <p>Already have an account? <a href="http://localhost:5000/user-login">Login</a></p>
</body>
</html>
```

Agora, ajustamos o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
# Código superior suprimido para facilitar a localização nos códigos
@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")
```

E por fim, vamos criar nossa página que será protegida por autenticação e a página que indica que uma falha aconteceu. Para a página de conteúdo protegido, vamos criar o arquivo ***"content.html"***, dentro do diretório ***"templates"***. Dentro deste arquivo, vamos inserir o código abaixo:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conteúdo Secreto</title>
</head>
<body>
    <h1>Conteúdo Secreto</h1>
    <img src="https://picsum.photos/300" width="300" height="300"/>
    <button onClick="window.location.reload();">Refresh Page</button>
</body>
</html>
```

E para a página de erro, vamos criar o arquivo ***"error.html"***, dentro do diretório ***"templates"***. Dentro deste arquivo, vamos inserir o código abaixo:

```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Something went wrong</title>
</head>
<body>
    <h1>Algo deu errado</h1>
    <img src="http://placekitten.com/300/300" width="300" height="300"/>
    <p>Vamos novamente? <a href="http://localhost:5000/user-login">Home</a></p>
</body>
</html>
```

E em nosso código no arquivo ***"main.py"***, dentro do diretório ***"src"***, vamos inserir o código abaixo:

```python
# Código anterior suprimido
@app.route("/content", methods=["GET"])
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")
```

Agora para lidar com a autenticação dos usuários, vamos utilizar a biblioteca ***JWTManager*** do ***flask_jwt_extended***. Para isso, vamos adicionar a biblioteca no arquivo ***"requirements.txt"***. Agora, vamos atualizar nosso arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
# Código anterior suprimido para facilitar a localização nos códigos

from flask_jwt_extended import JWTManager, set_access_cookies

app = Flask(__name__, template_folder="templates")
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "goku-vs-vegeta" 
# Seta o local onde o token será armazenado
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt = JWTManager(app)

# Restante do código foi suprimido para facilitar a localização nos códigos
```

Agora, vamos realizar a atualização do nosso arquivo fonte para gerar as chaves JWT de autenticação, quando um usuário solicitar. ***IMPORTANTE:*** este método vai verificar o usuário no banco de dados e então gerar a chave JWT caso o usuário e a senha do usuário estejam corretos. Para isso, vamos alterar o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
# Código anterior suprimido para facilitar a localização nos códigos

# Método para criar um token
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
@app.route("/token", methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # Query your database for username and password
    user = User.query.filter_by(email=username, password=password).first()
    if user is None:
        # the user was not found on the database
        return jsonify({"msg": "Bad username or password"}), 401
    
    # create a new token with the user id inside
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id })

# Restante do código foi suprimido para facilitar a localização nos códigos
```

Agora, para proteger as rotas, utilizar o decorador ***jwt_required***. Para isso, vamos alterar o arquivo ***"main.py"***, dentro do diretório ***"src"***. Dentro deste arquivo, vamos inserir o código abaixo:

```python
# Código anterior suprimido para facilitar a localização nos códigos

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

# Restante do código foi suprimido para facilitar a localização nos códigos
```

Assim, quando essa rota for acessada sem a chave de usuário, ela não será carregada.
Agora vamos ajustar o comportamento da rota de login.

```python	
import requests as http_request

# Código anterior suprimido para facilitar a localização nos códigos

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", None)
    password = request.form.get("password", None)
    # Verifica os dados enviados não estão nulos
    if username is None or password is None:
        # the user was not found on the database
        return render_template("error.html", message="Bad username or password")
    # faz uma chamada para a criação do token
    token_data = http_request.post("http://localhost:5000/token", json={"username": username, "password": password})
    if token_data.status_code != 200:
        return render_template("error.html", message="Bad username or password")
    # recupera o token
    response = make_response(render_template("content.html"))
    set_access_cookies(response, token_data.json()['token'])
    return response

# Restante do código foi suprimido para facilitar a localização nos códigos
```



## Docker

- TODO