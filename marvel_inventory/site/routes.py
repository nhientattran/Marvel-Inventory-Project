from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from marvel_inventory.forms import CharacterForm
from marvel_inventory.models import Character, db
from marvel_inventory.helpers import description_generator

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    characterform = CharacterForm()
    
    try:
        if request.method == 'POST' and characterform.validate_on_submit():
            name = characterform.name.data
            api_description = characterform.description.data if characterform.description.data else description_generator(name)
            movies_appeared = characterform.movies_appeared.data
            super_power = characterform.super_power.data
            date_created = characterform.date_created
            user_token = current_user.token

            character = Character(name, api_description, movies_appeared, super_power, date_created, user_token)
            
            db.session.add(character)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception('Character was not created, please check your form and try again')
    
    user_token = current_user.token
    characters = Character.query.filter_by(user_token=user_token)

    return render_template('profile.html', form=characterform, characters=characters)