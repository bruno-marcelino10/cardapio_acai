from flask import Flask, render_template, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from database_setup import users, cardapio

app = Flask(__name__)
app.secret_key = "key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///admins.sqlite3"
db = SQLAlchemy(app)

@app.route("/")
def produtos():
    return render_template("index.html", values = cardapio.query.all()) # lista de objetos contendo produtos e caracteristicas)

@app.route("/unidades")
def unidades():
    return render_template("unidades.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        login_existente = users.query.filter_by(email = email, senha = senha).first()
        if login_existente:
            session["email"] = email
            session["senha"] = senha
            return redirect(url_for("admin"))                       
        else:
            flash("E-mail ou senha incorretos!", "info")
            return render_template("login.html")
            
    else:
        if email in session and senha in session:
            return redirect(url_for("admin"))
        else:
            return render_template("login.html")

@app.route("/login/admin") 
def admin(): # só pode acessar se estiver logado
    if email in session and senha in session:
        email = session["email"]
        senha = session["senha"]
        return render_template("admin.html")
    else:
        return redirect(url_for("login.html"))
    
@app.route("/login/admin/lista_admins")
def lista_admins(): # GET database
    return render_template("lista_admins.html", values = users.query.all()) # lista de objetos contendo email e senha

@app.route("/login/admin/cadastro", methods = ["GET", "POST"])
def cadastro():
    if request.method == "POST":
        if request.form["adicionar_email"] and request.form["adicionar_senha"]: # formulario de adicionar preenchido
            novo_email = request.form["adicionar_email"]
            nova_senha = request.form["adicionar_senha"]

            usuario = users(novo_email, nova_senha)
            db.session.add(usuario)
            db.session.commit()
            flash("usuário adicionado!", "info")
            return render_template("cadastro.html")

        elif request.form["remover_email"] and request.form["remover_senha"]: # formulario de remover preenchido
            remover_email = request.form["remover_email"]
            remover_senha = request.form["remover_senha"]

            login_existente = users.query.filter_by(email = email, senha = senha).first()
            if login_existente:
                users.query.filter_by(email = email, senha = senha).delete()
                flash("Usuário removido!", "info")
                return render_template("cadastro.html")
            else:
                flash("Este usuário não existe!", "info")
                return render_template("cadastro.html")

        else:
            render_template("cadastro.html") # usuário preencheu somente um dos campos
    else:
        render_template("cadastro.html")

@app.route("/login/admin/alterar_cardapio", methods = ["GET", "POST"])
def alterar_cardapio():
    if request.method == "POST":
        if request.form["nome"] and request.form["ingredientes"] and request.form["preco"]: # formulario de adicionar preenchido
            nome = request.form["nome"]
            ingredientes = request.form["ingredientes"]
            preco = request.form["preco"]

            produto = cardapio(nome, ingredientes, preco)
            db.session.add(produto)
            db.session.commit()
            flash("Produto adicionado!", "info")

            render_template(url_for("admin"))
        else: 
            flash("Produto inválido!")
            return render_template("alterar_cardapio.html")
        
    return render_template("alterar_cardapio.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
