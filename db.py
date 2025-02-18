# ATTENZIONE
# NON CANCELLARE LA PARTE DI SOTTO COMMENTATA LA PARTE DI SOTTO FUNZIONA PERCHE L HO SCRITTA IO A MANO, 
# QUESTA PARTE COMMENTATA L'HO FATTA COMMENTARE A COPAILOT CA VO DI PRESSA, COSI SE HAI BISOGNO LA CAPISCI
# ATTENZIONE

from flask_mysqldb import MySQL
from flask import Flask
from werkzeug.security import generate_password_hash, check_password_hash

# Funzione per inserire un libro nel catalogo
# Inserisce il libro nella tabella Libro, la sua locazione nella tabella Locazione e collega il tutto nella tabella Catalogo
def insertLibrio_Catalogo(mysql,titolo,isbn,genere,piano,scaffale,posizione):
    cursor = mysql.connection.cursor()
   
    querySelect="SELECT * FROM Libro Where isbn=%s"
    cursor.execute(querySelect,(isbn,))
    if cursor.fetchall():
        querySelect="SELECT id FROM Locazione Where piano=%s AND scaffale=%s AND posizione=%s"
        cursor.execute(querySelect,(piano,scaffale,posizione))
        id_locazione=cursor.fetchall()
        print(id_locazione)
        if id_locazione:  
            print("id_locazione")  
            querySelect="SELECT * FROM Catalogo where id_locazione=%s"
            cursor.execute(querySelect,(id_locazione,))

            if(cursor.fetchall()):
                print("Libro gia inserito")
                return False
            else:
                # Inserisci la locazione nella tabella Locazione, aggiornando l'id se già esistente
                queryLocazione = "INSERT INTO Locazione (piano, scaffale, posizione) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)"
                cursor.execute(queryLocazione, (piano, scaffale, posizione))
                
                # Recupera l'id della locazione appena inserita  
                id_locazione = cursor.lastrowid

                # Inserisci i dati nel Catalogo collegando il libro alla locazione
                queryCatalogo = "INSERT INTO Catalogo (isbn, id_locazione) VALUES (%s, %s)"
                cursor.execute(queryCatalogo, (isbn, id_locazione))
                print("Libro esistente inserito nel catalogo")
                return True
    # Inserisci il libro nella tabella Libro
    queryLibro = "INSERT INTO Libro (isbn, titolo,genere) VALUES (%s, %s,%s)"
    cursor.execute(queryLibro, (isbn, titolo,genere))
    
    # Inserisci la locazione nella tabella Locazione, aggiornando l'id se già esistente
    queryLocazione = "INSERT INTO Locazione (piano, scaffale, posizione) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)"
    cursor.execute(queryLocazione, (piano, scaffale, posizione))
    
    # Recupera l'id della locazione appena inserita  
    id_locazione = cursor.lastrowid

    # Inserisci i dati nel Catalogo collegando il libro alla locazione
    queryCatalogo = "INSERT INTO Catalogo (isbn, id_locazione) VALUES (%s, %s)"
    cursor.execute(queryCatalogo, (isbn, id_locazione))
    
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
    print(data)
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
def registrazione(mysql,tessera,nome,cognome,datanascita,email,password):
    cursor=mysql.connection.cursor()
    
    # Controlla se l'email è già registrata
    querySelect="SELECT email FROM Utenti where email=%s"
    cursor.execute(querySelect,(email,))
    if cursor.fetchall():
        print("Utente gia registrato")
        return False
    
    # Controlla se la tessera è già in uso
    querySelect="SELECT tesseraCliente FROM Utenti where tesseraCliente=%s"
    cursor.execute(querySelect,(tessera,))
    if cursor.fetchall():
        print("Tessera gia in uso")
        return False
    
    # Inserisce il nuovo utente
    queryInsert="INSERT INTO Utenti VALUES(%s,%s,%s,%s,%s,%s)"
    cursor.execute(queryInsert,(tessera,nome,cognome,datanascita,email,generate_password_hash(password)))
    cursor.connection.commit()
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




# from flask_mysqldb import MySQL
# from flask import Flask
# from werkzeug.security import generate_password_hash, check_password_hash


# def insertLibrio_Catalogo(mysql,titolo,prezzo,isbn,piano,scaffale,posizione):
#     cursor = mysql.connection.cursor()
   
#     # Inserisci il libro nella tabella Libro
#     queryLibro = "INSERT INTO Libro (isbn, titolo, prezzo) VALUES (%s, %s, %s)"
#     cursor.execute(queryLibro, (isbn, titolo, prezzo))
    
#     # Inserisci la locazione nella tabella Locazione
#     queryLocazione = "INSERT INTO Locazione (piano, scaffale, posizione) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)"
#     cursor.execute(queryLocazione, (piano, scaffale, posizione))
    
#     # Recupera l'id della locazione appena inserita  
#     id_locazione = cursor.lastrowid

#     # Inserisci i dati nel Catalogo
#     queryCatalogo = "INSERT INTO Catalogo (isbn, id_locazione) VALUES (%s, %s)"
#     cursor.execute(queryCatalogo, (isbn, id_locazione))
    
#     mysql.connection.commit()
#     print("Libro inserito con ISBN:", isbn)
#     print("Locazione inserita con ID:", id_locazione)
    


# def ricercaParolaChiave(mysql,parola,posizione):# posizione: 0 inizio 1 nel mezzo 2 alla fine
#     cursor=mysql.connection.cursor()
#     query=""
#     if posizione == 0:
#         query=f"select * from Libro where titolo like '{parola}%'"
#     elif posizione == 1:
#         query=f"select * from Libro where titolo like '%{parola}%'"
#     elif posizione == 2:
#         query=f"select * from Libro where titolo like '%{parola}'"
#     else:
#         query=f"select * from Libro"
#     cursor.execute(query)
#     data=cursor.fetchall()
#     print(data)
#     return data


# def ordinamento(mysql,dato): #dato è il paramentro per cui stiamo ordinando  0 titolo #1 titolo
#     cursor=mysql.connection.cursor()
#     query=""
#     if dato == 0:
#         query="""SELECT l.isbn, l.titolo, l.prezzo, c.isPrestato
#                 FROM Catalogo AS c
#                 JOIN Libro AS l ON c.isbn = l.isbn
#                 ORDER BY l.titolo;"""
#     else:
#         query="""SELECT l.isbn, l.titolo, l.prezzo, a.nome AS autore, a.cognome
#                 FROM Catalogo AS c
#                 JOIN Libro AS l ON c.isbn = l.isbn
#                 JOIN Libro_Autore AS la ON l.isbn = la.id_libro
#                 JOIN Autore AS a ON la.id_autore = a.id
#                 ORDER BY a.nome, a.cognome;"""
#     cursor.execute(query)
#     dati=cursor.fetchall()
#     print(dati)
#     return dati

# def filtraGenere(mysql,genere):
#     cursor=mysql.connection.cursor()

#     query="select * from Libro"
#     cursor.execute(query)
    
#     # Calcolo statistiche sul nuemro di libri cercati nel genere
#     LibriTotali=len(cursor.fetchall())
#     query="select * from Libro where genere=%s"
#     cursor.execute(query,(genere,))
#     dati=len(cursor.fetchall())
#     print("libri del genere citato:" + dati + "libri totali: "+ LibriTotali)
#     return[dati,LibriTotali]



# def registrazione(mysql,tessera,nome,cognome,datanascita,email,password):
#     cursor=mysql.connection.cursor()
#     querySelect="SELECT email FROM Utenti where email=%s"
#     cursor.execute(querySelect,(email,))
#     if cursor.fetchall():
#         print("Utente gia registrato")
#         return False
#     querySelect="SELECT tesseraCliente FROM Utenti where tesseraCliente=%s"
#     cursor.execute(querySelect,(tessera,))
#     if cursor.fetchall():
#         print("Tessera gia in uso")
#         return False
#     queryInsert="INSERT INTO Utenti VALUES(%s,%s,%s,%s,%s,%s)"
#     cursor.execute(queryInsert,(tessera,nome,cognome,datanascita,email,generate_password_hash(password)))
#     cursor.connection.commit()
#     print("Inserimento avvenuto")
#     return True

# def mostraRiassunto(mysql,isbn):
#     cursor=mysql.connection.cursor()
#     query="Select riassunto from Libro where isbn=%s"
#     cursor.execute(query,(isbn,))
#     riassunto=cursor.fetchall()
#     print(riassunto)
#     return riassunto

# def logIn(mysql,email,password):
#     cursor=mysql.connection.cursor()
#     query="select * from Utenti where email=%s"
#     cursor.execute(query,(email,))
#     dati=cursor.fetchall()
#     if dati:
#         if check_password_hash(dati[0][5],password):
#             print("Sei loggato pero bisogna sviluppare la parte di area personale")
#             return True
#         else:
#             print("email o password non validi")
#             return False
#     print("email non registrata")
#     return False
    