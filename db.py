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
        id_locazione = cursor.lastrowid #prende l ultimo valore che inserisce
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
    query = """SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato, loc.piano, loc.scaffale, loc.posizione, l.genere, a.nome, a.cognome
                FROM Libro l
                JOIN Catalogo c ON l.isbn = c.isbn
                JOIN Locazione loc ON c.id_locazione = loc.id
                JOIN Libro_Autore la ON l.isbn = la.id_libro
                JOIN Autore a ON la.id_autore = a.id 
                WHERE l.titolo LIKE %s"""
    cursor.execute(query, (pattern,))
    return cursor.fetchall()


def ordinamento(mysql, dato):
    cursor = mysql.connection.cursor()
    if dato == 0:
        query = """SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato, loc.piano, loc.scaffale, loc.posizione, l.genere
                FROM Libro l
                JOIN Catalogo c ON l.isbn = c.isbn
                JOIN Locazione loc ON c.id_locazione = loc.id 
                ORDER BY titolo;"""
    else:
        #GROUP_CONTACT RAGGRUPPA IN UN UNICA STRINGA TUTTI I NOMI DEGLI AUTORI DI UN LIBRO
        #GROUPBY RAGGRUPPO I RISULTATI ESCLUDENDO GLI AUTORI PER EVITARE RIPETIZIONI
        query = """
                        SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato, 
                        loc.piano, loc.scaffale, loc.posizione, l.genere,
                        GROUP_CONCAT(DISTINCT a.nome, ' ', a.cognome ORDER BY a.cognome, a.nome SEPARATOR ', ') AS autori 
                        FROM Libro l
                        JOIN Catalogo c ON l.isbn = c.isbn
                        JOIN Locazione loc ON c.id_locazione = loc.id
                        JOIN Libro_Autore la ON l.isbn = la.id_libro
                        JOIN Autore a ON la.id_autore = a.id 
                        GROUP BY l.isbn, l.titolo, l.riassunto, c.isPrestato, 
                        loc.piano, loc.scaffale, loc.posizione, l.genere
                        ORDER BY MIN(a.cognome), MIN(a.nome);
        """
    cursor.execute(query)
    return cursor.fetchall()

def filtraGenere(mysql, genere):
    cursor = mysql.connection.cursor()
    cursor.execute("""      SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato, loc.piano, loc.scaffale, loc.posizione, l.genere
                            FROM Libro l
                            JOIN Catalogo c ON l.isbn = c.isbn
                            JOIN Locazione loc ON c.id_locazione = loc.id  
                            WHERE genere = %s""", (genere,))
    return cursor.fetchall()

def registrazione(mysql, tessera, nome, cognome, datanascita, email, password,user):
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):#VERIFICA LA VALIDITA DELLA MAIL
        return False
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Utenti WHERE email = %s OR tesseraCliente = %s", (email, tessera))
    if cursor.fetchone():
        return False
    if user==0:
        # user
        cursor.execute("INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password) VALUES (%s, %s, %s, %s, %s, %s)",
                    (tessera, nome, cognome, datanascita, email, generate_password_hash(password)))
    else:
        # admin
        cursor.execute("INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password,is_admin) VALUES (%s, %s, %s, %s, %s, %s,1)",
                    (tessera, nome, cognome, datanascita, email, generate_password_hash(password)))
    mysql.connection.commit()
    return True

def logIn(mysql, email, password):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Utenti WHERE email = %s", (email,))
    dati = cursor.fetchone()

    
    if dati and  dati[5]==1 and check_password_hash(dati[6], password):
            return "admin"
    if dati and check_password_hash(dati[6], password):
        
        return "user"
    return False

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

def getLibri(mysql):
    cursor = mysql.connection.cursor()
    
    query = """
    SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato, loc.piano, loc.scaffale, loc.posizione, l.genere
    FROM Libro l
    JOIN Catalogo c ON l.isbn = c.isbn
    JOIN Locazione loc ON c.id_locazione = loc.id
    """
    cursor.execute(query)
    return cursor.fetchall()

def presta(mysql,isbn,tessea_utente,data_inizio,data_fine):
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT id,isPrestato FROM Catalogo where isbn=%s",(isbn,))
    libro=cursor.fetchone()
    if libro[1]==0:
        cursor.execute("SELECT * FROM Prestiti where id_libro=%s and id_utente=%s and dataInizio=%s",(isbn,tessea_utente,data_inizio))
        if cursor.fetchone():
            print("libro gia in prestito dall'utente")
            return False
        else:
            n_prestiti=cursor.execute("SELECT n_prestiti FROM Prestiti where id_libro=%s and id_utente=%s" ,(isbn,tessea_utente))
            if n_prestiti:
                cursor.execute("UPDATE Prestiti SET n_prestiti = %s + 1 WHERE id_libro = %s AND id_utente = %s;", (n_prestiti,isbn,tessea_utente))
            else:
                cursor.execute("INSERT INTO Prestiti (id_libro,id_utente,dataInizio,dataFine) VALUE(%s,%s,%s,%s)", (isbn,tessea_utente,data_inizio,data_fine))
            
            cursor.execute("UPDATE Catalogo set isPrestato=1 where id=%s",(libro[0],))
    
    mysql.connection.commit()

    
def deposita(mysql,isbn):
    cursor=mysql.connection.cursor()
    cursor.execute("SELECT id,isPrestato FROM Catalogo where isbn=%s",(isbn,))
    libro=cursor.fetchone()
    if libro and libro[1]==1:
        cursor.execute("UPDATE Catalogo SET isPrestato=0 WHERE isbn=%s",(isbn,))
    mysql.connection.commit()
