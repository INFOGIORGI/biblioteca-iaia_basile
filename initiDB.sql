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
    genere VARCHAR(30),
  	riassunto text(255)
);

-- Tabella degli utenti (correzione della sintassi e controllo formato email)
CREATE TABLE Utenti (
    tesseraCliente VARCHAR(255) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cognome VARCHAR(255) NOT NULL,
    dataNascita DATE NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    CHECK (email LIKE  '%@%.%')
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

INSERT INTO Autore (nome, cognome, dataNascita, dataMorte) VALUES
('Giuseppe', 'Verdi', '1813-10-10', '1901-01-27'),
('Antonio', 'Vivaldi', '1678-03-04', '1741-07-28'),
('Alessandro', 'Manzoni', '1785-03-07', '1873-05-22'),
('Umberto', 'Eco', '1932-01-05', '2016-02-19'),
('Dante', 'Alighieri', '1265-01-01', '1321-09-14'),
('Italo', 'Calvino', '1923-10-15', '1985-09-19'),
('Luigi', 'Pirandello', '1867-06-28', '1936-12-09'),
('Primo', 'Levi', '1919-07-31', '1987-04-11'),
('Elena', 'Ferrante', '1943-01-01', NULL),
('Carlo', 'Collodi', '1826-03-24', '1890-09-26');

INSERT INTO Libro (isbn, titolo, genere, riassunto) VALUES
    ('9781234567897', 'La Divina Commedia', 'Poema epico', 'Un viaggio immaginario attraverso Inferno, Purgatorio e Paradiso, scritto da Dante Alighieri.'),
    ('9781234567898', 'I Promessi Sposi', 'Romanzo storico', 'La storia travagliata degli amori di Renzo e Lucia sullo sfondo della Lombardia del XVII secolo.'),
    ('9781234567899', 'Il Gattopardo', 'Romanzo storico', 'Un ritratto della nobiltà siciliana durante il Risorgimento, centrato sulla figura del Principe di Salina.'),
    ('9781234567800', 'Il Nome della Rosa', 'Romanzo storico/mistero', 'Un giallo ambientato in un monastero medievale, con protagonisti il monaco Guglielmo e il novizio Adso.'),
    ('9781234567801', 'Il Barone Rampante', 'Romanzo di formazione', 'La storia di Cosimo, un giovane che decide di vivere sugli alberi per sfuggire alle convenzioni sociali.'),
    ('9781234567802', "Cent'anni di solitudine", 'Romanzo', 'Una saga familiare che narra la storia dei Buendía in un villaggio immaginario in Colombia.'),
    ('9781234567803', 'La coscienza di Zeno', 'Romanzo', 'Il racconto in prima persona di Zeno Cosini, un uomo alle prese con le sue nevrosi e introspezioni.'),
    ('9781234567804', 'Se questo è un uomo', 'Memorie', 'La testimonianza di Primo Levi sulla sua prigionia nel campo di concentramento di Auschwitz.'),
    ('9781234567805', 'Il fu Mattia Pascal', 'Romanzo', 'La vicenda di un uomo che, creduto morto, decide di cambiare identità e iniziare una nuova vita.'),
    ('9781234567806', 'La luna e i falò', 'Romanzo', 'Il ritorno di un uomo emigrato in America al suo paese natale in Piemonte, alla ricerca delle sue radici.')
;
INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, password) VALUES
('T001', 'Mario', 'Rossi', '1980-05-12', 'mario.rossi@example.com', 'password1'),
('T002', 'Luigi', 'Verdi', '1975-09-23', 'luigi.verdi@example.com', 'password2'),
('T003', 'Anna', 'Bianchi', '1990-07-15', 'anna.bianchi@example.com', 'password3'),
('T004', 'Sara', 'Neri', '1985-03-08', 'sara.neri@example.com', 'password4'),
('T005', 'Paolo', 'Verdi', '1970-12-01', 'paolo.verdi@example.com', 'password5'),
('T006', 'Laura', 'Russo', '1995-11-22', 'laura.russo@example.com', 'password6'),
('T007', 'Giorgio', 'Ferri', '1982-04-30', 'giorgio.ferri@example.com', 'password7'),
('T008', 'Elena', 'Esposito', '1992-06-18', 'elena.esposito@example.com', 'password8'),
('T009', 'Francesco', 'Marino', '1988-08-09', 'francesco.marino@example.com', 'password9'),
('T010', 'Martina', 'Colombo', '1998-02-14', 'martina.colombo@example.com', 'password10');


INSERT INTO Locazione (piano, scaffale, posizione) VALUES
('1', 'A', '1'),
('1', 'A', '2'),
('1', 'B', '1'),
('1', 'B', '2'),
('2', 'A', '1'),
('2', 'A', '2'),
('2', 'B', '1'),
('2', 'B', '2'),
('3', 'A', '1'),
('3', 'A', '2');


INSERT INTO Catalogo (isbn, id_locazione, isPrestato) VALUES
('9781234567897', 1, 0),
('9781234567898', 2, 1),
('9781234567899', 3, 0),
('9781234567800', 4, 0),
('9781234567801', 5, 1),
('9781234567802', 6, 0),
('9781234567803', 7, 0),
('9781234567804', 8, 0),
('9781234567805', 9, 1),
('9781234567806', 10, 0);

INSERT INTO Libro_Autore (id_libro, id_autore) VALUES
('9781234567897', 1),
('9781234567898', 2),
('9781234567899', 3),
('9781234567800', 4),
('9781234567801', 5),
('9781234567802', 6),
('9781234567803', 7),
('9781234567804', 8),
('9781234567805', 9),
('9781234567806', 10);


INSERT INTO Prestiti (id_libro, id_utente, dataInizio, dataFine) VALUES
('9781234567897', 'T001', '2025-01-10', '2025-01-20'),
('9781234567898', 'T002', '2025-02-01', '2025-02-15'),
('9781234567899', 'T003', '2025-03-05', '2025-03-15'),
('9781234567800', 'T004', '2025-04-10', NULL),
('9781234567801', 'T005', '2025-05-20', '2025-06-01'),
('9781234567802', 'T006', '2025-06-15', '2025-06-25'),
('9781234567803', 'T007', '2025-07-10', '2025-07-20'),
('9781234567804', 'T008', '2025-08-05', '2025-08-15'),
('9781234567805', 'T009', '2025-09-01', '2025-09-10'),
('9781234567806', 'T010', '2025-10-15', '2025-10-25');