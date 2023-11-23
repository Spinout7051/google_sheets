import flask
import json

from flask import Flask

from database.db_manager import get_db_chart_data, get_db_table_data, get_total_data

app = Flask(__name__)


def make_json_chart_data():
    db_data = get_db_chart_data()
    result = [{
        'year': row[0].strftime('%m/%d/%Y'),
        'sum_order': row[1],
    } for row in db_data]

    with open('./static/data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


def make_json_table_data():
    db_data = get_db_table_data()
    result = [{
        'id_row': row.id_row,
        'id_order': row.id_order,
        'price_usd': row.price_usd,
        'year': row.delivery_date.strftime('%m/%d/%Y'),
    } for row in db_data]

    with open('./static/table_data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


@app.route('/')
def my_index():
    make_json_chart_data()
    make_json_table_data()
    total_price = get_total_data()
    return flask.render_template('index.html', token=total_price[0])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
