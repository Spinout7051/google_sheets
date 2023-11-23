from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from database.model import Journal, session


def get_db_chart_data():
    try:
        data = (session.query(Journal.delivery_date, func.sum(Journal.price_usd))
                .group_by(Journal.delivery_date)
                .order_by(Journal.delivery_date)
                .all())
        return data
    except SQLAlchemyError as e:
        print(f"Error occurred while querying chart data: {e}")
        return None


def get_db_table_data():
    try:
        data = session.query(Journal).all()
        return data
    except SQLAlchemyError as e:
        print(f"Error occurred while querying table data: {e}")
        return None


def get_total_data():
    try:
        data = session.query(func.sum(Journal.price_usd)).first()
        return data
    except SQLAlchemyError as e:
        print(f"Error occurred while querying total data: {e}")
        return None


def clean_table():
    try:
        session.query(Journal).delete()
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error occurred while cleaning the table: {e}")


def insert_data(data):
    try:
        session.bulk_insert_mappings(Journal, data)
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error occurred while inserting data: {e}")
