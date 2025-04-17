from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import db
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'Scemo_chi_legge(!)'


# Configurazione MySQL
app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = '5di'
app.config['MYSQL_PASSWORD'] = 'colazzo'
app.config['MYSQL_DB'] = 'iaia_basile'
mysql = MySQL(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "log_in"



class User(UserMixin):
    def __init__(self, tessera, email, role):
        self.id = tessera
        self.email = email
        self.role = role



@login_manager.user_loader
def load_user(user_id):
    user_data = db.get_user_by_id(mysql, user_id)
    if user_data:
        return User(user_data['tesseraCliente'], user_data['email'], user_data['is_admin'])
    return None



# Decoratore per verificare il ruolo (ora controlla current_user)
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != required_role:
                return "Accesso negato: non hai i permessi necessari per visualizzare questa pagina", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator



# ---------------------
# PAGINE Pubbliche
# ---------------------
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
            # Il parametro finale indica 0 per utente normale
            if db.registrazione(mysql, tessera, nome, cognome, data_nascita, email, password, 0):
                flash("Registrazione avvenuta con successo. Ora effettua il login.", "success")
                return redirect(url_for("log_in"))
            else:
                flash("Errore in registrazione. Email o tessera già in uso.", "danger")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user_data = db.logIn(mysql, email, password)
        print("DEBUG: user_data =", user_data)
        if user_data:
            # Crea un'istanza della classe User usando i dati restituiti
            user = User(user_data['tesseraCliente'], user_data['email'], user_data['is_admin'])
            # Chiama login_user per marcare l'utente come autenticato
            login_user(user)
            # Non serve salvare manualmente queste informazioni in sessione
            # Se vuoi comunque, puoi farlo, ma non è necessario per Flask-Login
            session['email'] = email
            session['role'] = user_data['is_admin']
            session['tesseraCliente'] = user_data['tesseraCliente']
            if user_data['is_admin'] == "admin":
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("users"))
        else:
            flash("Email o password errati. Riprova.", "danger")
    return render_template("login.html")






@app.route("/logout")
@login_required
def logout():
    print(generate_password_hash("user"))
    logout_user()
    flash("Logout effettuato.", "info")
    return redirect(url_for("home"))

# ---------------------
# Pagine per Utenti
# ---------------------
@app.route("/user", methods=["GET", "POST"])
def users():
    libri = db.getLibri(mysql)  # Supponiamo che restituisca una lista di tuple, dove l'indice 0 è l'ISBN
    # Costruisci un dizionario: chiave = ISBN, valore = lista di riassunti per quel libro
    riassunti_by_book = {}
    for libro in libri:
        isbn = libro[0]
        riassunti_by_book[isbn] = db.get_riassunti_by_isbn(mysql, isbn)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    return render_template("user.html", libri=libri, autori=autori, generi=generi, riassunti_by_book=riassunti_by_book)


@app.route("/parolaChiave", methods=["POST"])
@login_required
@role_required('user')
def parolaChiave():
    parola = request.form.get("keyword")
    libri = db.ricercaParolaChiave(mysql, parola)
    autori = db.getAutori(mysql)
    generi = db.getGeneri(mysql)
    riassunti_by_book = {}
    for libro in libri:
        isbn = libro[0]
        riassunti_by_book[isbn] = db.get_riassunti_by_isbn(mysql, isbn)
    return render_template("user.html", libri=libri, autori=autori, generi=generi,riassunti_by_book=riassunti_by_book)

@app.route("/ordinaPerAutore")
@login_required
@role_required('user')
def ordina_per_autore():
    libri=db.ordinamento(mysql, 1)
    riassunti_by_book = {}
    for libro in libri:
        isbn = libro[0]
        riassunti_by_book[isbn] = db.get_riassunti_by_isbn(mysql, isbn)
    return render_template("user.html", libri=libri,
                           autori=db.getAutori(mysql), generi=db.getGeneri(mysql),riassunti_by_book=riassunti_by_book)

@app.route("/ordinaPerTitolo")
@login_required
@role_required('user')
def ordina_per_titolo():
    libri=db.ordinamento(mysql, 0)
    riassunti_by_book = {}
    for libro in libri:
        isbn = libro[0]
        riassunti_by_book[isbn] = db.get_riassunti_by_isbn(mysql, isbn)
    return render_template("user.html", libri=libri,
                           autori=db.getAutori(mysql), generi=db.getGeneri(mysql),riassunti_by_book=riassunti_by_book)

@app.route("/filtraGenere", methods=["POST"])
@login_required
@role_required('user')
def filtra_genere():
    genere = request.form.get("genere")
    libri=db.filtraGenere(mysql, genere)
    riassunti_by_book = {}
    for libro in libri:
        isbn = libro[0]
        riassunti_by_book[isbn] = db.get_riassunti_by_isbn(mysql, isbn)
    return render_template("user.html", libri=libri,
                           autori=db.getAutori(mysql), generi=db.getGeneri(mysql),riassunti_by_book=riassunti_by_book)




# ---------------------
# Pagine per Admin
# ---------------------
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
            # Il parametro finale indica 1 per admin
            if db.registrazione(mysql, tessera, nome, cognome, data_nascita, email, password, 1):
                flash("Admin registrato con successo!", "success")
                return redirect(url_for("log_in"))
            else:
                flash("Errore in registrazione admin.", "danger")
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
        message = 1 if db.insertLibro_Catalogo(mysql, titolo, isbn, genere, piano, scaffale, posizione, autori) else 0
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




# ---------------------
# Funzionalità aggiuntive
# ---------------------
# Route per consentire a ciascun utente di lasciare un riassunto per un libro
from flask import flash  # Assicurati di aver importato flash

@app.route("/aggiungi_riassunto", methods=["POST"])
@login_required
def aggiungi_riassunto():
    isbn = request.form.get("isbn")
    riassunto = request.form.get("riassunto")
    # Supponendo che al login salvassi la tessera utente in session, ad esempio:
    tessera = session.get('tesseraCliente')
    if db.aggiungi_riassunto(mysql, isbn, current_user.id, riassunto):
        flash("Riassunto aggiunto con successo.", "success")
    else:
        flash("Errore nell'aggiunta del riassunto.", "danger")
    return redirect(url_for("users"))

@app.route("/mostraRiassunti")
@login_required
def mostra_riassunti():
    # Richiama la funzione per ottenere tutti i riassunti
    riassunti = db.get_all_riassunti(mysql)
    return render_template("mostra_riassunti.html", riassunti=riassunti)


# Route per visualizzare lo storico dei prestiti dell'utente corrente
@app.route("/storicoPrestiti")
@login_required
@role_required('user')
def storico_prestiti():
    # Recupera lo storico dei prestiti per l'utente (current_user.id)
    prestiti = db.get_prestiti_storico(mysql, current_user.id)
    return render_template("storico_prestiti.html", prestiti=prestiti)

if __name__ == '__main__':
    app.run(debug=True)
