from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuario.sqlite3"
Session(app)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.nome
    
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


@app.route("/")
def index():
    if session.get("user"):
        return redirect(url_for("inicio"))
    else:
        return render_template("index.html", titulo = "Página Inicial")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        user = User.query.filter_by(email=email, senha=senha).first()
        if user:
            session["user"] = user.id
            return redirect(url_for("inicio"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html", titulo = "Login")

@app.route("/inicio")
def inicio():
    user_id = session.get("user")
    if user_id:
        user = User.query.get(user_id)
        return render_template("inicio.html",nome_usuario = user.nome,titulo = "Inicio")
    else:
        return redirect(url_for("login"))

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]
        user = User(nome, email, senha)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("cadastro.html", titulo="Cadastro de Usuário")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
