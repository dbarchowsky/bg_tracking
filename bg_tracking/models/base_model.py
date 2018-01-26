from peewee import *
import os
import locale
from dateutil import parser

db = SqliteDatabase(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bgs.db'), **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):

    def collect_request_var(self, form, key):
        try:
            if len(str(form[key])) > 0:
                setattr(self, key, form[key])
        except KeyError:
            raise KeyError('Expected input is missing: {} \n'.format(key))
        except AttributeError:
            raise ValueError('Invalid input for {}.'.format(key))

    def collect_request_string(self, form, key):
        self.collect_request_var(form, key)
        if form[key] is None or form[key] == '':
            setattr(self, key, '')

    def collect_request_int(self, form, key):
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

    def collect_request_bool(self, form, key):
        self.collect_request_var(form, key)
        try:
            if form[key] is None or form[key] == '':
                setattr(self, key, None)
            elif (form[key].lower() == 'true' or
                  form[key] == '1' or
                  form[key].lower() == 'yes' or
                  form[key].lower() == 'on'):
                setattr(self, key, True)
            elif (form[key].lower() == 'false' or
                  form[key] == '0' or
                  form[key].lower() == 'no' or
                  form[key].lower() == 'off'):
                setattr(self, key, False)
            else:
                raise ValueError('Invalid boolean value: {}'.format(form[key]))
        except AttributeError:
            raise ValueError('Invalid value for {}'.format(key))

    def collect_request_float(self, form, key):
        self.collect_request_var(form, key)
        try:
            setattr(self, key, float(form[key]))
        except ValueError:
            if getattr(self, key) is None or getattr(self, key) == '':
                setattr(self, key, None)
            else:
                raise ValueError('Invalid float value: {}.'.format(form[key]))

    def collect_request_date(self, form, key):
        self.collect_request_var(form, key)
        try:
            d = parser.parse(getattr(self, key))
        except ValueError:
            raise ValueError('Invalid date value: {}.'.format(form[key]))
        except TypeError:
            setattr(self, key, None)
        except OverflowError:
            raise ValueError('Invalid date value: {}.'.format(form[key]))
        else:
            setattr(self, key, d.strftime('%Y-%m-%d'))

    class Meta:
        database = db
