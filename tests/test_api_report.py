
from flask import url_for
from tests.base import AppTestBase


class ReportUserListTestCase(AppTestBase):
    def test_get_report_user_list_with_user_not_authenticated(self):
        self.create_user()
        response = self.client.get(url_for('report_report_user_list'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['msg'], 'Missing Authorization Header')

    def test_get_report_user_list_with_user_authenticated(self):
        self.create_user()
        token = self.create_token()

        response = self.client.get(
            url_for('report_report_user_list'),
            headers=token
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')


class ReportTranscriptListTestCase(AppTestBase):
    def test_get_report_transcript_list_with_user_not_authenticated(self):
        self.create_user()
        self.create_transcript()
        response = self.client.get(url_for('report_report_transcript_list'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['msg'], 'Missing Authorization Header')

    def test_get_report_transcript_list_with_user_authenticated(self):
        self.create_user()
        self.create_transcript()
        token = self.create_token()

        response = self.client.get(
            url_for('report_report_transcript_list'),
            headers=token
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')


class ReportUserDetailTestCase(AppTestBase):
    def test_get_report_transcript_list_with_user_not_authenticated(self):
        self.create_user()
        self.create_transcript()

        response = self.client.get(url_for(
            'report_report_user_detail',
            username=self.user_data['username'])
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json['msg'], 'Missing Authorization Header')

    def test_get_report_transcript_list_with_user_authenticated(self):
        self.create_user()
        self.create_transcript()
        token = self.create_token()

        response = self.client.get(
            url_for(
                'report_report_user_detail',
                username=self.user_data['username']
            ),
            headers=token
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/pdf')

