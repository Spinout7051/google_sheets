from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from settings import DATABASE_HOST, DATABASE_NAME, DATABASE_PASS, DATABASE_USER


DB_ENGINE = f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}/{DATABASE_NAME}'
engine = create_engine(DB_ENGINE)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Journal(Base):
    __tablename__ = 'journal'

    id = Column(Integer, primary_key=True)
    id_row = Column(String(16))
    id_order = Column(String(16))
    price_usd = Column(Float)
    delivery_date = Column(DateTime)
    price_rub = Column(Float)


Base.metadata.create_all(engine)
