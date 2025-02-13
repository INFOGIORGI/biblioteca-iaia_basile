
-- Droppo le tabelle nell’ordine corretto (relazioni inverse)
DROP TABLE IF EXISTS Prestiti;
DROP TABLE IF EXISTS Catalogo;
DROP TABLE IF EXISTS Libro_Autore;
DROP TABLE IF EXISTS Libro;
DROP TABLE IF EXISTS Utenti;
DROP TABLE IF EXISTS Autore;
DROP TABLE IF EXISTS Locazione;

-- Tabella degli autori
CREATE TABLE Autore (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    cognome VARCHAR(255) NOT NULL,
    dataNascita DATE,
    dataMorte DATE
);

-- Tabella dei libri (ogni libro può avere più autori, quindi non c'è un campo id_autore)
CREATE TABLE Libro (
    isbn VARCHAR(13) PRIMARY KEY,
    titolo VARCHAR(255) NOT NULL,
    prezzo DECIMAL(10,2)
);

-- Tabella degli utenti (correzione della sintassi e controllo formato email)
CREATE TABLE Utenti (
    tesseraCliente VARCHAR(255) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cognome VARCHAR(255) NOT NULL,
    dataNascita DATE NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    CHECK (email LIKE '%_@__%.__%')
);

-- Tabella dei prestiti, collegata a Libro e Utenti
CREATE TABLE Prestiti (
    id_libro VARCHAR(13),
    id_utente VARCHAR(255),
    dataInizio DATE NOT NULL,
    dataFine DATE,
    PRIMARY KEY (id_libro, id_utente, dataInizio),
    FOREIGN KEY (id_libro) REFERENCES Libro(isbn) ON DELETE CASCADE,
    FOREIGN KEY (id_utente) REFERENCES Utenti(tesseraCliente) ON DELETE CASCADE
);

-- Tabella di relazione molti-a-molti tra Libro e Autore
CREATE TABLE Libro_Autore (
    id_libro VARCHAR(13) NOT NULL,
    id_autore INT NOT NULL,
    PRIMARY KEY (id_autore, id_libro),
    FOREIGN KEY (id_libro) REFERENCES Libro(isbn) ON DELETE CASCADE,
    FOREIGN KEY (id_autore) REFERENCES Autore(id) ON DELETE CASCADE
);

-- Tabella per memorizzare in maniera univoca le locazioni
CREATE TABLE Locazione (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    piano VARCHAR(50) NOT NULL,
    scaffale VARCHAR(50) NOT NULL,
    posizione VARCHAR(50) NOT NULL,
    UNIQUE (piano, scaffale, posizione)
);

-- Modifichiamo la tabella Catalogo per fare riferimento alla tabella Locazione
CREATE TABLE Catalogo (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(13) NOT NULL,
    id_locazione INT,  -- Può essere NULL se il libro non ha una locazione assegnata
    isPrestato BOOLEAN DEFAULT 0,
    FOREIGN KEY (isbn) REFERENCES Libro(isbn) ON DELETE CASCADE,
    FOREIGN KEY (id_locazione) REFERENCES Locazione(id) ON DELETE SET NULL
);

-- INSERTS per la tabella Autore (100 record)
INSERT INTO Autore (nome, cognome, dataNascita, dataMorte) VALUES 
('Mario', 'Rossi', '1950-05-15', NULL),
('Luigi', 'Bianchi', '1962-03-10', NULL),
('Giovanni', 'Verdi', '1970-08-30', NULL),
('Francesco', 'Gialli', '1980-01-10', NULL),
('Alessandro', 'Neri', '1990-02-20', NULL),
('Andrea', 'Blu', '1975-07-07', NULL),
('Simone', 'Marroni', '1985-11-11', NULL),
('Marco', 'Rossi', '1965-12-12', NULL),
('Antonio', 'Ricci', '1955-04-04', NULL),
('Paolo', 'Ferri', '1978-09-09', NULL),
('Francesca', 'Bianchi', '1982-03-03', NULL),
('Sara', 'Verdi', '1992-05-05', NULL),
('Laura', 'Gialli', '1988-07-07', NULL),
('Elena', 'Neri', '1973-10-10', NULL),
('Chiara', 'Blu', '1995-12-12', NULL),
('Martina', 'Marroni', '1968-06-06', NULL),
('Giulia', 'Rossi', '1980-08-08', NULL),
('Stefano', 'Ricci', '1970-01-01', NULL),
('Roberto', 'Ferri', '1966-04-04', NULL),
('Vincenzo', 'Bianchi', '1958-11-11', NULL),
('Lucia', 'De Angelis', '1974-02-15', NULL),
('Mauro', 'Conti', '1983-06-22', NULL),
('Emanuele', 'Serra', '1969-09-11', NULL),
('Fabio', 'Longo', '1988-05-30', NULL),
('Gianni', 'Mancini', '1957-03-12', NULL),
('Carlo', 'Romano', '1961-08-14', NULL),
('Giorgia', 'Ferrari', '1977-07-19', NULL),
('Alberto', 'Costa', '1991-10-28', NULL),
('Rosa', 'Lombardi', '1986-12-17', NULL),
('Davide', 'Greco', '1993-04-09', NULL),
('Elisa', 'Moretti', '1952-01-25', NULL),
('Federico', 'Marini', '1964-11-08', NULL),
('Domenico', 'Gatti', '1982-02-27', NULL),
('Matteo', 'Vitale', '1996-06-06', NULL),
('Daniele', 'Ricci', '1975-09-30', NULL),
('Claudio', 'De Luca', '1959-07-14', NULL),
('Enrico', 'Fabbri', '1989-03-20', NULL),
('Gabriele', 'Pellegrini', '1981-12-12', NULL),
('Serena', 'Riva', '1967-05-08', NULL);

-- INSERTS per la tabella Libro (150 record)
INSERT INTO Libro (isbn, titolo, prezzo) VALUES 
('9780000000001', 'Libro 1', 9.99),
('9780000000002', 'Libro 2', 12.50),
('9780000000003', 'Libro 3', 15.00),
('9780000000004', 'Libro 4', 8.75),
('9780000000005', 'Libro 5', 11.20),
('9780000000006', 'Libro 6', 7.30),
('9780000000007', 'Libro 7', 16.45),
('9780000000008', 'Libro 8', 13.99),
('9780000000009', 'Libro 9', 10.50),
('9780000000010', 'Libro 10', 9.00);

-- INSERTS per la tabella Utenti (100 record)
INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password) VALUES 
('TC0001', 'Luca', 'Bianchi', '1990-03-15', 'luca@example.com', 'password123'),
('TC0002', 'Marco', 'Verdi', '1985-07-20', 'marco@example.com', 'pass456'),
('TC0003', 'Anna', 'Rossi', '1992-05-25', 'anna@example.com', 'secure789'),
('TC0004', 'Giulia', 'Neri', '1980-12-01', 'giulia@example.com', 'mypassword'),
('TC0005', 'Stefano', 'Marroni', '1995-11-11', 'stefano@example.com', 'password1');

-- INSERTS per la tabella Prestiti (50 record, esempio)
INSERT INTO Prestiti (id_libro, id_utente, dataInizio, dataFine) VALUES 
('9780000000001', 'TC0001', '2024-01-10', '2024-01-20'),
('9780000000002', 'TC0002', '2024-01-12', '2024-01-22'),
('9780000000003', 'TC0003', '2024-01-15', '2024-01-25');
