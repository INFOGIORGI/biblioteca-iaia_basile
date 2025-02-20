from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'iaia_basile'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        if db.logIn(mysql, email, password):
            return redirect(url_for("users"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        tessera = request.form.get("tessera")
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        data_nascita = request.form.get("datanascita")
        email = request.form.get("email")
        password = request.form.get("password")
        conf = request.form.get("confirm_password")

        if password == conf:
            if db.registrazione(mysql, tessera, nome, cognome, data_nascita, email, password):
                return redirect(url_for("log_in"))
    return render_template("register.html")

@app.route("/user", methods=["GET", "POST"])
def users():
    keyword = request.form.get("keyword", "") if request.method == "POST" else ""
    libri = db.ricercaParolaChiave(mysql, "keyword", 1)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)

@app.route("/ordinaPerAutore")
def ordina_per_autore():
    return render_template("user.html", libri=db.ordinamento(mysql, 1), autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

@app.route("/ordinaPerTitolo")
def ordina_per_titolo():
    return render_template("user.html", libri=db.ordinamento(mysql, 0), autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

@app.route("/filtraGenere", methods=["POST"])
def filtra_genere():
    genere = request.form.get("genere")
    return render_template("user.html", libri=db.filtraGenere(mysql, genere), autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        titolo = request.form.get("titolo")
        isbn = request.form.get("isbn")
        genere = request.form.get("genere")
        piano = request.form.get("piano")
        scaffale = request.form.get("scaffale")
        posizione = request.form.get("posizione")
        autori = request.form.get("autori")
        riassunto = request.form.get("riassunto")
        message = 1 if db.insertLibrio_Catalogo(mysql, titolo, isbn, genere, piano, scaffale, posizione, autori, riassunto) else 0
        return render_template("admin.html", message=message)
    return render_template("admin.html", message=3)

@app.route("/aggiungiRiassunto", methods=["POST"])
def aggiungi_riassunto():
    isbn = request.form.get("isbn")
    riassunto = request.form.get("riassunto")
    if db.aggiungi_riassunto(mysql, isbn, riassunto):
        return redirect(url_for("users"))
    return "Errore nell'aggiunta del riassunto", 400

app.run(debug=True)