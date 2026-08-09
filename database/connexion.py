"""
Gestion de la connexion à la base de données via le pattern Singleton.

Le pattern Singleton garantit qu'une seule instance de connexion
existe pendant toute la durée de vie de l'application, ce qui évite
d'ouvrir inutilement plusieurs connexions à la base de données.
"""

import mysql.connector
from mysql.connector import Error

from database.config import DB_CONFIG


class Connexion:
    """Classe Singleton responsable de la connexion à MySQL."""

    _instance = None
    _connection = None

    def __new__(cls):
        # Si aucune instance n'existe encore, on la crée.
        if cls._instance is None:
            cls._instance = super(Connexion, cls).__new__(cls)
            cls._instance._connecter()
        return cls._instance

    def _connecter(self):
        """Établit la connexion à la base de données."""
        try:
            self._connection = mysql.connector.connect(
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                database=DB_CONFIG["database"],
            )
            if self._connection.is_connected():
                print("Connexion à la base de données réussie.")
        except Error as erreur:
            print(f"Erreur lors de la connexion à la base de données : {erreur}")
            self._connection = None

    def get_connexion(self):
        """Retourne la connexion active, en la rétablissant si besoin."""
        if self._connection is None or not self._connection.is_connected():
            self._connecter()
        return self._connection

    def fermer(self):
        """Ferme proprement la connexion à la base de données."""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Connexion à la base de données fermée.")
