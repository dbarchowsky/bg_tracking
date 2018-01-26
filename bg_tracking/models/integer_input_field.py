from peewee import *
import locale
from .input_field import InputField


class IntegerInputField(InputField, IntegerField):

    def collect_request_var(self, form, key):
        try:
            v = form[key]
        except KeyError:
            raise KeyError('Expected input is missing: {} \n'.format(key))

        if v is None or v == '':
            setattr(self, key, None)
            return

        # remove commas, e.g. 1,000
        v_str = format('{}').format(v)
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        v_stripped = locale.atoi(v_str)

        try:
            int_value = int(v_stripped)
        except ValueError:
            raise ValueError('Invalid value for {}: {}'.format(key, form[key]))
        else:
            setattr(self, key, int_value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
