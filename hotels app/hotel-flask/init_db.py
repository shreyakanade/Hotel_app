from app import create_app, db
from models import Package, MenuItem
app = create_app()
with app.app_context():
    db.create_all()
    if not Package.query.first():
        packages = [
            Package(name="Family Package", description="2 rooms + dinner + sightseeing", price=4999.0),
            Package(name="Couple Package", description="Romantic dinner for two", price=2999.0)
        ]
        db.session.bulk_save_objects(packages)
        db.session.commit()
    if not MenuItem.query.first():
        items = [
            MenuItem(name="Grilled Chicken", description="Served with veggies", price=499.0),
            MenuItem(name="Pav Bhaji", description="Spicy Indian staple", price=249.0)
        ]
        db.session.bulk_save_objects(items)
        db.session.commit()
print("DB initialized and seeded.")
