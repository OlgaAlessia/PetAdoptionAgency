from flask import Flask, render_template, flash, redirect, render_template, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///adoption_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "secret40"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["WTF_CSRF_ENABLED"] = False

debug = DebugToolbarExtension(app)

connect_db(app)


# app name
@app.errorhandler(404)

def not_found(e):
    """Renders 404 page."""
  
    return render_template("404.html")


@app.route("/")
def list_pets():
    """Renders homepage."""
    
    pets = Pet.query.all() 
    pets_av = [pet for pet in pets if pet.available]
    pets_nav = [pet for pet in pets if pet.available == False]
    
   # return render_template("list_pets.html", pets_av=pets_av, pets_nav=pets_nav)
    
    return render_template("list_pets.html", pets=pets)
  
  
@app.route("/add", methods=["GET", "POST"])
def add_pet():
    """Renders pet form (GET) or handles pet form submission (POST)"""
    
    form = AddPetForm()
    
    if form.validate_on_submit():
      
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data
        
        pet = Pet(name=name, species=species, photo_url=photo_url,  age=age, notes=notes, available=available)
        

        db.session.add(pet)
        db.session.commit()
        
        flash(f"Created new pet: name is {name}, of {species}")
        return redirect('/')
    else:
        return render_template("add_form.html", form=form)

@app.route('/<int:id>', methods=["GET", "POST"])
def edit_pet(id):
    """Renders the edit form (GET) or handles edit form submission (POST)"""
    
    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)
    
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        
        flash(f"Edited Pet {pet.name}")
        return redirect(url_for('list_pets'))
    else:
 
        return render_template("show_edit_form.html",  form=form, pet=pet)


