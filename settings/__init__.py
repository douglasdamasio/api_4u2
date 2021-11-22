import os


class Settings(object):
    DEBUG = os.environ.get('FLASK_DEBUG')
    ENV = os.environ.get('FLASK_ENV')

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_BUCKET = os.environ.get('BUCKET')
    REGION_NAME = os.environ.get('REGION_NAME')

    REPORT_FOLDER = os.path.join(os.getcwd(), 'api', 'reports', 'outputs')

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
