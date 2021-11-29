from api.transcripts.datasources import TranscriptDataSource
from api.transcripts.dtos import AudioDTO
from api.transcripts.exceptions import JobFail, UploadFail
from api.transcripts.models import TranscriptModel


class TranscriptService:
    @classmethod
    def speech_to_text(cls, audio: AudioDTO) -> TranscriptModel:
        try:
            TranscriptDataSource.upload_audio_file(audio)
        except UploadFail:
            raise UploadFail

        try:
            response = TranscriptDataSource.excute_transcribe_job(audio)
        except JobFail:
            raise JobFail

        return TranscriptModel(
            text=response.json()['results']['transcripts'][0]['transcript']
        )
