"""Seed file to make data for Adoption db."""

from models import Pet, db

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
Pet.query.delete()

pet1 = Pet(name="Woofly", species="dog", photo_url="https://ichef.bbci.co.uk/news/976/cpsprodpb/17638/production/_124800859_gettyimages-817514614.jpg.webp",  age=1)
pet2 = Pet(name="Porchetta", species="porcupine", photo_url="https://i0.wp.com/virginiazoo.org/wp-content/uploads/2021/01/PREHENSILE-TAIL-PORCUPINE-scaled.jpg?fit=2560%2C1702&ssl=1", notes="yellow teeth", )
pet3 = Pet(name="Snargle", species="cat", photo_url="https://d.newsweek.com/en/full/2049496/grumpy-maine-coon.jpg?w=1600&h=1600&q=88&f=64f13bc126cd2a7f05722ba91bec4e26", age=3, notes="grumpy", available=True)


db.session.add_all([pet1, pet2, pet3])
db.session.commit()