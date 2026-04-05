# **Sneaker Database Schema**

## **1. Sneaker Table**

**Table Name:** `Sneaker`

**Attributes:**

* `SneakerID` INT **(PK)** – Unique identifier for each sneaker
* `Brand` VARCHAR(50) – Brand name
* `Model` VARCHAR(100) – Model name
* `Colorway` VARCHAR(100) – Color/design *(NULL allowed, default: NULL)*
* `ReleaseDate` DATE – Release date *(NULL allowed, default: NULL)*

**Foreign Keys:** None

---

## **2. Supplier Table**

**Table Name:** `Supplier`

**Attributes:**

* `SupplierID` INT **(PK)** – Unique identifier for each supplier
* `Name` VARCHAR(100) – Supplier name
* `Type` VARCHAR(50) – Category/type *(NULL allowed, default: NULL)*
* `ContactInfo` VARCHAR(150) – Contact details *(NULL allowed, default: NULL)*

**Foreign Keys:** None

---

## **3. Customer Table**

**Table Name:** `Customer`

**Attributes:**

* `CustomerID` INT **(PK)** – Unique identifier for each customer
* `FirstName` VARCHAR(50) – First name
* `LastName` VARCHAR(50) – Last name
* `Email` VARCHAR(100) – Email *(NULL allowed, default: NULL)*
* `Phone` VARCHAR(20) – Phone number *(NULL allowed, default: NULL)*

**Foreign Keys:** None

---

## **4. Inventory Table**

**Table Name:** `Inventory`

**Attributes:**

* `ItemID` INT **(PK)** – Unique inventory item ID
* `SneakerID` INT – References sneaker
* `SupplierID` INT – References supplier
* `Size` DECIMAL(3,1) – Shoe size
* `Condition` VARCHAR(50) – Item condition
* `Status` VARCHAR(30) – Availability *(default: 'Available')*
* `PurchasePrice` DECIMAL(10,2) – Purchase price

**Foreign Keys:**

* `SneakerID` → `Sneaker(SneakerID)` *(ON DELETE NO ACTION)*
* `SupplierID` → `Supplier(SupplierID)` *(ON DELETE NO ACTION)*

---

## **5. Sale Table (Junction Table)**

**Table Name:** `Sale`

**Attributes:**

* `ItemID` INT **(PK, FK)** – Inventory item sold
* `CustomerID` INT **(PK, FK)** – Customer who bought the item

**Foreign Keys:**

* `ItemID` → `Inventory(ItemID)` *(ON DELETE NO ACTION)*
* `CustomerID` → `Customer(CustomerID)` *(ON DELETE NO ACTION)*

---

# **Relationships**

* **Sneaker → Inventory:** One-to-Many

  * One sneaker model can appear in many inventory items

* **Supplier → Inventory:** One-to-Many

  * One supplier can supply many inventory items

* **Inventory ↔ Customer:** Many-to-Many

  * Implemented via the `Sale` table

