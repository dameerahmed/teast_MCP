import sqlite3
from fastmcp import FastMCP

# Database File Name
DB_FILE = "expenses.db"


def db_init():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


# Start karte waqt table banayen
db_init()

mcp = FastMCP("Expense Tracker MCP")


@mcp.tool()
def create_expense(category: str, amount: float, date: str):
    """Create a new expense entry in the database."""
    conn = sqlite3.connect(DB_FILE)  # Connection yahan open karein
    cursor = conn.cursor()

    query = "INSERT INTO expenses (category, amount, date) VALUES (?, ?, ?)"
    params = (category, amount, date)

    cursor.execute(query, params)
    conn.commit()
    conn.close()
    return f"Expense created: {category}, {amount}, {date}"


@mcp.tool()
def get_expenses_by_category(category: str):
    """Retrieve all expenses for a given category."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT * FROM expenses WHERE category = ?"
    params = (category,)

    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()

    return str(results)


@mcp.tool()
def get_total_expenses():
    """Retrieve the total amount of all expenses."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    query = "SELECT SUM(amount) FROM expenses"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    total = result[0] if result and result[0] is not None else 0.0
    return total


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
