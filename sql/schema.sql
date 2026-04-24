PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS PurchasePrice;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Sneaker;

CREATE TABLE Sneaker (
    ID INTEGER PRIMARY KEY,
    Brand TEXT NOT NULL,
    Model TEXT NOT NULL,
    Colorway TEXT NOT NULL,
    ReleaseDate TEXT,
    UNIQUE (Brand, Model, Colorway)
);

CREATE TABLE Supplier (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Type TEXT NOT NULL,
    ContactInfo TEXT NOT NULL UNIQUE
);

CREATE TABLE Customer (
    ID INTEGER PRIMARY KEY,
    Phone TEXT,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE
);

CREATE TABLE PurchasePrice (
    SneakerID INTEGER NOT NULL,
    Size REAL NOT NULL,
    "Condition" TEXT NOT NULL,
    PurchasePrice REAL NOT NULL,
    PRIMARY KEY (SneakerID, Size, "Condition"),
    FOREIGN KEY (SneakerID) REFERENCES Sneaker(ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE Inventory (
    ID INTEGER PRIMARY KEY,
    SneakerID INTEGER NOT NULL,
    SupplierID INTEGER NOT NULL,
    Size REAL NOT NULL,
    "Condition" TEXT NOT NULL,
    Status TEXT NOT NULL CHECK (Status IN ('Available', 'Reserved', 'Sold')),
    CustomerID INTEGER NULL,
    FOREIGN KEY (SneakerID) REFERENCES Sneaker(ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (SupplierID) REFERENCES Supplier(ID)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (SneakerID, Size, "Condition") REFERENCES PurchasePrice(SneakerID, Size, "Condition")
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

PRAGMA foreign_keys = ON;
