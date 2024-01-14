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

def result():
    query = session.query(Book).join(Stock).join(Shop).join(Sale).join(Publisher).filter(Publisher.id == res).all()
    data = {}
    for q in query:
        data.setdefault(q.title, [])
        for st in q.stock:
            shop_name = st.shop.name
            for c, pr in enumerate(st.sale):
                price = pr.price
                data[q.title].append({'shop_name': shop_name, 'price': price, 'date_sale': pr.date_sale})
    for book in data.keys():
        for item in data[book]:
            shop_name = item['shop_name']
            price = item['price']
            date_sale = item['date_sale']
            print(book + ' | ' + shop_name + ' | ' + str(price) + ' | ' + date_sale.strftime('%m-%d-%Y'))

if __name__ == "__main__":
    res = int(input('Введите Id издателя (1 или 2): '))
    if res:
        result()
