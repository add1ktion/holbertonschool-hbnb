from app import create_app
from app.services import facade

app = create_app()
with app.app_context():
    user = facade.get_user_by_email('admin@hbnb.io')
    if user:
        # On teste si 'admin1234' match le hash en base
        is_ok = user.verify_password('admin1234')
        print(f"--- DIAGNOSTIC ---")
        print(f"Utilisateur trouvé : {user.first_name}")
        print(f"Mot de passe valide ? {'✅ OUI' if is_ok else '❌ NON (Double hachage suspecté)'}")
        print(f"Hash en base : {user.password[:20]}...") 
    else:
        print("❌ Utilisateur 'admin@hbnb.io' introuvable en base.")