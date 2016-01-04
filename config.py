# Clé secrète pour générer des tokens
SECRET_KEY = 'houdini'
# Identifiants administrateurs
ADMIN_CREDENTIALS = ('admin', 'pa$$')
# DEBUG doit être False en production par souçi de sécurité
DEBUG = True
# Détail de la connexion à PostgreSQL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:houdini@localhost:5433/taxisid'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# Configuration du serveur gmail pour envoyer des mails
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'noreply.taxisid'
MAIL_PASSWORD = '464PK2wnSY774_K'
ADMINS = ['noreply.taxisid@gmail.com']
# Nombre de fois qu'un mot de passe est hashé
BCRYPT_LOG_ROUNDS = 12
