"""
Classe abstraite BaseDAO.

Elle centralise les méthodes génériques (get_all, get_by_id,
delete_by_id) que chaque DAO spécifique (Fournisseur, Produit,
Commande) hérite et complète avec ses propres besoins.
"""

from abc import ABC, abstractmethod

from database.connexion import Connexion


class BaseDAO(ABC):
    """DAO générique dont héritent tous les DAO spécifiques."""

    table = None  # Nom de la table, défini par chaque sous-classe.

    def __init__(self):
        self.connexion = Connexion().get_connexion()

    @abstractmethod
    def _ligne_vers_objet(self, ligne):
        """Convertit une ligne (dict) issue de la BDD en objet métier."""
        raise NotImplementedError

    def get_all(self):
        """Retourne la liste de tous les enregistrements de la table."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            curseur.execute(f"SELECT * FROM {self.table}")
            lignes = curseur.fetchall()
            return [self._ligne_vers_objet(ligne) for ligne in lignes]
        except Exception as erreur:
            print(f"Erreur lors de la récupération des données : {erreur}")
            return []
        finally:
            curseur.close()

    def get_by_id(self, id_):
        """Retourne un enregistrement précis à partir de son id."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            requete = f"SELECT * FROM {self.table} WHERE id = %s"
            curseur.execute(requete, (id_,))
            ligne = curseur.fetchone()
            return self._ligne_vers_objet(ligne) if ligne else None
        except Exception as erreur:
            print(f"Erreur lors de la récupération de l'enregistrement : {erreur}")
            return None
        finally:
            curseur.close()

    def delete_by_id(self, id_):
        """Supprime un enregistrement à partir de son id."""
        curseur = self.connexion.cursor()
        try:
            requete = f"DELETE FROM {self.table} WHERE id = %s"
            curseur.execute(requete, (id_,))
            self.connexion.commit()
            return curseur.rowcount > 0
        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors de la suppression : {erreur}")
            return False
        finally:
            curseur.close()
