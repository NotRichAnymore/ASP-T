import datetime
import pysnooper


@pysnooper.snoop()
class CommandValidator:
    def __init__(self):
        self.current_datetime = datetime.datetime.now()

    def validate_date_format(self, fmt: str):
        try:
            if fmt is not None and isinstance(fmt, str):
                self.current_datetime.strftime(fmt)
                return True
        except Exception:
            return False

