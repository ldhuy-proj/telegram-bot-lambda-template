from configs import logger
from const import CommandType
from course_management import callback as course_callback
from transaction_management import callback as transaction_callback
import utils
import helpers

def handler(callback_query):
    logger.info("Handling callback query...")
    chat_id, first_name, callback_data, callback_id = utils.get_content_from_callback_query(callback_query)
    if callback_data[0] == CommandType.CallbackType.PRE_REGISTER:
        course_callback.callback_preregister_handler(chat_id, callback_data)
    elif callback_data[0] == CommandType.CallbackType.TRANSACTION:
        transaction_callback.request_transaction_hash(chat_id, request_id=callback_data[1])

    # Answer the callback query to remove the "loading" status
    helpers.answer_callback_query(callback_query_id=callback_id)