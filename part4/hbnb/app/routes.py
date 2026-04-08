"""Frontend routes definitions."""
from flask import Blueprint, render_template

# On crée l'objet Blueprint
frontend = Blueprint('frontend', __name__)


@frontend.route('/')
def index():
    """Renders the main index page."""
    return render_template('index.html')


@frontend.route('/login.html')
def login():
    """Renders the login page."""
    return render_template('login.html')


@frontend.route('/place.html')
def place_details():
    """Renders the details page of a place."""
    return render_template('place.html')


@frontend.route('/add_review.html')
def add_review():
    """Renders the review submission page."""
    return render_template('add_review.html')
