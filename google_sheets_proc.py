import json
import os
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta

import pygsheets
import requests
import schedule
import telebot

from database.db_manager import clean_table, insert_data
from settings import AUTH_SERVICE_FILE, SHEETS_NAME, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN


def send_telegram_message(message):
    try:
        bot = telebot.TeleBot(TELEGRAM_TOKEN)
        text_message = (
            f'*Срок поставки заказа истек!*\n\n'
            f'Срок поставки: *{message["delivery_date"]}*\n'
            f'Заказ №*{message["id_order"]}*\n'
            f'Стоимость: {message["price_usd"]}$ / {message["price_rub"]}₽\n'
            )

        bot.send_message(TELEGRAM_CHAT_ID, text=text_message, parse_mode='markdown')

    except Exception as e:
        print(f"Failed to send message via Telegram: {e}")


def get_exchange_rate():
    cache_file = './exchange_rate.cache'
    cache_date_format = '%Y-%m-%d %H:%M:%S'

    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)
        last_updated = datetime.strptime(cached_data['update_time'], cache_date_format)
        if datetime.now() - last_updated <= timedelta(hours=1):
            return cached_data['exchange_rate']

    url = 'https://www.cbr.ru/scripts/XML_daily.asp'
    response = requests.get(url)

    if response.status_code == 200:
        xml_string = response.content.decode('windows-1251')
        root_node = ET.fromstring(xml_string)

        for valute in root_node.findall('Valute'):
            if valute.find('CharCode').text == 'USD':
                exchange_rate = float(valute.find('Value').text.replace(',', '.'))
                with open(cache_file, 'w') as f:
                    json.dump({
                        'exchange_rate': exchange_rate,
                        'update_time': datetime.now().strftime(cache_date_format),
                    }, f)
                return exchange_rate


def get_sheet_data():
    try:
        gc = pygsheets.authorize(service_file=AUTH_SERVICE_FILE)
    except Exception as err:
        return f'Unexpected {err=}, {type(err)=}'

    worksheet = gc.open(SHEETS_NAME).sheet1
    sheet_data = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False)

    exchange_rate = get_exchange_rate()
    insert_records = []

    for row in sheet_data[1:]:
        delivery_date = datetime.strptime(row[3], '%d.%m.%Y').date()
        price_rub = int(row[2]) * exchange_rate

        sh_data = {
            'id_row': row[0],
            'id_order': row[1],
            'price_usd': float(row[2]),
            'delivery_date': delivery_date,
            'price_rub': round(price_rub, 2),
        }

        insert_records.append(sh_data)

        if date.today() > delivery_date:
            send_telegram_message(sh_data)

    clean_table()
    insert_data(insert_records)


def main():
    get_sheet_data()
    schedule.every(10).minutes.do(get_sheet_data)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
