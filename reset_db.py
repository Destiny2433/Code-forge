import os
from app import create_app, db
from app.seed import seed

app = create_app()

with app.app_context():
    print("Dropping database...")
    db.drop_all()
    print("Creating database...")
    db.create_all()
    print("Seeding database...")
    seed()
    print("Done!")
