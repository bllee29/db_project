DB_USERNAME = 'test'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_NAME = 'test'
DB_PORT = '3306'

SQLALCHEMY_DATABASE_URI = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"
# import os
#
# BASE_DIR = os.path.dirname(__file__)
#
# SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SECRET_KEY = "dev"