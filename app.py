from flask_mysqldb import MySQL
from flask import Flask, render_template, url_for
import requests
import db
app = Flask(__name__)



app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'iaia_basile'
mysql = MySQL(app)



@app.route("/")
def aggiungi_libro():    
    print(db.ordinamento(mysql,1))
    return render_template("index.html")


@app.route("/user")
def user():
    return render_template("users")





app.run(debug=True)
