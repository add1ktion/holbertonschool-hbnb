"""Pattern Repository implementation."""
from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """Abstract base class for all repositories."""

    @abstractmethod
    def add(self, obj):
        """Adds an object to the repository."""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Retrieves an object by ID."""
        pass

    @abstractmethod
    def get_all(self):
        """Retrieves all objects."""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Updates an object."""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Deletes an object by ID."""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Retrieves an object by a specific attribute."""
        pass


class SQLAlchemyRepository(Repository):
    """SQLAlchemy implementation of the Repository pattern."""

    def __init__(self, model):
        """Initializes with the specific SQLAlchemy model."""
        self.model = model

    def add(self, obj):
        """Adds and commits an object to the database."""
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        """Retrieves an object by ID."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieves all objects of this model."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Updates an object with provided data."""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        """Deletes an object by ID."""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieves the first object matching the attribute."""
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
        ).first()

    def get_all_by_attribute(self, attr_name, attr_value):
        """Retrieves all objects matching the attribute."""
        return self.model.query.filter(
            getattr(self.model, attr_name) == attr_value
        ).all()


class InMemoryRepository(Repository):
    """In-memory implementation of the Repository pattern."""

    def __init__(self):
        """Initializes empty storage dictionary."""
        self._storage = {}

    def add(self, obj):
        """Adds an object to storage."""
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """Retrieves an object by ID."""
        return self._storage.get(obj_id)

    def get_all(self):
        """Retrieves all stored objects."""
        return list(self._storage.values())

    def update(self, obj_id, data):
        """Updates an object in storage."""
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """Deletes an object from storage by ID."""
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieves the first object matching the attribute."""
        return next(
            (
                obj for obj in self._storage.values()
                if getattr(obj, attr_name) == attr_value
            ),
            None
        )
