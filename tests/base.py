import unittest, json
from src.main import db, create_app


class BaseTestClass(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            print('\n---- Create databases ----\n')
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            print('\n---- Remove databases ----\n')
            db.session.remove()
            db.drop_all()

def to_json(data):
    return json.loads(data.decode('utf-8'))