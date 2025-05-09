-- Droppo le tabelle nell’ordine corretto (relazioni inverse)
DROP TABLE IF EXISTS Prestiti;
DROP TABLE IF EXISTS Catalogo;
DROP TABLE IF EXISTS Libro_Autore;
DROP TABLE IF EXISTS Autore;
DROP TABLE IF EXISTS Locazione;
DROP TABLE IF EXISTS Riassunti;
DROP TABLE IF EXISTS Utenti;
DROP TABLE IF EXISTS Libro;

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
    genere VARCHAR(30)
);

-- Tabella degli utenti (correzione della sintassi e controllo formato email)
CREATE TABLE Utenti (
    tesseraCliente VARCHAR(255) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cognome VARCHAR(255) NOT NULL,
    dataNascita DATE NOT NULL,
    email VARCHAR(50) NOT NULL UNIQUE,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    password VARCHAR(255) NOT NULL,
    CHECK (email LIKE '%@%.%')
);

-- Tabella dei prestiti, collegata a Libro e Utenti
CREATE TABLE Prestiti (
    id_libro VARCHAR(13),
    id_utente VARCHAR(255),
    dataInizio DATE NOT NULL,
    dataFine DATE,
    n_prestiti INT DEFAULT 1,
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


CREATE TABLE Catalogo (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(13) NOT NULL,
    id_locazione INT,  -- Può essere NULL se il libro non ha una locazione assegnata
    isPrestato BOOLEAN DEFAULT 0,
    FOREIGN KEY (isbn) REFERENCES Libro(isbn) ON DELETE CASCADE,
    FOREIGN KEY (id_locazione) REFERENCES Locazione(id) ON DELETE SET NULL
);

DROP TABLE IF EXISTS Riassunti;
CREATE TABLE Riassunti (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    isbn VARCHAR(13) NOT NULL,
    tesseraCliente VARCHAR(255) NOT NULL,
    riassunto TEXT NOT NULL,
    dataInserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (isbn) REFERENCES Libro(isbn) ON DELETE CASCADE,
    FOREIGN KEY (tesseraCliente) REFERENCES Utenti(tesseraCliente) ON DELETE CASCADE
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


INSERT INTO Utenti (tesseraCliente, nome, cognome, dataNascita, email, is_admin, password) VALUES
('T001', 'Mario', 'Rossi', '1980-05-12', 'mario.rossi@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T002', 'Luigi', 'Verdi', '1975-09-23', 'luigi.verdi@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T003', 'Anna', 'Bianchi', '1990-07-15', 'anna.bianchi@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T004', 'Sara', 'Neri', '1985-03-08', 'sara.neri@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T005', 'Paolo', 'Verdi', '1970-12-01', 'paolo.verdi@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T006', 'Laura', 'Russo', '1995-11-22', 'laura.russo@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T007', 'Giorgio', 'Ferri', '1982-04-30', 'giorgio.ferri@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T008', 'Elena', 'Esposito', '1992-06-18', 'elena.esposito@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T009', 'Francesco', 'Marino', '1988-08-09', 'francesco.marino@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('T010', 'Martina', 'Colombo', '1998-02-14', 'martina.colombo@example.com', 0, 'scrypt:32768:8:1$FArjfPytjocKSAhK$8bb0af9c5f6a47110e80cd3bdffb7399cc5dad5950826926e82bd9316309ce1c408392d526c09813c5384097e3a0c9e199dba3a9cf65b46cbf0def5b8bbb22fb'),
('admin', 'admin', 'admin', '2025-01-01', 'emaildelladmin@gmail.com', 1, 'scrypt:32768:8:1$S4zk3zdHhGyWNqgv$7bd72c88b31f9cb4b0807837cc7a3a8f0c89d675411ed032d4f32b640698c648d529fb9a525303ab36fbf297eb21f4063a430cda7015844a586730ea55134543');

INSERT INTO Libro (isbn, titolo, genere) VALUES
('9781234567897', 'La Divina Commedia', 'Poema epico'),
('9781234567898', 'I Promessi Sposi', 'Romanzo storico'),
('9781234567899', 'Il Gattopardo', 'Romanzo storico'),
('9781234567800', 'Il Nome della Rosa', 'Romanzo storico/mistero'),
('9781234567801', 'Il Barone Rampante', 'Romanzo di formazione'),
('9781234567802', "Cent'anni di solitudine", 'Romanzo'),
('9781234567803', 'La coscienza di Zeno', 'Romanzo'),
('9781234567804', 'Se questo è un uomo', 'Memorie'),
('9781234567805', 'Il fu Mattia Pascal', 'Romanzo'),
('9781234567806', 'La luna e i falò', 'Romanzo')
;

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
