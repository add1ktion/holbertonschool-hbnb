from flask import Blueprint, render_template

# On crée l'objet Blueprint
frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/login.html')
def login():
    return render_template('login.html')

@frontend.route('/place.html')
def place_details():
    return render_template('place.html')

@frontend.route('/add_review.html')
def add_review():
    return render_template('add_review.html')