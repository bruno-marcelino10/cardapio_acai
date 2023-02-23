from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    
    id = db.Column("id", db.Integer, primary_key = True)
    email = db.Column("email", db.String(100))
    senha = db.Column("senha", db.String(100))

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

class cardapio(db.Model):
    
    id = db.Column("id", db.Integer, primary_key = True)
    nome = db.Column("nome", db.String(100))
    preco = db.Column("preco", db.Float(100))
    ingredientes = db.Column("ingredientes", db.String(100))
    
    def __init__(self, nome, preco, ingredientes):
        self.nome = nome
        self.preco = preco
        self.ingredientes = ingredientes