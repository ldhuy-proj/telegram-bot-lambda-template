import json
import utils
import callback_handler
import helpers
from configs import logger
from const import CommandType, ResponseText, UserState
from globals import user_states


default_response = {
    "statusCode": 200,
    "body": json.dumps('Hello from Lambda!')
}

@logger.inject_lambda_context
def lambda_handler(event, context):
    try:
        global user_states
        body=json.loads(event['body'])
        logger.debug(f"EVENT's body: {body}")
        logger.debug(f"Global User States: {user_states}")
        if body.get("callback_query"):
            callback_handler.handler(body.get("callback_query"))
            return default_response

        logger.info("Handling user message...")
        event_payload = body['message']
        chat_id, first_name, received_message = utils.get_content_from_message(event_payload)
        logger.debug(f"Received message: {received_message} from {chat_id}-{first_name}")
        if received_message == CommandType.START:
            helpers.bot_send_message(chat_id, ResponseText.WELCOME_MESSAGE.format(username=first_name))
            return default_response

        # User state is usued for handling if the bot is waiting for a user input
        user_state = user_states.get(chat_id) or {}
        if user_state.get("state") == UserState.AWAITING_USER_INFO_INPUT:
            helpers.bot_send_message(chat_id, f"Handle user info input: {received_message}")
            user_states[chat_id] = {"state": UserState.FREE}
            return default_response

        elif user_state.get("state") == UserState.AWAITING_OTHER_INPUT:
            helpers.bot_send_message(chat_id, f"Handle other input: {received_message}")
            user_states[chat_id] = {"state": UserState.FREE}
            return default_response

        # Other commands
        analysed_command = received_message.split(" ")
        command_type = analysed_command[0]
        if command_type == CommandType.HELP:
            helpers.bot_send_message(chat_id, ResponseText.HELP_MESSAGE)

        return default_response
    except Exception as e:
        logger.exception(f"An error has occurred. Details: {str(e)}")
        return {
            "statusCode": 200,
            "body": json.dumps(str(e))
        }