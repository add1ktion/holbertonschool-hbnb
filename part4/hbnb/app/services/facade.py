"""Facade module handling interactions between API and services."""
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app import db


class HBnBFacade:
    """Facade for the HBnB business logic layer."""

    def __init__(self):
        """Initializes repositories for the facade."""
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # --- User methods ---

    def create_user(self, user_data):
        """Creates a new user."""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieves a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieves a user by email."""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Retrieves all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Updates a user."""
        user = self.get_user(user_id)
        if not user:
            return None
        if 'password' in data:
            user.password = data.pop('password')
        user.update(data)
        db.session.commit()
        return user

    def delete_user(self, user_id):
        """Deletes a user."""
        user = self.get_user(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    # --- Amenity methods ---

    def create_amenity(self, amenity_data):
        """Creates a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieves an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieves all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Updates an amenity."""
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        db.session.commit()
        return amenity

    # --- Place methods ---

    def create_place(self, place_data):
        """Creates a new place."""
        owner_id = place_data.pop('owner_id', None)
        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.pop('amenities', [])

        place = Place(owner_id=owner_id, **place_data)

        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieves a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieves all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates a place."""
        place = self.get_place(place_id)
        if not place:
            return None
        place.update(place_data)
        db.session.commit()
        return place

    # --- Review methods ---

    def create_review(self, review_data):
        """Creates a new review."""
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        user = self.get_user(user_id)
        place = self.get_place(place_id)

        if not user:
            raise ValueError("User not found.")
        if not place:
            raise ValueError("Place not found.")

        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieves a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieves all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Retrieves all reviews for a place."""
        place = self.get_place(place_id)
        if not place:
            return None
        return self.review_repo.get_all_by_attribute('_place_id', place_id)

    def update_review(self, review_id, review_data):
        """Updates a review."""
        review = self.get_review(review_id)
        if not review:
            return None
        review.update(review_data)
        db.session.commit()
        return review

    def delete_review(self, review_id):
        """Deletes a review."""
        review = self.get_review(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        return True
