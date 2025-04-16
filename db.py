# database.py
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import re

def insertLibro_Catalogo(mysql, titolo, isbn, genere, piano, scaffale, posizione, autori, riassunto):
    cursor = mysql.connection.cursor()

    # Verifica se l'ISBN esiste già
    cursor.execute("SELECT isbn FROM Libro WHERE isbn = %s", (isbn,))
    if cursor.fetchone():
        return "Errore: Il libro con ISBN esiste già."

    # Inserisci il libro nella tabella Libro
    cursor.execute("INSERT INTO Libro (isbn, titolo, genere, riassunto) VALUES (%s, %s, %s, %s)",
                   (isbn, titolo, genere, riassunto))
    
    # Recupera l'id della locazione o creala se non esiste
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
        nome_cognome = autore.split(maxsplit=1)  # Supporta più nomi
        if len(nome_cognome) != 2:
            continue
        nome, cognome = nome_cognome
        cursor.execute("SELECT id FROM Autore WHERE nome = %s AND cognome = %s", (nome, cognome))
        autore_id = cursor.fetchone()
        if not autore_id:
            cursor.execute("INSERT INTO Autore (nome, cognome) VALUES (%s, %s)", (nome, cognome))
            autore_id = cursor.lastrowid
        else:
            autore_id = autore_id[0]
        cursor.execute("INSERT INTO Libro_Autore (id_libro, id_autore) VALUES (%s, %s)", (isbn, autore_id))
    
    mysql.connection.commit()
    return "Libro inserito con successo."

def ricercaParolaChiave(mysql, parola):
    cursor = mysql.connection.cursor()
    pattern = f"%{parola}%"
    query = """
    SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato,
           loc.piano, loc.scaffale, loc.posizione, l.genere,
           a.nome, a.cognome
    FROM Libro l
    JOIN Catalogo c ON l.isbn = c.isbn
    JOIN Locazione loc ON c.id_locazione = loc.id
    JOIN Libro_Autore la ON l.isbn = la.id_libro
    JOIN Autore a ON la.id_autore = a.id
    WHERE l.titolo LIKE %s
    """
    cursor.execute(query, (pattern,))
    return cursor.fetchall()

def ordinamento(mysql, dato):
    cursor = mysql.connection.cursor()
    if dato == 0:
        query = """
        SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato,
               loc.piano, loc.scaffale, loc.posizione, l.genere
        FROM Libro l
        JOIN Catalogo c ON l.isbn = c.isbn
        JOIN Locazione loc ON c.id_locazione = loc.id
        ORDER BY titolo;
        """
    else:
        query = """
        SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato,
               loc.piano, loc.scaffale, loc.posizione, l.genere,
               GROUP_CONCAT(DISTINCT a.nome, ' ', a.cognome
                   ORDER BY a.cognome, a.nome SEPARATOR ', ') AS autori
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
    query = """
    SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato,
           loc.piano, loc.scaffale, loc.posizione, l.genere
    FROM Libro l
    JOIN Catalogo c ON l.isbn = c.isbn
    JOIN Locazione loc ON c.id_locazione = loc.id
    WHERE l.genere = %s
    """
    cursor.execute(query, (genere,))
    return cursor.fetchall()

def registrazione(mysql, tessera, nome, cognome, datanascita, email, password, user):
    # Verifica formato email
    if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        return False
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Utenti WHERE email = %s OR tesseraCliente = %s", (email, tessera))
    if cursor.fetchone():
        return False
    if user == 0:
        cursor.execute(
            "INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password) VALUES (%s, %s, %s, %s, %s, %s)",
            (tessera, nome, cognome, datanascita, email, generate_password_hash(password))
        )
    else:
        cursor.execute(
            "INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password, is_admin) VALUES (%s, %s, %s, %s, %s, %s, 1)",
            (tessera, nome, cognome, datanascita, email, generate_password_hash(password))
        )
    mysql.connection.commit()
    return True

def logIn(mysql, email, password):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Utenti WHERE email = %s", (email,))
    dati = cursor.fetchone()
    # Il formato dei dati: (tesseraCliente, nome, cognome, dataNascita, email, is_admin, password)
    if dati and dati[5] == 1 and check_password_hash(dati[6], password):
        return {'tesseraCliente': dati[0], 'email': dati[4], 'is_admin': 'admin'}
    if dati and check_password_hash(dati[6], password):
        return {'tesseraCliente': dati[0], 'email': dati[4], 'is_admin': 'user'}
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

def aggiungi_riassunto(mysql, isbn, tessera_utente, riassunto):
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Riassunti (isbn, tesseraCliente, riassunto) VALUES (%s, %s, %s)", 
                   (isbn, tessera_utente, riassunto))
    mysql.connection.commit()
    return True

def get_riassunti_by_isbn(mysql, isbn):
    cursor = mysql.connection.cursor()
    query = """
       SELECT U.nome, U.cognome, R.riassunto, R.dataInserimento
       FROM Riassunti R
       JOIN Utenti U ON R.tesseraCliente = U.tesseraCliente
       WHERE R.isbn = %s
       ORDER BY R.dataInserimento DESC;
    """
    cursor.execute(query, (isbn,))
    results = cursor.fetchall()
    return results



def getGeneri(mysql):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT DISTINCT genere FROM Libro")
    return cursor.fetchall()

def getLibri(mysql):
    cursor = mysql.connection.cursor()
    query = """
    SELECT l.isbn, l.titolo, l.riassunto, c.isPrestato,
           loc.piano, loc.scaffale, loc.posizione, l.genere
    FROM Libro l
    JOIN Catalogo c ON l.isbn = c.isbn
    JOIN Locazione loc ON c.id_locazione = loc.id
    """
    cursor.execute(query)
    return cursor.fetchall()

def presta(mysql, isbn, tessera_utente, data_inizio, data_fine):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, isPrestato FROM Catalogo WHERE isbn = %s", (isbn,))
    libro = cursor.fetchone()
    if libro[1] == 0:
        cursor.execute("SELECT * FROM Prestiti WHERE id_libro = %s AND id_utente = %s AND dataInizio = %s", 
                       (isbn, tessera_utente, data_inizio))
        if cursor.fetchone():
            print("Il libro è già in prestito per questo utente")
            return False
        else:
            n_prestiti = cursor.execute("SELECT n_prestiti FROM Prestiti WHERE id_libro = %s AND id_utente = %s",
                                         (isbn, tessera_utente))
            if n_prestiti:
                cursor.execute("UPDATE Prestiti SET n_prestiti = %s + 1 WHERE id_libro = %s AND id_utente = %s",
                               (n_prestiti, isbn, tessera_utente))
            else:
                cursor.execute("INSERT INTO Prestiti (id_libro, id_utente, dataInizio, dataFine) VALUES (%s, %s, %s, %s)",
                               (isbn, tessera_utente, data_inizio, data_fine))
            cursor.execute("UPDATE Catalogo SET isPrestato = 1 WHERE id = %s", (libro[0],))
    mysql.connection.commit()

def deposita(mysql, isbn):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, isPrestato FROM Catalogo WHERE isbn = %s", (isbn,))
    libro = cursor.fetchone()
    if libro and libro[1] == 1:
        cursor.execute("UPDATE Catalogo SET isPrestato = 0 WHERE isbn = %s", (isbn,))
    mysql.connection.commit()

def get_user_by_id(mysql, user_id):
    cursor = mysql.connection.cursor()
    query = "SELECT tesseraCliente, email, is_admin FROM Utenti WHERE tesseraCliente = %s"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    if row:
        # Se il campo is_admin è 1, interpretiamo l'utente come 'admin', altrimenti 'user'
        role = "admin" if row[2] == 1 else "user"
        return {
            'tesseraCliente': row[0],
            'email': row[1],
            'is_admin': role
        }
    return None

def get_prestiti_storico(mysql, tessera):
    cursor = mysql.connection.cursor()
    query = """
    SELECT l.titolo, p.dataInizio, p.dataFine, p.n_prestiti
    FROM Prestiti p
    JOIN Libro l ON p.id_libro = l.isbn
    WHERE p.id_utente = %s
    ORDER BY p.dataInizio DESC
    """
    cursor.execute(query, (tessera,))
    return cursor.fetchall()
