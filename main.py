import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = 'postgresql://postgres:admin@localhost:5432/netology_bd'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name="Питер")
publisher2 = Publisher(name="Азбука")
session.add_all([publisher1, publisher2])
session.commit()

book1 = Book(title="Капитанская дочка", id_publisher=1)
book2 = Book(title="Евгений Онегин", id_publisher=1)
book3 = Book(title="Python", id_publisher=2)
session.add_all([book1, book2, book3])
session.commit()

shop1 = Shop(name='Книжный дом')
shop2 = Shop(name='Книжный мир')
session.add_all([shop1, shop2])
session.commit()

stock1 = Stock(id_book='1', id_shop='1', count=5)
stock2 = Stock(id_book='2', id_shop='1', count=6)
stock3 = Stock(id_book='3', id_shop='2', count=4)
session.add_all([stock1, stock2, stock3])
session.commit()

sale1 = Sale(price=500, date_sale='09-11-2022', id_stock=1, count=3)
sale2 = Sale(price=700, date_sale='07-03-2018', id_stock=2, count=4)
sale3 = Sale(price=1200, date_sale='01-12-2020', id_stock=3, count=2)
session.add_all([sale1, sale2, sale3])
session.commit()

def get_shops(res):
    query = session.query(
        Book.title, Shop.name, Sale.price, Sale.date_sale,
    ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if res.isdigit():
        query = query.filter(Publisher.id == res).all()
    else:
        query = query.filter(Publisher.name == res).all()
    for title, name, price, date_sale in query:
        print(f"{title: <20} | {name: <15} | {price: <5} | {date_sale.strftime('%d-%m-%Y')}")

if __name__ == "__main__":
    res = input('Введите Id (1 или 2) или имя издателя (Питер или Азбука): ')
    get_shops(res)
