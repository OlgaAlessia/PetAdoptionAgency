from unittest import TestCase

from app import app
from models import db, Pet

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adoption_db_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Don't need to use CSRF for testing
app.config['WTF_CSRF_ENABLED'] = False

db.drop_all()
db.create_all()


class PetViewsTestCase(TestCase):
    def setUp(self):
        """Make demo data."""

        Pet.query.delete()

        pet = Pet(name="TestPet", species="TestDog", photo_url="www.google.com", age=11)
        db.session.add(pet)
        db.session.commit()

        self.pet = pet

    def tearDown(self):
        """Clean up transactions."""

        db.session.rollback()
        
    def test_pet_list(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<img src="{self.pet.photo_url}" class="figure-img img-fluid rounded" alt="{self.pet.name}"', html)
  
    def test_pet_add_form(self):
        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label class="form-label" for="name">Pet Name</label>', html)
    
#    def test_pet_add(self):
#        with app.test_client() as client:
#            d = {"name":"TestPet1", "species":"TestCat", "notes":"Carino e Coccoloso"}
#            resp = client.post("/add", data=d, follow_redirects=True)
#            html = resp.get_data(as_text=True)
#
#            self.assertEqual(resp.status_code, 200)
#            self.assertIn("Created new pet: name is TestPet1, of TestCat", html)
#            
    def test_pet_edit_form(self):
        with app.test_client() as client:
            resp = client.get(f"/{self.pet.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)
            
    def test_pet_edit(self):
        with app.test_client() as client:
            resp = client.post(f"/{self.pet.id}", 
                    data={'available': False, 'photo_url': 'https://t2.gstatic.com/licensed-image?q=tbn:ANd9GcRtK0ghlVD9B8kICThHycGN-lepqMukdhk3-iY6APM3eErNdf1mG9yoYx-7YipisfiB'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"Edited Pet {self.pet.name}", html)

            self.assertIn('<span class="text-danger"> not </span> available!', html)
            
    def test_pet_edit_form_fail(self):
        with app.test_client() as client:
            # add w/ invalid email
            resp = client.post(
                f"/{self.pet.id}",
                data={'photo_url': 'google.'})
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<form", html)
            self.assertIn("Invalid URL", html)