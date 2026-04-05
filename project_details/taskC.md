## create.sql

```sql
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS PurchasePrice;
DROP TABLE IF EXISTS Customer;
DROP TABLE IF EXISTS Supplier;
DROP TABLE IF EXISTS Sneaker;

CREATE TABLE Sneaker (
  ID INT PRIMARY KEY,
  Brand VARCHAR(50) NOT NULL,
  Model VARCHAR(80) NOT NULL,
  Colorway VARCHAR(100) NOT NULL,
  ReleaseDate DATE,
  CONSTRAINT uq_sneaker_variant UNIQUE (Brand, Model, Colorway)
);

CREATE TABLE Supplier (
  ID INT PRIMARY KEY,
  Name VARCHAR(100) NOT NULL,
  Type VARCHAR(50) NOT NULL,
  ContactInfo VARCHAR(120) NOT NULL,
  CONSTRAINT uq_supplier_contact UNIQUE (ContactInfo)
);

CREATE TABLE Customer (
  ID INT PRIMARY KEY,
  Phone VARCHAR(20),
  FirstName VARCHAR(50) NOT NULL,
  LastName VARCHAR(50) NOT NULL,
  Email VARCHAR(120) NOT NULL,
  CONSTRAINT uq_customer_email UNIQUE (Email)
);

CREATE TABLE PurchasePrice (
  SneakerID INT NOT NULL,
  Size DECIMAL(4,1) NOT NULL,
  `Condition` VARCHAR(20) NOT NULL,
  PurchasePrice DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (SneakerID, Size, `Condition`),
  CONSTRAINT fk_purchaseprice_sneaker
    FOREIGN KEY (SneakerID) REFERENCES Sneaker(ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

CREATE TABLE Inventory (
  ID INT PRIMARY KEY,
  SneakerID INT NOT NULL,
  SupplierID INT NOT NULL,
  Size DECIMAL(4,1) NOT NULL,
  `Condition` VARCHAR(20) NOT NULL,
  Status VARCHAR(20) NOT NULL,
  CustomerID INT NULL,
  CONSTRAINT fk_inventory_sneaker
    FOREIGN KEY (SneakerID) REFERENCES Sneaker(ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_inventory_supplier
    FOREIGN KEY (SupplierID) REFERENCES Supplier(ID)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT fk_inventory_customer
    FOREIGN KEY (CustomerID) REFERENCES Customer(ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_inventory_purchaseprice
    FOREIGN KEY (SneakerID, Size, `Condition`)
    REFERENCES PurchasePrice(SneakerID, Size, `Condition`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE,
  CONSTRAINT chk_inventory_status
    CHECK (Status IN ('Available', 'Reserved', 'Sold'))
);
```

## load.sql

```sql
LOAD DATA LOCAL INFILE 'data/sneaker.csv'
INTO TABLE Sneaker
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ID, Brand, Model, Colorway, ReleaseDate);

LOAD DATA LOCAL INFILE 'data/supplier.csv'
INTO TABLE Supplier
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ID, Name, Type, ContactInfo);

LOAD DATA LOCAL INFILE 'data/customer.csv'
INTO TABLE Customer
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ID, Phone, FirstName, LastName, Email);

LOAD DATA LOCAL INFILE 'data/purchase_price.csv'
INTO TABLE PurchasePrice
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(SneakerID, Size, `Condition`, PurchasePrice);

LOAD DATA LOCAL INFILE 'data/inventory.csv'
INTO TABLE Inventory
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(ID, SneakerID, SupplierID, Size, `Condition`, Status, @CustomerID)
SET CustomerID = NULLIF(@CustomerID, '');
```
