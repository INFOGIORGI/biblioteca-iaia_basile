from flask_mysqldb import MySQL
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash
import re

def insertLibro_Catalogo(mysql, titolo, isbn, genere, piano, scaffale, posizione, autori, riassunto):
    cursor = mysql.connection.cursor()

    # Controlla se l'ISBN esiste già
    cursor.execute("SELECT isbn FROM Libro WHERE isbn = %s", (isbn,))
    if cursor.fetchone():#prende solo il primo set
        return "Errore: Il libro con ISBN esiste già."

    # Inserisci il libro nella tabella Libro
    cursor.execute("INSERT INTO Libro (isbn, titolo, genere, riassunto) VALUES (%s, %s, %s, %s)",
                   (isbn, titolo, genere, riassunto))
    
    # Recupera l'id della locazione o la crea se non esiste
    cursor.execute("SELECT id FROM Locazione WHERE piano = %s AND scaffale = %s AND posizione = %s",
                   (piano, scaffale, posizione))
    id_locazione = cursor.fetchone()
    if not id_locazione:
        cursor.execute("INSERT INTO Locazione (piano, scaffale, posizione) VALUES (%s, %s, %s)",
                       (piano, scaffale, posizione))
        id_locazione = cursor.lastrowid
    else:
        id_locazione = id_locazione[0]
    
    # Inserisci i dati nel Catalogo
    cursor.execute("INSERT INTO Catalogo (isbn, id_locazione) VALUES (%s, %s)", (isbn, id_locazione))
    
    # Inserisci gli autori nella tabella Libro_Autore
    for autore in autori.split(','):
        autore = autore.strip()
        nome_cognome = autore.split(maxsplit=1)  # Permette più nomi
        if len(nome_cognome) != 2:
            continue  # Ignora autori non validi
        nome, cognome = nome_cognome
        cursor.execute("SELECT id FROM Autore WHERE nome = %s AND cognome = %s", (nome, cognome))
        autore_id = cursor.fetchone()
        if not autore_id:#Se l'autore non esiste lo inserisci 
            cursor.execute("INSERT INTO Autore (nome, cognome) VALUES (%s, %s)", (nome, cognome))
            autore_id = cursor.lastrowid
        else:#lo referenzio se esiste
            autore_id = autore_id[0]
        cursor.execute("INSERT INTO Libro_Autore (id_libro, id_autore) VALUES (%s, %s)", (isbn, autore_id))
    
    mysql.connection.commit()
    return "Libro inserito con successo."

def ricercaParolaChiave(mysql, parola):
    cursor = mysql.connection.cursor()
    pattern = f"%{parola}%"
    query = "SELECT * FROM Libro WHERE titolo LIKE %s"
    cursor.execute(query, (pattern,))
    return cursor.fetchall()


def ordinamento(mysql, dato):
    cursor = mysql.connection.cursor()
    if dato == 0:
        query = "SELECT isbn, titolo FROM Libro ORDER BY titolo;"
    else:
        query = """
        SELECT l.isbn, l.titolo, a.nome, a.cognome
        FROM Libro l
        JOIN Libro_Autore la ON l.isbn = la.id_libro
        JOIN Autore a ON la.id_autore = a.id
        ORDER BY a.nome, a.cognome;
        """
    cursor.execute(query)
    return cursor.fetchall()

def filtraGenere(mysql, genere):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Libro WHERE genere = %s", (genere,))
    return cursor.fetchall()

def registrazione(mysql, tessera, nome, cognome, datanascita, email, password):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):#VERIFICA LA VALIDITA DELLA MAIL
        return False
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Utenti WHERE email = %s OR tesseraCliente = %s", (email, tessera))
    if cursor.fetchone():
        return False
    
    cursor.execute("INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password) VALUES (%s, %s, %s, %s, %s, %s)",
                   (tessera, nome, cognome, datanascita, email, generate_password_hash(password)))
    mysql.connection.commit()
    return True

def logIn(mysql, email, password):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password FROM Utenti WHERE email = %s", (email,))
    dati = cursor.fetchone()
    if dati and check_password_hash(dati[0], password):
        return False
    return True

def mostraRiassunto(mysql, isbn):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT riassunto FROM Libro WHERE isbn = %s", (isbn,))
    return cursor.fetchone()

def getAutori(mysql):
    cursor = mysql.connection.cursor()
    query = """
    SELECT a.id, a.nome, a.cognome, l.isbn
    FROM Autore a
    JOIN Libro_Autore la ON a.id = la.id_autore
    JOIN Libro l ON la.id_libro = l.isbn
    """
    cursor.execute(query)
    return cursor.fetchall()

def aggiungi_riassunto(mysql, isbn, riassunto):
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Libro SET riassunto = %s WHERE isbn = %s", (riassunto, isbn))
    mysql.connection.commit()
    return True

def getGeneri(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT genere FROM Libro")
    return cursor.fetchall()
