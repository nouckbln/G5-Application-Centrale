# Clé secrète pour générer des tokens
SECRET_KEY = 'houdini'
# DEBUG doit être False en production par souçi de sécurité
DEBUG = True
# Détail de la connection à SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# Nombre de fois qu'un mot de passe est hashé
BCRYPT_LOG_ROUNDS = 12
