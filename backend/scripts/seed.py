from app.database import SessionLocal
from app.models import User, Category, Product
from app.utils.security import hash_password

products = [
    ('Auriculares Pro', 19999), ('Smartwatch Fit', 25999), ('Mouse Gamer', 8999), ('Teclado Mecánico', 15999),
    ('Campera Urbana', 18999), ('Remera Basic', 5999), ('Lentes Classic', 7499), ('Mochila Tech', 14999),
    ('Lámpara LED', 12999), ('Set Cocina', 21999), ('Silla Ergonómica', 49999), ('Organizador Desk', 5499)
]

cats = [('Electrónica','electronica'),('Ropa','ropa'),('Accesorios','accesorios'),('Hogar','hogar')]


def run():
    db = SessionLocal()
    category_map = {}
    for name, slug in cats:
        cat = Category(name=name, slug=slug, description=f'Categoría {name}')
        db.add(cat)
        db.flush()
        category_map[name] = cat.id

    for i, (name, price) in enumerate(products):
        db.add(Product(name=name, description=f'{name} con detalles premium.', price=price, stock=10+i, category_id=list(category_map.values())[i%4], images=['https://images.unsplash.com/photo-1491553895911-0055eca6402d']))

    db.add(User(email='admin@example.com', password_hash=hash_password('admin123'), first_name='Admin', last_name='User', is_admin=True))
    db.add(User(email='user1@example.com', password_hash=hash_password('user12345'), first_name='Ana', last_name='Pérez'))
    db.add(User(email='user2@example.com', password_hash=hash_password('user12345'), first_name='Luis', last_name='Gómez'))

    db.commit()
    db.close()
    print('Seed completado')

if __name__ == '__main__':
    run()
