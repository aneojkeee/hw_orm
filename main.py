import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Sale, Book, Stock, Shop


SQLsystem = 'postgresql'
login = 'postgres'
password = '6522'
host = 'localhost'
port = 5432
db_name = "hw_db"

DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('tests_data.json', 'r') as db:
    data = json.load(db)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

publ_name = input('Введите Имя издателя или id: ')
if publ_name.isnumeric():
    for c in session.query(Publisher).filter(
            Publisher.id == int(publ_name)).all():
        print(c)
else:
    for c in session.query(Publisher).filter(
            Publisher.name.like(f'%{publ_name}%')).all():
        print(c)

session.close()
