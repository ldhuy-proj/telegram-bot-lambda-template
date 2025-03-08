from configs import logger, TLG_SEND_MESSAGE_URL, TLG_ANSWER_CALLBACK_URL, ROW_BUTTONS
from const import ParseMode
import requests
import requests

def bot_send_message(chat_id, message, button_list = [[]], parse_mode = ParseMode.HTML):
    try:
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": False,
            "reply_markup": {
                "inline_keyboard": button_list
            }
        }
        logger.debug(f"Send message request: {payload}")
        response = requests.post(TLG_SEND_MESSAGE_URL,
                        json=payload)
        logger.debug(f"Send message result: {response.json()}")
    except Exception as e:
        logger.exception(f"An error has occurred. Details: {str(e)}")


def generate_button_list(callback_type: str, button_list_info: list) -> list:
    button_list = []
    row_buttons = []
    for the_info in button_list_info:
        row_buttons.append({
            "text": f"{the_info}",
            "callback_data": f"{callback_type}_{the_info}"
        })
        if len(row_buttons) == int(ROW_BUTTONS):
            button_list.append(row_buttons)
            row_buttons = []

    if row_buttons:
        button_list.append(row_buttons)

    return button_list


def answer_callback_query(callback_query_id):
    """Acknowledge the callback query."""
    try:
        response = requests.post(TLG_ANSWER_CALLBACK_URL, data={"callback_query_id": callback_query_id})
        response.raise_for_status()
    except Exception as e:
        logger.exception(f"An error has occurred. Details: {str(e)}")