"""
CS 4347 – Assignment 5: SQL Injection Demo
Self-contained Flask app that shares sneakervault.db with the main project.

Run on a different port so both servers can be live simultaneously:
    python sql_injection_demo/app_demo.py
  → http://127.0.0.1:5001
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from flask import Flask, g, jsonify, render_template_string, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "sneakervault.db"   # reuse the main database

app = Flask(__name__)
app.config["DATABASE"] = str(DB_PATH)


# ── DB helpers ────────────────────────────────────────────────────────────────

def get_db() -> sqlite3.Connection:
    if "db" not in g:
        conn = sqlite3.connect(app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


@app.teardown_appcontext
def close_db(_: Any) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def ok(payload: dict[str, Any], status: int = 200):
    result: dict[str, Any] = {"ok": True}
    result.update(payload)
    return jsonify(result), status


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index() -> Any:
    html_path = BASE_DIR / "index.html"
    return html_path.read_text(encoding="utf-8")


# Part (a) – VULNERABLE: user input is concatenated directly into the query
@app.route("/api/sneaker-search/unsafe")
def api_unsafe() -> Any:
    brand    = request.args.get("brand", "")
    model    = request.args.get("model", "")
    colorway = request.args.get("colorway", "")

    # ⚠️  String concatenation — intentionally vulnerable for demonstration
    query = (
        "SELECT ID, Brand, Model, Colorway, ReleaseDate "
        "FROM Sneaker "
        f"WHERE Brand = '{brand}' "
        f"AND Model = '{model}' "
        f"AND Colorway = '{colorway}'"
    )

    db = get_db()
    try:
        rows = db.execute(query).fetchall()
        return ok({"results": [dict(r) for r in rows], "query": query})
    except Exception as err:
        return ok({"results": [], "query": query, "error": str(err)})


# Part (b) – SAFE: parameterized prepared statement
@app.route("/api/sneaker-search/safe")
def api_safe() -> Any:
    brand    = request.args.get("brand", "")
    model    = request.args.get("model", "")
    colorway = request.args.get("colorway", "")

    # ✅  Parameterized — values bound separately, injection is impossible
    query = (
        "SELECT ID, Brand, Model, Colorway, ReleaseDate "
        "FROM Sneaker "
        "WHERE Brand = ? "
        "AND Model = ? "
        "AND Colorway = ?"
    )
    display_query = (
        f"{query}\n"
        f"-- Bound parameters: ('{brand}', '{model}', '{colorway}')"
    )

    db = get_db()
    try:
        rows = db.execute(query, (brand, model, colorway)).fetchall()
        return ok({"results": [dict(r) for r in rows], "query": display_query})
    except Exception as err:
        return ok({"results": [], "query": display_query, "error": str(err)})


if __name__ == "__main__":
    if not DB_PATH.exists():
        raise SystemExit(
            f"Database not found at {DB_PATH}. "
            "Start the main project first (python app.py) to initialise it."
        )
    print(f"Using database: {DB_PATH}")
    app.run(port=5001, debug=True)
