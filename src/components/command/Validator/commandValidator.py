import base64
import datetime

import bcrypt
import pysnooper
from pathlib import Path
from src.components.command.exceptions import InvalidCommandFormatError


@pysnooper.snoop()
class CommandValidator:
    def __init__(self):
        self.current_datetime = datetime.datetime.now()

    def validate_date_format(self, command_details, fmt: str):
        try:
            if not fmt:
                raise InvalidCommandFormatError(command_details[0], command_details[1])
            self.current_datetime.strftime(fmt)
            return True
        except Exception:
            return False

    def validate_command(self, tokens: list, command_name, command_format):
        match command_name:
            case 'help':
                if len(tokens) != 2:
                    raise InvalidCommandFormatError(command_name, command_format)
            case 'clear':
                if len(tokens) != 1:
                    raise InvalidCommandFormatError(command_name, command_format)
            case 'history':
                if len(tokens) != 1:
                    raise InvalidCommandFormatError(command_name, command_format)
            case 'date':
                if len(tokens) > 3:
                    raise InvalidCommandFormatError(command_name, command_format)
            case 'sleep':
                if len(tokens) > 2:
                    raise InvalidCommandFormatError(command_name, command_format)
            case 'uptime':
                if len(tokens) != 1:
                    raise InvalidCommandFormatError(command_name, command_format)

    def validate_password(self, password, hashed_password):
        if not isinstance(password, bytes) :
            password = base64.b64encode(bytes(password, 'utf-8'))
        if not isinstance(hashed_password, bytes):
            hashed_password = bytes(hashed_password, 'utf-8')
        return bcrypt.checkpw(password, hashed_password)

    def validate_path(self, path):
        valid_path = Path(path).is_dir()
        return False if not valid_path else True
