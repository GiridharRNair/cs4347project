from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, g, jsonify, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sneakervault.db"
DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "sql"

VALID_STATUSES = {"Available", "Reserved", "Sold"}

app = Flask(__name__, static_folder="html", static_url_path="")
app.config["DATABASE"] = str(DB_PATH)


def init_db_if_needed() -> None:
    """Initialize database if it doesn't exist."""
    if DB_PATH.exists():
        return

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    # Create schema
    conn.executescript((SQL_DIR / "schema.sql").read_text())

    # Load CSV data
    def load_csv(
        conn: sqlite3.Connection, file_name: str, query: str, transform=None
    ) -> None:
        file_path = DATA_DIR / file_name
        if not file_path.exists():
            return
        with file_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = [transform(row) if transform else row for row in reader]
            conn.executemany(query, rows)

    load_csv(
        conn,
        "sneaker.csv",
        """
        INSERT INTO Sneaker (ID, Brand, Model, Colorway, ReleaseDate)
        VALUES (:ID, :Brand, :Model, :Colorway, :ReleaseDate)
        """,
    )

    load_csv(
        conn,
        "supplier.csv",
        """
        INSERT INTO Supplier (ID, Name, Type, ContactInfo)
        VALUES (:ID, :Name, :Type, :ContactInfo)
        """,
    )

    load_csv(
        conn,
        "customer.csv",
        """
        INSERT INTO Customer (ID, Phone, FirstName, LastName, Email)
        VALUES (:ID, :Phone, :FirstName, :LastName, :Email)
        """,
    )

    load_csv(
        conn,
        "purchase_price.csv",
        """
        INSERT INTO PurchasePrice (SneakerID, Size, "Condition", PurchasePrice)
        VALUES (:SneakerID, :Size, :Condition, :PurchasePrice)
        """,
    )

    def inv_transform(row: dict[str, str]) -> dict[str, str | None]:
        row["CustomerID"] = row["CustomerID"] or None
        return row

    load_csv(
        conn,
        "inventory.csv",
        """
        INSERT INTO Inventory (ID, SneakerID, SupplierID, Size, "Condition", Status, CustomerID)
        VALUES (:ID, :SneakerID, :SupplierID, :Size, :Condition, :Status, :CustomerID)
        """,
        transform=inv_transform,
    )

    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_PATH}")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(_: Any) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def parse_int(value: str, field_name: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a whole number.") from exc
    if parsed <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")
    return parsed


def parse_optional_int(value: Any, field_name: str) -> int | None:
    text = str(value or "").strip()
    if not text:
        return None
    return parse_int(text, field_name)


def parse_float(value: str, field_name: str) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be numeric.") from exc
    if parsed <= 0:
        raise ValueError(f"{field_name} must be greater than 0.")
    return parsed


def parse_status(value: str) -> str:
    if value not in VALID_STATUSES:
        raise ValueError("Status must be Available, Reserved, or Sold.")
    return value


def next_id(table_name: str) -> int:
    db = get_db()
    return db.execute(f"SELECT COALESCE(MAX(ID), 0) + 1 FROM {table_name}").fetchone()[0]


def bad_request(message: str, status_code: int = 400):
    return jsonify({"ok": False, "error": message}), status_code


def ok(payload: dict[str, Any], status_code: int = 200):
    result = {"ok": True}
    result.update(payload)
    return jsonify(result), status_code


def fetch_dashboard_metrics() -> dict[str, Any]:
    db = get_db()

    metrics = {
        "total_inventory": db.execute("SELECT COUNT(*) FROM Inventory").fetchone()[0],
        "items_sold": db.execute("SELECT COUNT(*) FROM Inventory WHERE Status = 'Sold'").fetchone()[0],
        "items_available": db.execute("SELECT COUNT(*) FROM Inventory WHERE Status = 'Available'").fetchone()[0],
        "items_reserved": db.execute("SELECT COUNT(*) FROM Inventory WHERE Status = 'Reserved'").fetchone()[0],
    }

    cost_of_sold = db.execute(
        """
        SELECT COALESCE(SUM(pp.PurchasePrice), 0)
        FROM Inventory i
        JOIN PurchasePrice pp
            ON pp.SneakerID = i.SneakerID
            AND pp.Size = i.Size
            AND pp."Condition" = i."Condition"
        WHERE i.Status = 'Sold'
        """
    ).fetchone()[0]
    metrics["sold_inventory_cost"] = float(cost_of_sold)

    recent_sold = db.execute(
        """
        SELECT i.ID AS ItemID,
               i.CustomerID,
               s.Brand,
               s.Model
        FROM Inventory i
        JOIN Sneaker s ON s.ID = i.SneakerID
        WHERE i.Status = 'Sold'
        ORDER BY i.ID DESC
        LIMIT 8
        """
    ).fetchall()

    return {"metrics": metrics, "recent_sold": recent_sold}


@app.route("/")
def index() -> Any:
    return app.send_static_file("index.html")


@app.route("/index.html")
def page_index() -> Any:
    return app.send_static_file("index.html")


@app.route("/add_sneaker.html")
def page_add_sneaker() -> Any:
    return app.send_static_file("add_sneaker.html")


@app.route("/add_inventory.html")
def page_add_inventory() -> Any:
    return app.send_static_file("add_inventory.html")


@app.route("/supplier_management.html")
def page_supplier_management() -> Any:
    return app.send_static_file("supplier_management.html")


@app.route("/record_sale.html")
def page_record_sale() -> Any:
    return app.send_static_file("record_sale.html")


@app.route("/customer_management.html")
def page_customer_management() -> Any:
    return app.send_static_file("customer_management.html")


@app.route("/inventory_search.html")
def page_inventory_search() -> Any:
    return app.send_static_file("inventory_search.html")


@app.route("/reports.html")
def page_reports() -> Any:
    return app.send_static_file("reports.html")


@app.route("/style.css")
def page_style_css() -> Any:
    return app.send_static_file("style.css")


@app.route("/app.js")
def page_app_js() -> Any:
    return app.send_static_file("app.js")


@app.route("/api/dashboard")
def api_dashboard() -> Any:
    data = fetch_dashboard_metrics()
    metrics = data["metrics"]
    recent_sold = [dict(row) for row in data["recent_sold"]]
    return ok({"metrics": metrics, "recentSold": recent_sold})


@app.route("/api/sneakers", methods=["GET", "POST"])
def api_sneakers() -> Any:
    db = get_db()
    if request.method == "GET":
        rows = db.execute(
            "SELECT ID, Brand, Model, Colorway, ReleaseDate FROM Sneaker ORDER BY ID DESC"
        ).fetchall()
        return ok({"sneakers": [dict(r) for r in rows]})

    data = request.get_json(silent=True) or {}
    try:
        sneaker_id = parse_optional_int(data.get("sneakerId"), "Sneaker ID")
        brand = str(data.get("brand", "")).strip()
        model = str(data.get("model", "")).strip()
        colorway = str(data.get("colorway", "")).strip()
        release_date = str(data.get("releaseDate", "")).strip() or None
        if sneaker_id is None:
            sneaker_id = next_id("Sneaker")
        if not brand or not model:
            raise ValueError("Brand and model are required.")
    except ValueError as err:
        return bad_request(str(err))

    try:
        db.execute(
            """
            INSERT INTO Sneaker (ID, Brand, Model, Colorway, ReleaseDate)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sneaker_id, brand, model, colorway, release_date),
        )
        db.commit()
    except sqlite3.IntegrityError as err:
        return bad_request(f"Could not add sneaker: {err}")
    return ok({"message": f"Sneaker saved with ID {sneaker_id}."}, 201)


@app.route("/api/sneakers/<int:sneaker_id>", methods=["DELETE"])
def api_delete_sneaker(sneaker_id: int) -> Any:
    db = get_db()
    try:
        db.execute("DELETE FROM Sneaker WHERE ID = ?", (sneaker_id,))
        db.commit()
    except sqlite3.IntegrityError:
        return bad_request("Cannot delete sneaker referenced by inventory or purchase price.")
    return ok({"message": "Sneaker deleted."})


@app.route("/api/inventory", methods=["GET", "POST"])
def api_inventory() -> Any:
    db = get_db()
    if request.method == "GET":
        brand = (request.args.get("brand") or "").strip()
        size = (request.args.get("size") or "").strip()
        status = (request.args.get("status") or "").strip()

        where_parts = []
        params: list[Any] = []

        if brand:
            where_parts.append("s.Brand LIKE ?")
            params.append(f"%{brand}%")
        if size:
            try:
                size_num = parse_float(size, "Size")
                where_parts.append("i.Size = ?")
                params.append(size_num)
            except ValueError as err:
                return bad_request(str(err))
        if status:
            try:
                status = parse_status(status)
            except ValueError as err:
                return bad_request(str(err))
            where_parts.append("i.Status = ?")
            params.append(status)

        where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""

        rows = db.execute(
            f"""
            SELECT i.ID AS ItemID,
                   i.SneakerID,
                   s.Brand,
                   s.Model,
                   i.Size,
                   i."Condition" AS ItemCondition,
                   pp.PurchasePrice,
                   i.SupplierID,
                   i.Status,
                   i.CustomerID
            FROM Inventory i
            JOIN Sneaker s ON s.ID = i.SneakerID
            JOIN PurchasePrice pp
              ON pp.SneakerID = i.SneakerID
             AND pp.Size = i.Size
             AND pp."Condition" = i."Condition"
            {where_clause}
            ORDER BY i.ID DESC
            """,
            params,
        ).fetchall()
        return ok({"inventory": [dict(r) for r in rows]})

    data = request.get_json(silent=True) or {}
    try:
        item_id = parse_optional_int(data.get("itemId"), "Item ID")
        sneaker_id = parse_int(str(data.get("sneakerId", "")), "Sneaker ID")
        size = parse_float(str(data.get("size", "")), "Size")
        condition = str(data.get("condition", "")).strip()
        purchase_price = parse_float(str(data.get("purchasePrice", "")), "Purchase Price")
        supplier_id = parse_int(str(data.get("supplierId", "")), "Supplier ID")
        status = parse_status(str(data.get("status", "")).strip())
        if item_id is None:
            item_id = next_id("Inventory")
        if not condition:
            raise ValueError("Condition is required.")
    except ValueError as err:
        return bad_request(str(err))

    try:
        db.execute(
            """
            INSERT OR REPLACE INTO PurchasePrice (SneakerID, Size, "Condition", PurchasePrice)
            VALUES (?, ?, ?, ?)
            """,
            (sneaker_id, size, condition, purchase_price),
        )
        db.execute(
            """
            INSERT INTO Inventory (ID, SneakerID, SupplierID, Size, "Condition", Status, CustomerID)
            VALUES (?, ?, ?, ?, ?, ?, NULL)
            """,
            (item_id, sneaker_id, supplier_id, size, condition, status),
        )
        db.commit()
    except sqlite3.IntegrityError as err:
        return bad_request(f"Could not add inventory item: {err}")
    return ok({"message": f"Inventory item saved with Item ID {item_id}."}, 201)


@app.route("/api/inventory/<int:item_id>", methods=["DELETE"])
def api_delete_inventory(item_id: int) -> Any:
    db = get_db()
    db.execute("DELETE FROM Inventory WHERE ID = ?", (item_id,))
    db.commit()
    return ok({"message": "Inventory item deleted."})

@app.route("/api/suppliers", methods=["GET", "POST"])
def api_suppliers() -> Any:
    db = get_db()
    if request.method == "GET":
        search_name = (request.args.get("searchName") or "").strip()
        search_type = (request.args.get("searchType") or "").strip()

        where_parts = []
        params: list[Any] = []

        if search_name:
            where_parts.append("Name LIKE ?")
            params.append(f"%{search_name}%")
        if search_type:
            where_parts.append("Type LIKE ?")
            params.append(f"%{search_type}%")

        where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        rows = db.execute(
            f"SELECT ID, Name, Type, ContactInfo FROM Supplier {where_clause} ORDER BY ID DESC",
            params,
        ).fetchall()
        return ok({"suppliers": [dict(r) for r in rows]})

    data = request.get_json(silent=True) or {}
    try:
        supplier_id = parse_optional_int(data.get("supplierId"), "Supplier ID")
        name = str(data.get("name", "")).strip()
        supplier_type = str(data.get("type", "")).strip()
        contact_info = str(data.get("contactInfo", "")).strip()
        if supplier_id is None:
            supplier_id = next_id("Supplier")
        if not name or not supplier_type or not contact_info:
            raise ValueError("Name, type, and contact info are required.")
    except ValueError as err:
        return bad_request(str(err))

    try:
        db.execute(
            """
            INSERT INTO Supplier (ID, Name, Type, ContactInfo)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(ID) DO UPDATE SET
                Name = excluded.Name,
                Type = excluded.Type,
                ContactInfo = excluded.ContactInfo
            """,
            (supplier_id, name, supplier_type, contact_info),
        )
        db.commit()
    except sqlite3.IntegrityError as err:
        return bad_request(f"Supplier operation failed: {err}")
    return ok({"message": f"Supplier saved with ID {supplier_id}."})
@app.route("/api/suppliers/<int:supplier_id>", methods=["DELETE"])
def api_delete_supplier(supplier_id: int) -> Any:
    db = get_db()
    try:
        db.execute("DELETE FROM Supplier WHERE ID = ?", (supplier_id,))
        db.commit()
    except sqlite3.IntegrityError as err:
        return bad_request(f"Cannot delete supplier: {err}")
    return ok({"message": "Supplier deleted."})


@app.route("/api/customers", methods=["GET", "POST"])
def api_customers() -> Any:
    db = get_db()
    if request.method == "GET":
        search_name = (request.args.get("searchName") or "").strip()
        search_email = (request.args.get("searchEmail") or "").strip()

        where_parts = []
        params: list[Any] = []

        if search_name:
            where_parts.append("(FirstName LIKE ? OR LastName LIKE ?)")
            params.extend([f"%{search_name}%", f"%{search_name}%"])
        if search_email:
            where_parts.append("Email LIKE ?")
            params.append(f"%{search_email}%")

        where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        rows = db.execute(
            f"SELECT ID, FirstName, LastName, Email, Phone FROM Customer {where_clause} ORDER BY ID DESC",
            params,
        ).fetchall()
        return ok({"customers": [dict(r) for r in rows]})

    data = request.get_json(silent=True) or {}
    try:
        customer_id = parse_optional_int(data.get("customerId"), "Customer ID")
        first_name = str(data.get("firstName", "")).strip()
        last_name = str(data.get("lastName", "")).strip()
        email = str(data.get("email", "")).strip()
        phone = str(data.get("phone", "")).strip()
        if customer_id is None:
            customer_id = next_id("Customer")
        if not first_name or not last_name or not email:
            raise ValueError("First name, last name, and email are required.")
    except ValueError as err:
        return bad_request(str(err))

    try:
        db.execute(
            """
            INSERT INTO Customer (ID, Phone, FirstName, LastName, Email)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(ID) DO UPDATE SET
                Phone = excluded.Phone,
                FirstName = excluded.FirstName,
                LastName = excluded.LastName,
                Email = excluded.Email
            """,
            (customer_id, phone or None, first_name, last_name, email),
        )
        db.commit()
    except sqlite3.IntegrityError as err:
        return bad_request(f"Customer operation failed: {err}")
    return ok({"message": f"Customer saved with ID {customer_id}."})


@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def api_delete_customer(customer_id: int) -> Any:
    db = get_db()
    try:
        db.execute("DELETE FROM Customer WHERE ID = ?", (customer_id,))
        db.commit()
    except sqlite3.IntegrityError as err:
        return bad_request(f"Cannot delete customer: {err}")
    return ok({"message": "Customer deleted."})


@app.route("/api/record_sale", methods=["GET", "POST"])
def api_record_sale() -> Any:
    db = get_db()
    if request.method == "GET":
        sold_preview = db.execute(
            """
            SELECT i.ID AS ItemID, i.CustomerID, s.Brand, s.Model
            FROM Inventory i
            JOIN Sneaker s ON s.ID = i.SneakerID
            WHERE i.Status = 'Sold'
            ORDER BY i.ID DESC
            LIMIT 10
            """
        ).fetchall()
        return ok({"soldPreview": [dict(r) for r in sold_preview]})

    data = request.get_json(silent=True) or {}
    try:
        item_id = parse_int(str(data.get("itemId", "")), "Item ID")
        customer_id = parse_int(str(data.get("customerId", "")), "Customer ID")
    except ValueError as err:
        return bad_request(str(err))

    customer_exists = db.execute(
        "SELECT 1 FROM Customer WHERE ID = ?", (customer_id,)
    ).fetchone()
    if not customer_exists:
        return bad_request("Customer ID does not exist.")

    inv_row = db.execute(
        "SELECT Status FROM Inventory WHERE ID = ?", (item_id,)
    ).fetchone()
    if not inv_row:
        return bad_request("Item ID does not exist.")
    if inv_row["Status"] == "Sold":
        return bad_request("Item is already marked as Sold.")

    db.execute(
        "UPDATE Inventory SET Status = 'Sold', CustomerID = ? WHERE ID = ?",
        (customer_id, item_id),
    )
    db.commit()
    return ok({"message": "Sale recorded by updating Inventory status to Sold."})
@app.route("/api/reports")
def api_reports() -> Any:
    db = get_db()

    status_breakdown = db.execute(
        """
        SELECT Status, COUNT(*) AS Count
        FROM Inventory
        GROUP BY Status
        ORDER BY Status
        """
    ).fetchall()

    sold_by_model = db.execute(
        """
        SELECT s.ID AS SneakerID,
               s.Brand,
               s.Model,
               COUNT(*) AS SoldCount,
               COALESCE(SUM(pp.PurchasePrice), 0) AS TotalCost
        FROM Inventory i
        JOIN Sneaker s ON s.ID = i.SneakerID
        JOIN PurchasePrice pp
          ON pp.SneakerID = i.SneakerID
         AND pp.Size = i.Size
         AND pp."Condition" = i."Condition"
        WHERE i.Status = 'Sold'
        GROUP BY s.ID, s.Brand, s.Model
        ORDER BY SoldCount DESC, TotalCost DESC
        LIMIT 10
        """
    ).fetchall()

    supplier_stock = db.execute(
        """
        SELECT sp.ID AS SupplierID,
               sp.Name,
               COUNT(*) AS TotalItems,
               SUM(CASE WHEN i.Status = 'Available' THEN 1 ELSE 0 END) AS AvailableItems,
               SUM(CASE WHEN i.Status = 'Sold' THEN 1 ELSE 0 END) AS SoldItems
        FROM Supplier sp
        LEFT JOIN Inventory i ON i.SupplierID = sp.ID
        GROUP BY sp.ID, sp.Name
        ORDER BY TotalItems DESC, sp.ID
        """
    ).fetchall()

    return ok(
        {
            "statusBreakdown": [dict(r) for r in status_breakdown],
            "soldByModel": [dict(r) for r in sold_by_model],
            "supplierStock": [dict(r) for r in supplier_stock],
        }
    )


if __name__ == "__main__":
    init_db_if_needed()
    app.run(debug=True)
