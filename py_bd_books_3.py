from itertools import count
from turtle import title
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40))

    def __str__(self) -> str:
        return f'Publisher {self.id}:({self.name})'


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    publisher_id = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="book")



class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    book_id = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    shop_id = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL(5,2))
    date_sale = sq.Column(sq.Date)
    stock_id = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

login = 'postgres'
password = 'Mikmik38'
name_db = 'py_bd_books'

DSN = 'postgresql://' + login + ':' + password + '@localhost:5432/' + name_db

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Создание объектов (наполнение таблиц)

OReilly = Publisher(name="O\u2019Reilly")
Ms_Press = Publisher(name="Microsoft Press")
Pearson = Publisher(name="Pearson")
N_press = Publisher(name="No starch press")

book_1 = Book(title = 'Programming Python, 4th Edition1',  publisher = OReilly)
book_2 = Book(title = 'Learning Python, 4th Edition',  publisher = OReilly)
book_3 = Book(title = 'Natural Language Processing with Python',  publisher = OReilly)
book_4 = Book(title = 'Hacking: The Art of Exploitation',  publisher = N_press)
book_5 = Book(title = 'Modern Operating Systems',  publisher = Ms_Press)
book_6 = Book(title = 'Code Complete: Second Edition',  publisher = Pearson)

shop_1 = Shop(name = 'Labirint')
shop_2 = Shop(name = 'OZON')
shop_3 = Shop(name = 'Amazon')

stock_1 = Stock(shop = shop_1, book = book_1 , count = 34)
stock_2 = Stock(shop = shop_1, book = book_2, count = 30)
stock_3 = Stock(shop = shop_1, book = book_3, count = 0)
stock_4 = Stock(shop = shop_2, book = book_5, count = 40)
stock_5 = Stock(shop = shop_2, book = book_6, count = 50)
stock_6 = Stock(shop = shop_3, book = book_4, count = 10)
stock_7 = Stock(shop = shop_3, book = book_6, count = 10)
stock_8 = Stock(shop = shop_2, book = book_1, count = 10)
stock_9 = Stock(shop = shop_3, book = book_1, count = 10)

sale_1 = Sale(price = 50.05, date_sale = '2018-10-25', stock = stock_1, count = 16)
sale_2 = Sale(price = 50.05, date_sale = '2018-10-25', stock = stock_3, count = 10)
sale_3 = Sale(price = 10.50, date_sale = '2018-10-25', stock = stock_6, count = 9)
sale_4 = Sale(price = 16.00, date_sale = '2018-10-25', stock = stock_5, count = 5)
sale_5 = Sale(price = 16.00, date_sale = '2018-10-25', stock = stock_9, count = 5)
sale_6 = Sale(price = 16.00, date_sale = '2018-10-25', stock = stock_4, count = 1)

session.add_all([OReilly, Ms_Press, Pearson, N_press])
session.add_all([book_1, book_2, book_3, book_4, book_5, book_6])
session.add_all([shop_1, shop_2, shop_3])
session.add_all([stock_1, stock_2, stock_3, stock_4, stock_5, stock_6, stock_7, stock_8, stock_9])
session.add_all([sale_1, sale_2, sale_3, sale_4, sale_5, sale_6])


session.commit()  # фиксируем изменения

def query_to_base(pub_name):
    subq = session.query(Shop).join(Stock.shop).join(Stock.book).join(Book.publisher).filter(Publisher.name == pub_name)
    for s in subq.all():
        print(s.id, s.name)

publisher_name = input('Input pablisher name: ')
if publisher_name !='':
    query_to_base(publisher_name)
else:
    publisher_id = input('Input publisher id: ')
    if publisher_id != '': 
        pub_id = int(publisher_id)
        q = session.query(Publisher.name).filter(Publisher.id == pub_id)
        query_to_base(q)
