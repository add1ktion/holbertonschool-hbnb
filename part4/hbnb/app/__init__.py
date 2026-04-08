import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    # On récupère le chemin absolu du dossier 'app'
    app_dir = os.path.dirname(os.path.abspath(__file__))
    # Le dossier racine du projet (là où se trouvent templates/ et static/)
    root_dir = os.path.dirname(app_dir)

    # Configuration explicite des dossiers
    app = Flask(__name__, 
                template_folder=os.path.join(root_dir, 'templates'),
                static_folder=os.path.join(root_dir, 'static'),
                static_url_path='/static') # Crucial pour le chargement du CSS
    
    app.config.from_object(config_class)
    
    # Configuration CORS large pour le développement local sur le même port
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Imports des modèles pour SQLAlchemy
    from app.models.user import User
    from app.models.place import Place
    from app.models.amenity import Amenity
    from app.models.review import Review

    # --- 1. Enregistrement du Frontend (Blueprint) ---
    # On le fait AVANT l'API pour qu'il soit prioritaire sur la racine '/'
    from .routes import frontend
    app.register_blueprint(frontend)

    # --- 2. Configuration de l'API RestX ---
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.users import api as users_ns
    from app.api.v1.auth import api as auth_ns

    api = Api(
        app, version='1.0',
        title='HBnB API',
        description='HBnB Application API',      
        doc='/api/v1/' # La doc Swagger sera sur /api/v1/
    )

    api.add_namespace(auth_ns, path='/api/v1/auth')
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app