import binascii
from base64 import b64decode
from datetime import datetime
from io import BytesIO

import filetype
from api.transcripts.exceptions import InvalidType


class AudioDTO:
    def __init__(self, base64: str, username: str):
        self.username = username
        self.audio_name = datetime.now().strftime('%d-%m-%Y-%H-%M-%S')

        try:
            self.base64 = BytesIO(b64decode(base64, validate=True))
        except binascii.Error:
            self.base64 = None

        try:
            self.file_type = self.get_file_type()
        except InvalidType:
            self.file_type = None

        self.full_audio_name = f'{self.audio_name}.{self.file_type}'

    def __repr__(self) -> str:
        return f'<AudioDTO {self.audio_name}>'

    def get_file_type(self) -> str:
        file_type = filetype.guess(self.base64)

        if file_type.EXTENSION in ['wav', 'ogg', 'mp3']:
            self.base64.seek(0)
            return file_type.EXTENSION
        else:
            raise InvalidType
