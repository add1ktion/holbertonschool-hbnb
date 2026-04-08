from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

app = create_app()

with app.app_context():
    # 1. Reset total pour partir sur une base saine
    db.drop_all()
    db.create_all()

    # 2. Création des Amenities (Les équipements)
    wifi = Amenity(name="WiFi")
    bed = Amenity(name="Bed")
    bath = Amenity(name="Bath")
    db.session.add_all([wifi, bed, bath])
    db.session.commit()

    # 3. Création des Utilisateurs
    admin = User(first_name="Admin", last_name="HBnB", email="admin@hbnb.io", password="admin1234", is_admin=True)
    alice = User(first_name="Alice", last_name="Merveille", email="alice@test.com", password="password123")
    bob = User(first_name="Bob", last_name="Bricoleur", email="bob@test.com", password="password123")
    db.session.add_all([admin, alice, bob])
    db.session.commit()

    # 4. Création des Places (Chacun sa maison)
    # L'Admin a un Loft
    loft = Place(title="Loft Moderne Marais", description="Un espace chic au coeur de Paris.", price=95.0, latitude=48.8566, longitude=2.3522, owner_id=admin.id)
    loft.amenities.append(wifi)
    loft.amenities.append(bath)

    # Alice a une Villa
    villa = Place(title="Villa Côte d'Azur", description="Vue mer et piscine à débordement.", price=212.0, latitude=43.7102, longitude=7.2620, owner_id=alice.id)
    villa.amenities.append(wifi)
    villa.amenities.append(bed)

    # Bob a une Cabane
    cabane = Place(title="Cabane Forestière", description="Calme absolu dans les sapins.", price=49.0, latitude=45.7640, longitude=4.8357, owner_id=bob.id)
    
    db.session.add_all([loft, villa, cabane])
    db.session.commit()

    # 5. Création des Reviews (On croise les avis !)
    # Alice note le Loft de l'Admin
    rev1 = Review(text="Super séjour, l'admin est très réactif !", rating=5, place_id=loft.id, user_id=alice.id)
    # Bob note la Villa d'Alice
    rev2 = Review(text="Un peu cher mais la piscine est incroyable.", rating=4, place_id=villa.id, user_id=bob.id)
    # L'Admin note la Cabane de Bob
    rev3 = Review(text="Idéal pour déconnecter, rustique mais propre.", rating=5, place_id=cabane.id, user_id=admin.id)
    
    db.session.add_all([rev1, rev2, rev3])
    db.session.commit()

    print("✅ Base de données peuplée avec succès !")
    print("--- Comptes créés ---")
    print("Admin: admin@hbnb.io / admin1234")
    print("Alice: alice@test.com / password123")
    print("Bob: bob@test.com / password123")