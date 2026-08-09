"""
Configuration de la connexion à la base de données MySQL.

Les valeurs par défaut peuvent être surchargées par des variables
d'environnement, ce qui évite de mettre des identifiants en dur
dans le code (bonne pratique de sécurité).
"""

import os

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Mamadou14072004@"),
    "database": os.getenv("DB_NAME", "gestion_commandes"),
}
