import unittest
from peewee import *
from bg_tracking.models import *


class BaseModelTestCase(unittest.TestCase):
    """
    Tests BaseModel routines
    """
    def setUp(self):
        base_model.db.connect()

    def tearDown(self):
        base_model.db.close()

    def test_collect_bool_form_data(self):
        m = Background()

        data = {'approved': 'False'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, False)

        data = {'approved': 'True'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, True)

        data = {'approved': ''}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, None)

        data = {'approved': 'false'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, False)

        data = {'approved': 'YES'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, True)

        data = {'approved': 'no'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, False)

        data = {'approved': 'on'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, True)

        data = {'approved': 'Off'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, False)

        data = {'approved': '1'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, True)

        data = {'approved': '0'}
        m.collect_request_bool(data, 'approved')
        self.assertEqual(m.approved, False)

        data = {'approved': '2'}
        with self.assertRaises(ValueError) as e:
            m.collect_request_bool(data, 'approved')
            self.assertEqual(e.msg, 'Invalid boolean value: 2')

        data = {'approved': 1}
        with self.assertRaises(ValueError) as e:
            m.collect_request_bool(data, 'approved')
            self.assertEqual(e.msg, 'Invalid input.')

        data = {'approved': 0}
        with self.assertRaises(ValueError) as e:
            m.collect_request_bool(data, 'approved')
            self.assertEqual(e.msg, 'Invalid input.')

        data = {'bogus_key': 'true'}
        with self.assertRaises(KeyError) as e:
            m.collect_request_bool(data, 'approved')
            self.assertEqual(e.msg, 'Expected input is missing: approved')

        data = {'bogus_key': 'true'}
        m.collect_request_bool(data, 'bogus_key')

    def test_collect_int_form_data(self):
        class TestModel(BaseModel):
            int_field = IntegerField()

        class Meta:
            db_table = 'test_model'

        m = TestModel()
        key = 'int_field'

        data = {key: 1}
        m.collect_request_int(data, key)
        self.assertEqual(m.int_field, data[key])

        data = {key: '1'}
        m.collect_request_int(data, key)
        self.assertEqual(m.int_field, int(data[key]))

        data = {key: '0'}
        m.collect_request_int(data, key)
        self.assertEqual(m.int_field, int(data[key]))

        data = {key: ''}
        m.collect_request_int(data, key)
        self.assertEqual(m.int_field, None)

        data = {key: 'abc'}
        with self.assertRaises(ValueError) as e:
            m.collect_request_int(data, key)
            self.assertRegex(e.msg, '^Invalid value for int_field')

        data = {key: '1.5'}
        with self.assertRaises(ValueError) as e:
            m.collect_request_int(data, key)
            self.assertRegex(e.msg, '^Invalid value for int_field')

        data = {key: '1,000'}
        m.collect_request_int(data, key)
        self.assertEqual(m.int_field, 1000)

        data = {key: '-1'}
        m.collect_request_int(data, key)
        self.assertEqual(m.int_field, int(data[key]))

        data = {key: -2}
        m.collect_request_int(data, key)
        self.assertEqual(m.int_field, data[key])

    def test_collect_float_form_data(self):
        m = Background()

        data = {'hours': '1'}
        m.collect_request_float(data, 'hours')
        self.assertEqual(m.hours, 1.0)

        data = {'hours': '2.5'}
        m.collect_request_float(data, 'hours')
        self.assertEqual(m.hours, 2.5)

        data = {'hours': 1}
        m.collect_request_float(data, 'hours')
        self.assertEqual(m.hours, 1.0)

        data = {'hours': 0}
        m.collect_request_float(data, 'hours')
        self.assertEqual(m.hours, 0.0)

        data = {'hours': ''}
        m.collect_request_float(data, 'hours')
        self.assertEqual(m.hours, None)

        data = {'hours': 'abc'}
        with self.assertRaises(ValueError) as e:
            m.collect_request_float(data, 'hours')
            self.assertEqual(e.msg, 'Invalid float value: abc')

    def test_collect_float_form_data(self):
        m = Background()

        data = {'date_started': '1/23/2018'}
        m.collect_request_date(data, 'date_started')
        self.assertEqual(m.date_started, '2018-01-23')

        data = {'date_started': '2018-01-24'}
        m.collect_request_date(data, 'date_started')
        self.assertEqual(m.date_started, '2018-01-24')

        data = {'date_started': '01/08/2018'}
        m.collect_request_date(data, 'date_started')
        self.assertEqual(m.date_started, '2018-01-08')

        data = {'date_started': 'dagdadfdd'}
        with self.assertRaises(ValueError) as e:
            m.collect_request_date(data, 'date_started')
            self.assertRegex(e.msg, '/^Invalid date value:/')


if __name__ == '__main__':
    unittest.main()
