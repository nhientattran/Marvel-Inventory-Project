from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from marvel_inventory.forms import CharacterForm
from marvel_inventory.models import Character, db
from marvel_inventory.helpers import description_generator, movies_appeared_generator, super_power_generator
from datetime import datetime

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    characterform = CharacterForm()
    
   
    if request.method == 'POST' and characterform.validate_on_submit():
        name = characterform.name.data
        if characterform.description.data != "":
            description = characterform.description.data
        else:
            description = description_generator(name)
        if characterform.movies_appeared.data != "data":
            movies_appeared = characterform.movies_appeared.data
        else:
            movies_appeared = movies_appeared_generator(name)
        if characterform.super_power.data != "":
            super_power = characterform.super_power.data
        else:
            super_power = super_power_generator(name)
        # movies_appeared = characterform.movies_appeared.data
        # super_power = characterform.super_power.data
        date_created = characterform.date_created if characterform.date_created.data else datetime.utcnow()
        user_token = current_user.token

        character = Character(name, description, movies_appeared, super_power, date_created, user_token)
        
        db.session.add(character)
        db.session.commit()

        return redirect(url_for('site.profile'))

    
    user_token = current_user.token
    characters = Character.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=characterform, characters=characters)