import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    publisher = relationship(Publisher, backref="book")

    def __str__(self):
        return f'{self.id}: {self.title}: {self.id_publisher}'

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey('book.id'), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey('shop.id'), nullable=False)

    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

    def __str__(self):
        return f'{self.id}: {self.count}: {self.id_book}: {self.id_shop}'

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey('stock.id'), nullable=False)

    stock = relationship(Stock, backref="sale")

def create_tables(engine):
    Base.metadata.create_all(engine)

def print_pub():
    autor = input('Введите издательство: ')
    selected = session.query(Book.title, Shop.name, Sale.price, Sale.data_sale).join(Publisher).join(Stock).join(
        Shop).join(Sale).filter(Publisher.name.like(autor))
    for s in selected.all():
        print(s)

DSN = 'postgresql://postgres:*******@localhost:5432/netdb'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

pub = Publisher(name='Эксмо')
b1 = Book(title='Евгений Онегин', publisher=pub)
b2 = Book(title='Капитанская дочка', publisher=pub)
shp1 = Shop(name='Книгомир')
shp2 = Shop(name='Читай город')
stk1 = Stock(count='10', book=b1, shop=shp1)
stk2 = Stock(count='5', book=b2, shop=shp2)
sl1 = Sale(count='10', price='500', data_sale='03-06-2024', stock=stk1)
sl2 = Sale(count='3', price='400', data_sale='15-03-2024', stock=stk2)
pub2 = Publisher(name='Проспект')
b3 = Book(title='Война и мир', publisher=pub2)
stk3 = Stock(count='108', book=b3, shop=shp1)
sl3 = Sale(count='2', price='800', data_sale='12-02-2024', stock=stk3)
# session.add_all([pub,pub2,b1,b2,b3,shp1,shp2,stk1,stk2,stk3,sl1,sl2,sl3])
session.commit()  # фиксируем изменения
print_pub()
session.close()

