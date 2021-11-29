

from flask.helpers import url_for
from tests.base import AppTestBase


class AuthenticationTestCase(AppTestBase):
    def test_authentication_error_with_invalid_payload(self):
        response = self.client.post(
            url_for('auth_authentication'),
            json={'username': 'some_user'}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[0]['password'][0], 'Missing data for required field.')

    def test_authentication_error_with_invalid_credentials(self):
        response = self.client.post(
            url_for('auth_authentication'),
            json={
                'username': 'user_not_exists@ttest.com',
                'password': 'not_exists'
            }
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid Credentials')

    def test_authentication(self):
        self.create_user()
        response = self.client.post(
            url_for('auth_authentication'),
            json=self.user_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['access_token'])
