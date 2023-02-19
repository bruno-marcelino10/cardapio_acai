from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/")
def produtos():
    return render_template("index.html")

@app.route("/unidades")
def unidades():
    return "Em construção"

@app.route("/contato")
def contato():
    return "Em construção"

if __name__ == "__main__":
    app.run()
