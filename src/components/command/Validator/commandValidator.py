import datetime
import pysnooper
from src.components.command.exceptions import InvalidCommandFormatError


@pysnooper.snoop()
class CommandValidator:
    def __init__(self):
        self.current_datetime = datetime.datetime.now()

    def validate_date_format(self, fmt: str):
        try:
            if not fmt:
                raise InvalidCommandFormatError(self.command_name, self.command_format)
            self.current_datetime.strftime(fmt)
            return True
        except Exception:
            return False

