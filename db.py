from flask_mysqldb import MySQL
from flask import Flask
app=Flask(__name__)
app.config["MYSQL_HOST"]="138.41.20.102"
app.config["MYSQL_PORT"]=53306
app.config["MYSQL_USER"]="ospite"
app.config["MYSQL_PASSWORD"]="ospite"
app.config["MYSQL_DB"]="iaia_basile"

mysql=MySQL(app)
class DB:

    def __init__(self):
        cursor = mysql.connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS Autore (
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            nome VARCHAR(255) NOT NULL,
            cognome VARCHAR(255) NOT NULL,
            dataNascita DATE,
            dataMorte DATE
        );

        CREATE TABLE IF NOT EXISTS Libro (
            isbn VARCHAR(13) PRIMARY KEY,
            id_autore INT,
            titolo VARCHAR(255) NOT NULL,
            prezzo DECIMAL(10,2),
            locazione VARCHAR(255),
            FOREIGN KEY (id_autore) REFERENCES Autore(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Utenti (
            tesseraCliente VARCHAR(255) PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            cognome VARCHAR(255) NOT NULL,
            dataNascita DATE,
            dataMorte DATE
        );

        CREATE TABLE IF NOT EXISTS Prestiti (
            id_libro VARCHAR(13),
            id_utente VARCHAR(255),
            dataInizio DATE NOT NULL,
            dataFine DATE,
            PRIMARY KEY (id_libro, id_utente, dataInizio),
            FOREIGN KEY (id_libro) REFERENCES Libro(isbn) ON DELETE CASCADE,
            FOREIGN KEY (id_utente) REFERENCES Utenti(tesseraCliente) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Autori (
            id_autori INT NOT NULL AUTO_INCREMENT,
            id_libro VARCHAR(13) NOT NULL,
            id_autore INT NOT NULL,
            PRIMARY KEY(id_autori, id_libro),
            FOREIGN KEY (id_libro) REFERENCES Libro(isbn) ON DELETE CASCADE,
            FOREIGN KEY (id_autore) REFERENCES Autore(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS Catalogo (
            isbn VARCHAR(13) NOT NULL,
            isPrestato BOOLEAN DEFAULT 0, 
            PRIMARY KEY(isbn),
            FOREIGN KEY (isbn) REFERENCES Libro(isbn) ON DELETE CASCADE
        );"""  
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()




# @app.route("/")
# def crea_db():
