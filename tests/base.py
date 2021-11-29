from builtins import classmethod
from unittest import TestCase, mock

from flask.globals import current_app
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

        self.user_data = {
            'username': 'test@test.com',
            'password': 'secure_word'
        }

        self.transcript_data = {
            'username': self.user_data['username'],
            'base64': 'same_base64'
        }

    def tearDown(self) -> None:
        mock.patch.stopall()

    @classmethod
    def tearDownClass(cls):
        cls.app.db.drop_all()
        cls.app_context.pop()

    def create_user(self):
        self.client.post(url_for('user_user_list'), json=self.user_data)

    def create_token(self):
        authentication = self.client.post(
            url_for('auth_authentication'),
            json=self.user_data
        )
        return {
            'Authorization': authentication.json['access_token']
        }

    def create_transcript(self):
        from api.transcripts.models import TranscriptModel
        self.create_user()

        transcript = TranscriptModel(text='same_base64', user_id=1)

        self.app.db.session.add(transcript)
        self.app.db.session.commit()
