from configs import logger
from const import CommandType
from course_management import callback as course_callback
from transaction_management import callback as transaction_callback
import utils
import helpers

def handler(callback_query):
    logger.info("Handling callback query...")
    chat_id, first_name, callback_data, callback_id = utils.get_content_from_callback_query(callback_query)
    if callback_data[0] == CommandType.CallbackType.BASIC:
        helpers.bot_send_message(chat_id, f"Basic callback data: {callback_data}")
    elif callback_data[0] == CommandType.CallbackType.GENERAL:
        helpers.bot_send_message(chat_id, f"General callback data: {callback_data}")

    # Answer the callback query to remove the "loading" status
    helpers.answer_callback_query(callback_query_id=callback_id)