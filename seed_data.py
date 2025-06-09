from datetime import datetime
from app import db, create_app
from app.models import FitnessClass

app = create_app()

with app.app_context():
    db.create_all()  # Creates fitness.db and all tables if not already there

    # Optional: Seed only if no data exists
    if FitnessClass.query.count() == 0:
        yoga = FitnessClass(
            name="Yoga",
            datetime=datetime(2025, 6, 10, 7, 0),
            instructor="Aarti",
            total_slots=10,              
            available_slots=10
        )
        zumba = FitnessClass(
            name="Zumba",
            datetime=datetime(2025, 6, 11, 18, 0),
            instructor="Rahul",
            total_slots=15,   
            available_slots=15
        )
        db.session.add_all([yoga, zumba])
        db.session.commit()
        print("Seeded fitness classes successfully.")
    else:
        print(" Fitness classes already exist. No seeding needed.")




