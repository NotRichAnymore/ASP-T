from src.components.Utilities.utilities import create_error_message

import re
import datetime


class CommandValidator:
    def __init__(self):
        self.current_datetime = str(datetime.datetime.now())

    def validate_date_format(self, tokens):
        try:
            for token in tokens:
                if token is not None and isinstance(token, str):
                    datetime_obj = datetime.datetime.strptime(token, self.current_datetime)
                    if not isinstance(datetime_obj, datetime.datetime):
                        raise Exception
            return True
        except Exception:
            return False

