class DevelopmentConfig():
    DEBUG=True
    MYSQL_HOST = 'mysql-db'
    # MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    # MYSQL_PASSWORD = ''
    MYSQL_DB = 'school'

config = {
    'development': DevelopmentConfig
}