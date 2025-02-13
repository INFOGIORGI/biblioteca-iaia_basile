from flask_mysqldb import MySQL
from flask import Flask


app=Flask(__name__)

app.config['MYSQL_HOST'] = ''
app.config['MYSQL_PORT'] = ''
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'w3schools'
mysql = MySQL(app)

def insertLibrio_Catalogo(titolo,prezzo,isbn,piano,scaffale,posizione):
    cursor=mysql.connection.cursor()
    queryLibro="INSERT INTO Libro VALUES(%s,%s,%s)"
    cursor.execute(queryLibro,(isbn,titolo,prezzo))
    queryLocazione="INSERT INTO Locazione VALUES(%s,%s,%s)"
    cursor.execute(queryLocazione,(piano,scaffale,posizione))
    querySelectLocazione="SELECT id FROM Locazione where piano=%s AND scaffale=%s AND posizione=%s"
    cursor.execute(querySelectLocazione,())
    locazione=cursor.fatchall
    queryCatalogo="INSERT INTO Catalogo VALUES(%s,%s)"
    cursor.execute(queryCatalogo,(isbn,locazione))


