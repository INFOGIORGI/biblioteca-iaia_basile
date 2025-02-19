from flask_mysqldb import MySQL
from flask import Flask, render_template, url_for, request, redirect
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

@app.route("/login")
def log_in():
    if request.method=="GET":
        return render_template("login.html")
    else:
        emali=request.form.get("email")
        password=request.form.get("password")
        db.logIn(mysql,emali,password)

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template("register.html")
    else:
        tessera=request.form.get("tessera")
        nome=request.form.get("nome")
        cognome=request.form.get("cognome")
        data_nascita=request.form.get("datanascita")
        email=request.form.get("tessera")
        password=request.form.get("password")
        conf=request.form.get("confirm_password")

        if password==conf:
            db.registrazione(mysql,tessera,nome,cognome,data_nascita,email,password)
            return render_template("login.html")
        else:
            render_template("register.html")
@app.route("/user", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        keyword = request.form.get("keyword")
        libri = db.ricercaParolaChiave(mysql, keyword, 1)
    else:
        libri = db.ricercaParolaChiave(mysql, "", 0)
    
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)

@app.route("/ordinaPerAutore")
def ordina_per_autore():
    libri = db.ordinamento(mysql, 1)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)

@app.route("/ordinaPerTitolo")
def ordina_per_titolo():
    libri = db.ordinamento(mysql, 0)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)

@app.route("/filtraGenere", methods=["POST"])
def filtra_genere():
    genere = request.form.get("genere")
    libri = db.filtraGenere(mysql, genere)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "GET":
        return render_template("admin.html", message=3)
    else:
        titolo = request.form.get("titolo")
        isbn = request.form.get("isbn")
        genere = request.form.get("genere")
        piano = request.form.get("piano")
        scaffale = request.form.get("scaffale")
        posizione = request.form.get("posizione")
        autori = request.form.get("autori")
        riassunto = request.form.get("riassunto")
        
        if db.insertLibrio_Catalogo(mysql, titolo, isbn, genere, piano, scaffale, posizione, autori, riassunto):
            return render_template("admin.html", message=1)
        else:
            return render_template("admin.html", message=0)

@app.route("/aggiungiRiassunto", methods=["POST"])
def aggiungi_riassunto():
    isbn = request.form.get("isbn")
    riassunto = request.form.get("riassunto")
    if db.aggiungi_riassunto(mysql, isbn, riassunto):
        return redirect(url_for("users"))
    else:
        return "Errore nell'aggiunta del riassunto", 400

app.run(debug=True)
