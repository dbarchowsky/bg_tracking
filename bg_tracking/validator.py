import datetime


class Validator:
    @staticmethod
    def is_number(s):
        if s is None:
            return False
        try:
            float(s)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def is_integer(v):
        """Tests if variable is an integer.
        Returns:
            (bool): True if the variable is an integer. False if the variable is a string, no matter what its value.
        """
        if v is None:
            return False
        return isinstance(v, int)

    @staticmethod
    def is_boolean(s):
        """Tests if variable is a boolean.
        Returns:
            (bool): True if the variable is a boolean. False otherwise.
        """
        if s is None:
            return False
        return isinstance(s, bool)

    @staticmethod
    def is_date(v):
        if v is None:
            return False
        return type(v) is datetime.datetime

    @staticmethod
    def is_non_empty_string(s):
        if s is None:
            return False
        if not isinstance(s, str):
            return False
        return len(s) > 0

    @staticmethod
    def is_non_zero_int_value(s):
        return s is not None and Validator.is_integer(s) and s > 0

