import requests as http_request
from flask import make_response
from flask import Flask
from database.database import db
from flask import jsonify, request, render_template
from database.models import User

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

# Verifica se o parâmetro create_db foi passado na linha de comando
import sys
if len(sys.argv) > 1 and sys.argv[1] == 'create_db':
    # cria o banco de dados
    with app.app_context():
        db.create_all()
    # Finaliza a execução do programa
    print("Database created successfully")
    sys.exit(0)



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

@app.route("/user-login", methods=["GET"])
def user_login():
    return render_template("login.html")


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
    # response.set_cookie("token", token_data.json()['token'])
    return response


@app.route("/user-register", methods=["GET"])
def user_register():
    return render_template("register.html")

@app.route("/content", methods=["GET"])
@jwt_required()
def content():
    return render_template("content.html")

@app.route("/error", methods=["GET"])
def error():
    return render_template("error.html")