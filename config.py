class Config():
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:Altabatch3@project.cwwlyuwat89s.ap-southeast-1.rds.amazonaws.com:3306/project'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://resita:alta123@localhost:3306/testing'