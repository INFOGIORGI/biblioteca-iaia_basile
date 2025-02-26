from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for
import db

app = Flask(__name__)

app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = '5di'
app.config['MYSQL_PASSWORD'] = 'colazzo'
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
        value=db.logIn(mysql, email, password)
        print(value)
        if value =="admin":
            print("admin")
            return redirect(url_for("admin"))
        elif value=="user":
            print("user")
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
            if db.registrazione(mysql, tessera, nome, cognome, data_nascita, email, password,0):
                return redirect(url_for("log_in"))
    return render_template("register.html")

@app.route("/user", methods=["GET", "POST"])
def users():
    libri = db.getLibri(mysql)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)

@app.route("/parolaChiave",methods=["POST"])
def parolaChiave():
    parola=request.form.get("keyword")
    libri = db.ricercaParolaChiave(mysql,parola)
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
        message = 1 if db.insertLibro_Catalogo(mysql, titolo, isbn, genere, piano, scaffale, posizione, autori, riassunto) else 0
        return render_template("admin.html", message=message)
    return render_template("admin.html", message=3)

@app.route("/aggiungiRiassunto", methods=["POST"])
def aggiungi_riassunto():
    isbn = request.form.get("isbn")
    riassunto = request.form.get("riassunto")
    if db.aggiungi_riassunto(mysql, isbn, riassunto):
        return redirect(url_for("users"))
    return "Errore nell'aggiunta del riassunto", 400

@app.route("/registerAdmin",methods=["GET","POST"])
def registerAdmin():
    if request.method == "POST":
        print("sono qui")
        tessera = request.form.get("tessera")
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        data_nascita = request.form.get("datanascita")
        email = request.form.get("email")
        password = request.form.get("password")
        conf = request.form.get("confirm_password")

        if password == conf:
            if db.registrazione(mysql, tessera, nome, cognome, data_nascita, email, password,1):
                return redirect(url_for("log_in"))
    return render_template("registerAdmin.html")

@app.route("/prestiti",methods=["GET","POST"])
def presta():
    if request.method=="POST":
        isbn=request.form.get("isbn")
        tessera=request.form.get("tessera")
        data_inizio=request.form.get("datainizio")
        data_fine=request.form.get("datafine")
        db.presta(mysql,isbn,tessera,data_inizio,data_fine)
        libri=db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri, autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

    else:
        libri=db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri, autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

        

@app.route("/deposita", methods=["GET","POST"])
def deposita():
    if request.method=="POST":
        isbn=request.form.get("isbn")
        db.deposita(mysql,isbn)
        libri=db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri, autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

    else:
        libri=db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri, autori=db.getAutori(mysql), generi=db.getGeneri(mysql))


app.run(debug=True)