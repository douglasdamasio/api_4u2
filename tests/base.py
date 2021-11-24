from builtins import classmethod
from typing import Dict
from unittest import TestCase, mock

from flask.helpers import url_for

from app import create_app


class AppTestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.app.testing = True
        cls.app_context = cls.app.test_request_context()
        cls.app_context.push()
        cls.app.db.create_all()

    def setUp(self):
        self.client = self.app.test_client()

        self.user = {
            'username': 'test@test.com',
            'password': 'secure_word'
        }

    def tearDown(self) -> None:
        mock.patch.stopall()

    @classmethod
    def tearDownClass(cls):
        cls.app.db.drop_all()
        cls.app_context.pop()

    def create_user(self):
        self.client.post(url_for('user_user_list'), json=self.user)

    def create_token(self):
        authentication = self.client.post(
            url_for('auth_authentication'),
            json=self.user
        )
        return {
            'Authorization': 'Bearer ' + authentication.data['access_token']
        }
