from flask_mysqldb import MySQL
from flask import Flask, render_template, url_for

app = Flask(__name__)



app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'iaia_basile'
mysql = MySQL(app)



@app.route("/")
def aggiungi_libro():    
    titolo = "a"
    prezzo = 0
    isbn = "i"
    piano = "p"
    scaffale = "s"
    posizione = "p"
    cursor = mysql.connection.cursor()

    # Inserisci il libro nella tabella Libro
    queryLibro = "INSERT INTO Libro (isbn, titolo, prezzo) VALUES (%s, %s, %s)"
    cursor.execute(queryLibro, (isbn, titolo, prezzo))

    # Inserisci la locazione nella tabella Locazione
    queryLocazione = "INSERT INTO Locazione (piano, scaffale, posizione) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)"
    cursor.execute(queryLocazione, (piano, scaffale, posizione))

    # Recupera l'id della locazione appena inserita
    id_locazione = cursor.lastrowid

    # Inserisci i dati nel Catalogo
    queryCatalogo = "INSERT INTO Catalogo (isbn, id_locazione) VALUES (%s, %s)"
    cursor.execute(queryCatalogo, (isbn, id_locazione))
    
    # Completare la transazione
    mysql.connection.commit()
    
    print("Libro inserito con ISBN:", isbn)
    print("Locazione inserita con ID:", id_locazione)
    return render_template("index.html")


@app.route("/user")
def user():
    return render_template("users")





app.run(debug=True)
