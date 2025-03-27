from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import db

app = Flask(__name__)
app.secret_key = 'Scemo_chi_legge(!)'  # Necessaria per firmare i cookie di sessione

# Configurazione MySQL
app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = '5di'
app.config['MYSQL_PASSWORD'] = 'colazzo'
app.config['MYSQL_DB'] = 'iaia_basile'
mysql = MySQL(app)

# CHAT GPT MA NON HO CAPITO COME FUNZIONE 
#DOVREBBE ESSERCI UNA FUNZIONE PREESISTENTE CHE PERMETTE DI RICONOSCERE SE SI E' LOGGATI E CHE RUOLO SI RICOPRE
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'role' not in session:
            return redirect(url_for('log_in'))
        return f(*args, **kwargs)
    return decorated_function

# Decoratore per verificare il ruolo
def role_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('role') != required_role:
                return "Accesso negato: non hai i permessi necessari per visualizzare questa pagina", 403
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

# PAGINE pubbliche
@app.route("/")
def home():
    return render_template("index.html")

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
            # Qui il parametro finale indica 0 per utente normale
            if db.registrazione(mysql, tessera, nome, cognome, data_nascita, email, password, 0):
                return redirect(url_for("log_in"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        # La funzione logIn restituisce una stringa con il ruolo: "admin" oppure "user"
        value = db.logIn(mysql, email, password)
        print(value)
        if value == "admin" or value == "user":
            # Salviamo nella sessione il ruolo (e altre info, se necessario)
            session['email'] = email
            session['role'] = value
            print(f"{value} loggato")
            # Reindirizza in base al ruolo
            if value == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("users"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# Pagine per utenti 
@app.route("/user", methods=["GET", "POST"])
@login_required
@role_required('user')
def users():
    libri = db.getLibri(mysql)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)

@app.route("/parolaChiave", methods=["POST"])
@login_required
@role_required('user')
def parolaChiave():
    parola = request.form.get("keyword")
    libri = db.ricercaParolaChiave(mysql, parola)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi)    

@app.route("/ordinaPerAutore")
@login_required
@role_required('user')
def ordina_per_autore():
    return render_template("user.html", libri=db.ordinamento(mysql, 1),
                           autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

@app.route("/ordinaPerTitolo")
@login_required
@role_required('user')
def ordina_per_titolo():
    return render_template("user.html", libri=db.ordinamento(mysql, 0),
                           autori=db.getAutori(mysql), generi=db.getGeneri(mysql))

@app.route("/filtraGenere", methods=["POST"])
@login_required
@role_required('user')
def filtra_genere():
    genere = request.form.get("genere")
    return render_template("user.html", libri=db.filtraGenere(mysql, genere),
                           autori=db.getAutori(mysql), generi=db.getGeneri(mysql))



# Pagine per gli admin 

@app.route("/registerAdmin", methods=["GET", "POST"])
@login_required
@role_required('admin')
def registerAdmin():
    if request.method == "POST":
        tessera = request.form.get("tessera")
        nome = request.form.get("nome")
        cognome = request.form.get("cognome")
        data_nascita = request.form.get("datanascita")
        email = request.form.get("email")
        password = request.form.get("password")
        conf = request.form.get("confirm_password")

        if password == conf:
            # Qui il parametro finale indica 1 per admin
            if db.registrazione(mysql, tessera, nome, cognome, data_nascita, email, password, 1):
                return redirect(url_for("log_in"))
    return render_template("registerAdmin.html")



@app.route("/admin", methods=["GET", "POST"])
@login_required
@role_required('admin')
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


@app.route("/deposita", methods=["GET", "POST"])
@login_required
@role_required('admin')
def deposita():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        db.deposita(mysql, isbn)
        libri = db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri,
                               autori=db.getAutori(mysql), generi=db.getGeneri(mysql))
    else:
        libri = db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri,
                               autori=db.getAutori(mysql), generi=db.getGeneri(mysql))
    
@app.route("/prestiti", methods=["GET", "POST"])
@login_required
@role_required('admin')
def presta():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        tessera = request.form.get("tessera")
        data_inizio = request.form.get("datainizio")
        data_fine = request.form.get("datafine")
        db.presta(mysql, isbn, tessera, data_inizio, data_fine)
        libri = db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri,
                               autori=db.getAutori(mysql), generi=db.getGeneri(mysql))
    else:
        libri = db.getLibri(mysql)
        return render_template("prestiti.html", libri=libri,
                               autori=db.getAutori(mysql), generi=db.getGeneri(mysql))




@app.route("/aggiungiRiassunto", methods=["POST"])
def aggiungi_riassunto():
    isbn = request.form.get("isbn")
    riassunto = request.form.get("riassunto")
    if db.aggiungi_riassunto(mysql, isbn, riassunto):
        return redirect(url_for("users"))
    return "Errore nell'aggiunta del riassunto", 400





if __name__ == '__main__':
    app.run(debug=True)




