-- SneakerVault Task C: Load Data
-- Run create.sql before this script.
-- If your SQL client requires absolute paths, replace data/*.csv accordingly.

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
