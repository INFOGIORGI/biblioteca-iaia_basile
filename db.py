from flask_mysqldb import MySQL
from flask import Flask


def insertLibrio_Catalogo(mysql,titolo,prezzo,isbn,piano,scaffale,posizione):
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
    
    mysql.connection.commit()
    print("Libro inserito con ISBN:", isbn)
    print("Locazione inserita con ID:", id_locazione)
    


def ricercaParolaChiave(mysql,parola,posizione):#0 inizio 1 nel mezzo 2 alla fine
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


def ordinamento(mysql,dato): #0 titolo #1 titolo
    cursor=mysql.connection.cursor()
    query=""
    if dato == 0:
        query="""SELECT l.isbn, l.titolo, l.prezzo, c.isPrestato
                FROM Catalogo AS c
                JOIN Libro AS l ON c.isbn = l.isbn
                ORDER BY l.titolo;"""
    else:
        query="""SELECT l.isbn, l.titolo, l.prezzo, a.nome AS autore, a.cognome
                FROM Catalogo AS c
                JOIN Libro AS l ON c.isbn = l.isbn
                JOIN Libro_Autore AS la ON l.isbn = la.id_libro
                JOIN Autore AS a ON la.id_autore = a.id
                ORDER BY a.nome, a.cognome;"""
    cursor.execute(query)
    dati=cursor.fetchall()
    print(dati)
    return dati

