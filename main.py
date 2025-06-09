# # main.py

# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)


# main.py

from app import create_app, db
from app import models  # Make sure models are imported so Flask knows them

app = create_app()

with app.app_context():
    db.create_all()  # ✅ This will create the fitness_class and booking tables if they don’t exist

if __name__ == '__main__':
    app.run(debug=True)
