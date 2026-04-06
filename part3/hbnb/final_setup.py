import os
from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # On crée le VRAI compte admin
    admin = User(
        first_name="Admin", 
        last_name="HBnB", 
        email="admin@hbnb.io", 
        password="admin1234", 
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    
    print("🚀 BASE RÉINITIALISÉE !")
    print("Identifiants : admin@hbnb.io / admin1234")