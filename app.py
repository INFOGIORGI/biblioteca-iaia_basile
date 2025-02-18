from flask_mysqldb import MySQL
from flask import Flask, render_template, url_for,request
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
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/user", methods=["GET","POST"])
def users():
    if request.method=="GET":
        libri=db.ricercaParolaChiave(mysql,"",0)
        return render_template("user.html",libri=libri)
   

@app.route("/admin", methods=["GET","POST"])
def admin():
    if request.method=="GET":
        return render_template("admin.html",message=0)
    else:
        titolo=request.form.get("titolo")
        isbn=request.form.get("isbn")
        genere=request.form.get("genere")
        piano=request.form.get("piano")
        scaffale=request.form.get("scaffale")
        posizione=request.form.get("posizione")
        if(db.insertLibrio_Catalogo(mysql,titolo,isbn,genere,piano,scaffale,posizione)):
            return render_template("admin.html",message=1)
        else:
            return render_template("admin.html",message=0)
app.run(debug=True)
