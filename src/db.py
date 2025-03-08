from pymongo import MongoClient
from bson.objectid import ObjectId
from configs import logger
import configs


class Dao:
    def __init__(self):
        client = MongoClient(configs.CONNECTION_STR)
        self.db = client[configs.DB_NAME]

# region Any
    def get_all_things(self):
        try:
            result = self.db["t_course"].find({}, {})
            if result:
                return list(result)
            return []
        except Exception as e:
            logger.exception(f"An error has occurred: {str(e)}")
            raise e
# endregion Any