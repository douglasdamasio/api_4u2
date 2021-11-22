
from time import sleep

import boto3
import botocore
from api.transcripts.dtos import AudioDTO
from api.transcripts.exceptions import JobFail, UploadFail
from api.transcripts.models import TranscriptModel
from flask import current_app
from requests import get


class TranscriptService:
    @classmethod
    def speech_to_text(cls, audio: AudioDTO) -> TranscriptModel:
        try:
            cls._upload_audio_file(audio)
        except UploadFail:
            raise UploadFail

        try:
            response = cls._excute_transcribe_job(audio)
        except JobFail:
            raise JobFail

        return TranscriptModel(
            text=response.json()['results']['transcripts'][0]['transcript']
        )

    @staticmethod
    def amazon_up(service: str):
        return boto3.client(
            service,
            aws_access_key_id=current_app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=current_app.config['AWS_SECRET_ACCESS_KEY'],
            region_name=current_app.config['REGION_NAME']
        )

    @classmethod
    def _excute_transcribe_job(cls, audio: AudioDTO) -> dict:
        transcribe = cls.amazon_up('transcribe')
        media_uri = f"s3://{current_app.config['AWS_BUCKET']}/{audio.full_audio_name}"

        transcribe.start_transcription_job(
            TranscriptionJobName=audio.audio_name,
            Media={'MediaFileUri': media_uri},
            MediaFormat=audio.file_type,
            LanguageCode='pt-BR'
        )
        while True:
            result = transcribe.get_transcription_job(TranscriptionJobName=audio.audio_name)
            if result['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            sleep(5)

        if result['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            return get(result['TranscriptionJob']['Transcript']['TranscriptFileUri'])

        else:
            raise JobFail

    @classmethod
    def _upload_audio_file(cls, audio: AudioDTO) -> None:
        s3 = cls.amazon_up('s3')
        try:
            s3.upload_fileobj(
                audio.base64,
                current_app.config['AWS_BUCKET'],
                audio.full_audio_name
            )
        except botocore.exceptions.ClientError:
            raise UploadFail

        sleep(5)
