# # # seed.py

# # from app import create_app, db
# # from app.models import FitnessClass
# # from datetime import datetime
# # import pytz

# # app = create_app()

# # with app.app_context():
# #     db.create_all()

# #     # Optional: Clear and re-add
# #     db.session.query(FitnessClass).delete()

# #     classes = [
# #         FitnessClass(
# #             name='Yoga',
# #             datetime=pytz.timezone('Asia/Kolkata').localize(datetime(2025, 6, 10, 7, 0)),
# #             instructor='Aarti',
# #             total_slots=10,
# #             available_slots=10
# #         ),
# #         FitnessClass(
# #             name='Zumba',
# #             datetime=pytz.timezone('Asia/Kolkata').localize(datetime(2025, 6, 11, 18, 0)),
# #             instructor='Rahul',
# #             total_slots=15,
# #             available_slots=15
# #         )
# #     ]

# #     db.session.bulk_save_objects(classes)
# #     db.session.commit()
# #     print("Seeded classes successfully.")


# seed_data.py

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




