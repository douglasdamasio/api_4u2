
from datetime import datetime
from unittest import mock

from flask.helpers import url_for
from tests.base import AppTestBase

from api.transcripts.exceptions import JobFail, UploadFail


class TranscriptListTestCase(AppTestBase):
    def create_audio_dto(self):
        return mock.Mock(
            username=self.user_data['username'],
            audio_name=str(datetime.now()),
            base64='some_base64',
            file_type='WAV',
            full_audio_name=str(datetime.now()) + 'wav'
        )

    def test_get_transcripts_list(self):
        self.create_transcript()
        response = self.client.get(
            url_for('transcript_transcript_list'),
            json=self.transcript_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) >= 1)

    def test_create_transcript_error_with_incorrect_payload(self):
        response = self.client.post(
            url_for('transcript_transcript_list'),
            json={'username': self.user_data['username']}
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json[0]['base64'][0], 'Missing data for required field.')

    def test_create_transcript_error_with_invalid_audio(self):
        response = self.client.post(
            url_for('transcript_transcript_list'),
            json=self.transcript_data
        )

        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json['message'], 'Audio file error')

    def test_create_transcript_error_with_user_not_found(self):
        with mock.patch(
            'api.transcripts.schemas.AudioDTO',
            return_value=self.create_audio_dto()
        ):

            response = self.client.post(
                url_for('transcript_transcript_list'),
                json={
                    'username': 'user_not_exists@test.com',
                    'base64': 'some_base64'
                }
            )

            self.assertEqual(response.status_code, 404)
            self.assertTrue(response.json['message'], 'User not found')

    def test_create_transcript_error_upload_fail(self):
        self.create_user()
        with mock.patch(
            'api.transcripts.schemas.AudioDTO',
            return_value=self.create_audio_dto()
        ), mock.patch(
            'api.transcripts.services.TranscriptDataSource.upload_audio_file',
            side_effect=UploadFail
        ):

            response = self.client.post(
                url_for('transcript_transcript_list'),
                json=self.transcript_data
            )

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.json['message'], 'We have a problem!')

    def test_create_transcript_error_job_fail(self):
        self.create_user()
        with mock.patch(
            'api.transcripts.schemas.AudioDTO',
            return_value=self.create_audio_dto()
        ), mock.patch(
            'api.transcripts.services.TranscriptDataSource.upload_audio_file'
        ), mock.patch(
            'api.transcripts.services.TranscriptDataSource.excute_transcribe_job',
            side_effect=JobFail
        ):

            response = self.client.post(
                url_for('transcript_transcript_list'),
                json=self.transcript_data
            )

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.json['message'], 'We have a problem!')

    def test_create_transcript(self):
        self.create_user()
        with mock.patch(
            'api.transcripts.schemas.AudioDTO',
            return_value=self.create_audio_dto()
        ), mock.patch(
            'api.transcripts.services.TranscriptDataSource.upload_audio_file'
        ), mock.patch(
            'api.transcripts.services.TranscriptDataSource.excute_transcribe_job'
        ) as response_mock:

            response_mock.return_value.json.return_value = {
                'results': {
                    'transcripts': [{
                        'transcript': 'audio to text test'
                    }]
                }
            }

            response = self.client.post(
                url_for('transcript_transcript_list'),
                json=self.transcript_data
            )

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.json['text'], 'audio to text test')


class TranscriptDetailTestCase(AppTestBase):
    def test_get_transcript_detail(self):
        self.create_transcript()
        response = self.client.get(
            url_for('transcript_transcript_detail', id=1),
            json=self.transcript_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json), 1)

    def test_delete_transcript_error_transcript_not_found(self):
        self.create_transcript()
        response = self.client.delete(
            url_for('transcript_transcript_detail', id=100),
            json=self.transcript_data
        )

        self.assertEqual(response.status_code, 404)
        self.assertTrue(response.json['message'], 'Transcript not found')

    def test_delete_transcript(self):
        self.create_transcript()
        response = self.client.delete(
            url_for('transcript_transcript_detail', id=1),
            json=self.transcript_data
        )

        self.assertEqual(response.status_code, 204)


class TranscriptUserDetailTestCase(AppTestBase):
    def test_get_transcript_user_detail(self):
        self.create_transcript()
        response = self.client.get(
            url_for(
                'transcript_transcript_user_detail',
                username=self.user_data['username']
            ),
            json=self.transcript_data
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.json[0]['user']['username'],
            self.user_data['username']
        )
