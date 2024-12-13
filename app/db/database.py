import sqlite3

DATABASE_NAME = "habits.db"


def init_db():
    """Initialize the database with necessary tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Create habits table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        habit_name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        UNIQUE(user_id, habit_name)
    )
    """)

    # Create habit_dates table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS habit_dates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (habit_id) REFERENCES habits (id),
        UNIQUE(habit_id, date)
    )
    """)

    conn.commit()
    conn.close()


def create_user(user_id: str):
    """Create a new user in the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
    finally:
        conn.close()


def add_habit(user_id: str, habit_name: str):
    """Add a new habit for a user."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO habits (user_id, habit_name) VALUES (?, ?)",
            (user_id, habit_name),
        )
        conn.commit()
    finally:
        conn.close()


def delete_habit(user_id: str, habit_name: str):
    """Delete a habit and all its associated dates."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Get habit_id first
        cursor.execute(
            "SELECT id FROM habits WHERE user_id = ? AND habit_name = ?",
            (user_id, habit_name),
        )
        habit_result = cursor.fetchone()
        if habit_result:
            habit_id = habit_result[0]
            # Delete associated dates first (due to foreign key constraint)
            cursor.execute("DELETE FROM habit_dates WHERE habit_id = ?", (habit_id,))
            # Then delete the habit
            cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        conn.commit()
    finally:
        conn.close()


def toggle_habit_date(user_id: str, habit_name: str, date: str):
    """Toggle a date for a specific habit."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        # Get habit_id
        cursor.execute(
            "SELECT id FROM habits WHERE user_id = ? AND habit_name = ?",
            (user_id, habit_name),
        )
        habit_result = cursor.fetchone()
        if not habit_result:
            return

        habit_id = habit_result[0]

        # Check if date exists
        cursor.execute(
            "SELECT id FROM habit_dates WHERE habit_id = ? AND date = ?",
            (habit_id, date),
        )
        date_exists = cursor.fetchone()

        if date_exists:
            # Delete the date if it exists
            cursor.execute(
                "DELETE FROM habit_dates WHERE habit_id = ? AND date = ?",
                (habit_id, date),
            )
        else:
            # Add the date if it doesn't exist
            cursor.execute(
                "INSERT INTO habit_dates (habit_id, date) VALUES (?, ?)",
                (habit_id, date),
            )

        conn.commit()
    finally:
        conn.close()


def get_user_habits(user_id: str) -> list[str]:
    """Get all habits for a user."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT habit_name FROM habits WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()


def get_habit_dates(user_id: str, habit_name: str) -> list[str]:
    """Get all marked dates for a specific habit."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            SELECT hd.date
            FROM habit_dates hd
            JOIN habits h ON h.id = hd.habit_id
            WHERE h.user_id = ? AND h.habit_name = ?
        """,
            (user_id, habit_name),
        )
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()


def load_user_data(user_id: str) -> tuple[list[str], dict]:
    """Load all habits and their dates for a user."""
    habits = get_user_habits(user_id)
    habit_dates = {}
    for habit in habits:
        dates = get_habit_dates(user_id, habit)
        habit_dates[habit] = set(dates)
    return habits, habit_dates
