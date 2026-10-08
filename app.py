"""Local development entry point for CodeForge.

Run with: python app.py
Uses SQLite by default; set DATABASE_URL in .env when moving to PostgreSQL.
"""
import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "0") == "1",
        use_reloader=False,
    )
