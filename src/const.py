BOT_NAME = "My Bot Name"

# TELEGRAM CONSTANTS
TLG_MAXIMUM_MSG_LENGTH = 4096

DE_ENCODED_METHOD = "ascii"
class ResponseText:
    WELCOME_MESSAGE = """
        Welcome {username} to this bot.
    """
    HELP_MESSAGE = """
        This is a help message
    """

class CommandType:
    START = "/start"
    HELP = "help"
    class CallbackType:
        BASIC = "basic"
        GENERAL = "general"

class StatusCode:
    SUCCESS_STATUS_CODES = [code for code in range(200,300)]

class ParseMode:
    HTML = "HTML"
    MARKDOWN_V2 = "MarkdownV2"
    MARKDOWN = "Markdown"

class UserState:
    AWAITING_OTHER_INPUT = "awaiting_other_input"
    AWAITING_USER_INFO_INPUT = "awaiting_user_info_input"
    FREE = None
