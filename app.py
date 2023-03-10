from flask import Flask, render_template, url_for, request, session, flash, redirect
from models import db, users, cardapio

app = Flask(__name__)
app.secret_key = "key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/produtos")
def produtos():
    return render_template("produtos.html", values = users.query.all()) # lista de objetos contendo produtos e caracteristicas)

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
        admin = {"email": "admin@admin.com.br", "senha" : "admin"}
        if login_existente or (email == admin["email"] and senha == admin["senha"]):
            session["email"] = email
            session["senha"] = senha
            return redirect(url_for("admin"))                       
        else:
            flash("E-mail ou senha incorretos!", "info")
            return render_template("login.html")
    else:
            return render_template("login.html")

@app.route("/logout")
def logout():
    del session["email"]
    del session["senha"]
    return redirect(url_for('home'))

@app.route("/login/admin") 
def admin(): # só pode acessar se estiver logado
    if "email" in session and "senha" in session:
        return render_template("admin.html")
    else:
        return redirect(url_for("login.html"))
    
@app.route("/login/admin/cadastro", methods = ["GET", "POST"])
def cadastro(): # GET and UPDATE database
    if request.method == "POST":
        novo_email = request.form["adicionar_email"]
        nova_senha = request.form["adicionar_senha"]

        login_existente = users.query.filter_by(email = novo_email, senha = nova_senha).first()
        if not login_existente:
            usuario = users(novo_email, nova_senha)
            db.session.add(usuario)
            db.session.commit()
            flash("usuário adicionado!", "info")
            return redirect(url_for('cadastro'))
        else:
            flash("O usuário já consta na nossa base de dados", "info")
            return render_template("cadastro.html", values = users.query.all())
    else:
        if "email" in session and "senha" in session:
            return render_template("cadastro.html", values = users.query.all())
        else:
            return redirect(url_for("login.html"))

@app.route("/login/admin/alterar_cardapio", methods = ["GET", "POST"])
def alterar_cardapio():
    if request.method == "POST":
        novo_nome = request.form["nome"]
        novo_ingredientes = request.form["ingredientes"]
        novo_preco = request.form["preco"]
        
        produto_existente = users.query.filter_by(nome = novo_nome, ingredientes = novo_ingredientes, preco = novo_preco).first()
        if not produto_existente:
            produto = cardapio(novo_nome, novo_ingredientes, novo_preco)
            db.session.add(produto)
            db.session.commit()
            flash("Produto adicionado!", "info")
            return redirect(url_for('cadastro'))
        else:
            flash("O usuário já consta na nossa base de dados", "info")
            return render_template("cadastro.html", values = users.query.all())    
    else:
        if "email" in session and "senha" in session:
            return render_template("alterar_cardapio.html")
        else:
            return redirect(url_for("login.html"))

if __name__ == "__main__":    
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)