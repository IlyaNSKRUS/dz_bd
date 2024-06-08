import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale


DSN = 'postgresql://postgres:Qwerty12%40@localhost:5432/mydb'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('C:/PycharmProjects/pythonProject/tests_data.json', 'r') as fd:
    data = json.load(fd)
    # print(data)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    print(record)
    session.add(model(id=record.get('pk'), **record.get('fields'))) # **record.get('fields'))
session.commit()

# TypeError: 'date_sale' is an invalid keyword argument for Sale
#  ОШИБКА:  неверный синтаксис для типа integer: "50.05"