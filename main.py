"""Point d'entrée principal de l'application."""

from database.connexion import Connexion
from menu.interface import Interface


def main():
    connexion = Connexion()
    try:
        interface = Interface()
        interface.lancer()
    finally:
        connexion.fermer()


if __name__ == "__main__":
    main()
