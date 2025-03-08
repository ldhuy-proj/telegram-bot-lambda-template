from configs import ADMIN_TELEGRAM_IDS
from const import BSCSCAN_DATETIME_FORMAT, DEFAULT_COURSE_CURRENCY
from datetime import datetime
import time

def get_content_from_message(event_payload):
    chat_id = event_payload['chat']['id']
    first_name = event_payload['chat']['first_name']
    user_message = event_payload.get('text')
    return str(chat_id), first_name, user_message

def get_content_from_callback_query(callback_query):
    chat_id = callback_query['from']['id']
    first_name = callback_query['from']['first_name']
    callback_data = callback_query['data'].split("_")
    callback_id = callback_query['id']
    return str(chat_id), first_name, callback_data, callback_id

def get_current_epoch_time():
    return int(time.time() * 1000)
