
from flask.helpers import url_for
from tests.base import AppTestBase


class UserListTestCase(AppTestBase):
    def test_list_users(self):
        self.create_user()
        self.create_user()
        response = self.client.get(url_for('user_user_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 2)

    def test_create_user_error_with_incorrect_payload(self):
        incorrect_payload = {'username': 'test2@test.com'}
        response = self.client.post(url_for('user_user_list'), json=incorrect_payload)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json[0]['password'][0], 'Missing data for required field.')

    def test_create_user(self):
        correct_payload = {'username': 'test2@test.com', 'password': 'new_secret'}
        response = self.client.post(url_for('user_user_list'), json=correct_payload)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['username'], correct_payload['username'])


class UserDetailTestCase(AppTestBase):
    def test_get_user_detail_not_found(self):
        response = self.client.get(url_for('user_user_details', id=10))

        self.assertEqual(response.status_code, 404)

    def test_get_only_user(self):
        self.create_user()
        response = self.client.get(url_for('user_user_details', id=1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], self.user_data['username'])

    def test_put_user_detail_not_found(self):
        response = self.client.put(url_for('user_user_details', id=10), json={})

        self.assertEqual(response.status_code, 404)

    def test_put_user_attribute(self):
        self.create_user()
        new_username = {'username': 'new_name@test.com'}
        response = self.client.put(
            url_for('user_user_details', id=1),
            json=new_username
        )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json['username'], new_username['username'])

    def test_delete_user_not_found(self):
        response = self.client.delete(url_for('user_user_details', id=10))

        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        self.create_user()
        response = self.client.delete(url_for('user_user_details', id=1))

        self.assertEqual(response.status_code, 204)
