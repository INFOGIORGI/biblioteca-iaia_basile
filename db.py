# ATTENZIONE
# NON CANCELLARE LA PARTE DI SOTTO COMMENTATA LA PARTE DI SOTTO FUNZIONA PERCHE L HO SCRITTA IO A MANO, 
# QUESTA PARTE COMMENTATA L'HO FATTA COMMENTARE A COPAILOT CA VO DI PRESSA, COSI SE HAI BISOGNO LA CAPISCI
# ATTENZIONE

from flask_mysqldb import MySQL
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

# Funzione per inserire un libro nel catalogo
# Inserisce il libro nella tabella Libro, la sua locazione nella tabella Locazione e collega il tutto nella tabella Catalogo
def insertLibrio_Catalogo(mysql, titolo, isbn, genere, piano, scaffale, posizione, autori, riassunto):
    cursor = mysql.connection.cursor()

    # Controlla se l'ISBN esiste già
    queryCheck = "SELECT isbn FROM Libro WHERE isbn = %s"
    cursor.execute(queryCheck, (isbn,))
    if cursor.fetchone():
        print(f"Il libro con ISBN '{isbn}' esiste già.")
        return False
    
    # Inserisci il libro nella tabella Libro
    queryLibro = "INSERT INTO Libro (isbn, titolo, genere, riassunto) VALUES (%s, %s, %s, %s)"
    cursor.execute(queryLibro, (isbn, titolo, genere, riassunto))
    
    # Inserisci la locazione nella tabella Locazione, aggiornando l'id se già esistente
    queryLocazione = "INSERT INTO Locazione (piano, scaffale, posizione) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)"
    cursor.execute(queryLocazione, (piano, scaffale, posizione))
    
    # Recupera l'id della locazione appena inserita  
    id_locazione = cursor.lastrowid

    # Inserisci i dati nel Catalogo collegando il libro alla locazione
    queryCatalogo = "INSERT INTO Catalogo (isbn, id_locazione) VALUES (%s, %s)"
    cursor.execute(queryCatalogo, (isbn, id_locazione))
    
    # Inserisci gli autori nella tabella Libro_Autore
    for autore in autori.split(','):
        autore = autore.strip()
        nome_cognome = autore.split()
        if len(nome_cognome) != 2:
            print(f"Autore '{autore}' non valido. Inserisci sia nome che cognome.")
            continue
        nome, cognome = nome_cognome
        queryAutore = "SELECT id FROM Autore WHERE nome = %s AND cognome = %s"
        cursor.execute(queryAutore, (nome, cognome))
        autore_id = cursor.fetchone()
        if autore_id:
            autore_id = autore_id[0]
        else:
            queryInserisciAutore = "INSERT INTO Autore (nome, cognome) VALUES (%s, %s)"
            cursor.execute(queryInserisciAutore, (nome, cognome))
            autore_id = cursor.lastrowid
        
        queryLibroAutore = "INSERT INTO Libro_Autore (id_libro, id_autore) VALUES (%s, %s)"
        cursor.execute(queryLibroAutore, (isbn, autore_id))

    mysql.connection.commit()
    print("Libro inserito con ISBN:", isbn)
    print("Locazione inserita con ID:", id_locazione)
    return True



# Funzione per ricercare un libro nel catalogo in base a una parola chiave
# La posizione indica dove deve essere trovata la parola nel titolo (0: inizio, 1: ovunque, 2: fine)
def ricercaParolaChiave(mysql,parola,posizione):
    cursor=mysql.connection.cursor()
    query=""
    if posizione == 0:
        query=f"select * from Libro where titolo like '{parola}%'"
    elif posizione == 1:
        query=f"select * from Libro where titolo like '%{parola}%'"
    elif posizione == 2:
        query=f"select * from Libro where titolo like '%{parola}'"
    else:
        query=f"select * from Libro"
    cursor.execute(query)
    data=cursor.fetchall()
    # print(data)
    return data

# Funzione per ordinare i libri in base a un determinato parametro
# Se dato == 0 ordina per titolo, altrimenti ordina per nome e cognome dell'autore
def ordinamento(mysql,dato): 
    cursor=mysql.connection.cursor()
    query=""
    if dato == 0:
        query="""SELECT l.isbn, l.titolo, c.isPrestato
                FROM Catalogo AS c
                JOIN Libro AS l ON c.isbn = l.isbn
                ORDER BY l.titolo;"""
    else:
        query="""SELECT l.isbn, l.titolo, a.nome AS autore, a.cognome
                FROM Catalogo AS c
                JOIN Libro AS l ON c.isbn = l.isbn
                JOIN Libro_Autore AS la ON l.isbn = la.id_libro
                JOIN Autore AS a ON la.id_autore = a.id
                ORDER BY a.nome, a.cognome;"""
    cursor.execute(query)
    dati=cursor.fetchall()
    print(dati)
    return dati

# Funzione per filtrare i libri in base al genere
def filtraGenere(mysql,genere):
    cursor=mysql.connection.cursor()

    # Recupera il numero totale di libri
    query="select * from Libro"
    cursor.execute(query)
    LibriTotali=len(cursor.fetchall())
    
    # Recupera il numero di libri del genere specificato
    query="select * from Libro where genere=%s"
    cursor.execute(query,(genere,))
    dati=len(cursor.fetchall())
    print("libri del genere citato:" + dati + "libri totali: "+ LibriTotali)
    return[dati,LibriTotali]

# Funzione per registrare un nuovo utente
# Verifica che email e tessera non siano già registrate prima di inserire il nuovo utente
import re
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

def registrazione(mysql, tessera, nome, cognome, datanascita, email, password):
    # Verifica che l'email abbia un formato valido
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_regex.match(email):
        print("Formato email non valido")
        return False
    
    cursor = mysql.connection.cursor()
    
    # Controlla se l'email è già registrata
    querySelect = "SELECT email FROM Utenti WHERE email = %s"
    cursor.execute(querySelect, (email,))
    if cursor.fetchall():
        print("Utente già registrato")
        return False
    
    # Controlla se la tessera è già in uso
    querySelect = "SELECT tesseraCliente FROM Utenti WHERE tesseraCliente = %s"
    cursor.execute(querySelect, (tessera,))
    if cursor.fetchall():
        print("Tessera già in uso")
        return False
    
    # Inserisce il nuovo utente
    queryInsert = "INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(queryInsert, (tessera, nome, cognome, datanascita, email, generate_password_hash(password)))
    mysql.connection.commit()
    print("Inserimento avvenuto")
    return True


# Funzione per mostrare il riassunto di un libro dato il suo ISBN
def mostraRiassunto(mysql,isbn):
    cursor=mysql.connection.cursor()
    query="Select riassunto from Libro where isbn=%s"
    cursor.execute(query,(isbn,))
    riassunto=cursor.fetchall()
    print(riassunto)
    return riassunto

# Funzione per gestire il login degli utenti
def logIn(mysql,email,password):
    cursor=mysql.connection.cursor()
    query="select * from Utenti where email=%s"
    cursor.execute(query,(email,))
    dati=cursor.fetchall()
    
    if dati:
        # Controlla se la password fornita corrisponde all'hash salvato nel database
        if check_password_hash(dati[0][5],password):
            print("Sei loggato pero bisogna sviluppare la parte di area personale")
            return True
        else:
            print("email o password non validi")
            return False
    
    print("email non registrata")
    return False



def getAutori(mysql):
    cur = mysql.connection.cursor()
    query = """
    SELECT a.id, a.nome, a.cognome, l.isbn
    FROM Autore a
    JOIN Libro_Autore la ON a.id = la.id_autore
    JOIN Libro l ON la.id_libro = l.isbn
    """
    cur.execute(query)
    autori = cur.fetchall()
    cur.close()
    return autori


def aggiungi_riassunto(mysql, isbn, riassunto):
    cursor = mysql.connection.cursor()
    query = "UPDATE Libro SET riassunto = %s WHERE isbn = %s"
    cursor.execute(query, (riassunto, isbn))
    mysql.connection.commit()
    return True

def getGeneri(mysql):
    cursor = mysql.connection.cursor()
    query = "SELECT DISTINCT genere FROM Libro"
    cursor.execute(query)
    generi = cursor.fetchall()
    cursor.close()
    return generi

def filtraGenere(mysql, genere):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM Libro WHERE genere = %s"
    cursor.execute(query, (genere,))
    libri = cursor.fetchall()
    cursor.close()
    return libri
def ordinamento(mysql, dato): 
    cursor = mysql.connection.cursor()
    if dato == 0:
        query = """
        SELECT l.isbn, l.titolo, l.genere, l.riassunto
        FROM Libro AS l
        ORDER BY l.titolo;
        """
    else:
        query = """
        SELECT l.isbn, l.titolo, l.genere, l.riassunto, a.nome, a.cognome
        FROM Libro AS l
        JOIN Libro_Autore AS la ON l.isbn = la.id_libro
        JOIN Autore AS a ON la.id_autore = a.id
        ORDER BY a.nome, a.cognome;
        """
    cursor.execute(query)
    dati = cursor.fetchall()
    cursor.close()
    return dati

def ricercaParolaChiave(mysql, parola, posizione):
    cursor = mysql.connection.cursor()
    if posizione == 0:
        query = "SELECT * FROM Libro WHERE titolo LIKE %s"
        cursor.execute(query, (parola + '%',))
    elif posizione == 1:
        query = "SELECT * FROM Libro WHERE titolo LIKE %s"
        cursor.execute(query, ('%' + parola + '%',))
    elif posizione == 2:
        query = "SELECT * FROM Libro WHERE titolo LIKE %s"
        cursor.execute(query, ('%' + parola, ))
    else:
        query = "SELECT * FROM Libro"
        cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

