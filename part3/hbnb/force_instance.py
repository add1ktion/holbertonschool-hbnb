from app import create_app, db
from app.models.user import User
import os

app = create_app()
# On s'assure que le dossier instance existe
if not os.path.exists('instance'):
    os.makedirs('instance')

with app.app_context():
    # On crée les tables dans le fichier que Flask utilise par défaut
    db.create_all()
    
    # On vérifie si l'admin est déjà là (au cas où)
    admin = User.query.filter_by(email="admin@hbnb.io").first()
    if not admin:
        admin = User(
            first_name="Admin",
            last_name="HBnB",
            email="admin@hbnb.io",
            password="admin1234",
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("🚀 Base créée dans /instance avec l'admin !")
    else:
        print("✅ L'admin existe déjà dans /instance.")