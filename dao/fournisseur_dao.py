"""DAO responsable des opérations CRUD sur la table fournisseur."""

from dao.base_dao import BaseDAO
from models.fournisseur import Fournisseur


class FournisseurDAO(BaseDAO):

    table = "fournisseur"

    def _ligne_vers_objet(self, ligne):
        return Fournisseur(
            id=ligne["id"],
            code=ligne["code"],
            raison_sociale=ligne["raison_sociale"],
            email=ligne["email"],
            telephone=ligne["telephone"],
            adresse=ligne["adresse"],
            date_creation=ligne["date_creation"],
        )

    def create(self, fournisseur: Fournisseur):
        """Ajoute un nouveau fournisseur et retourne son id."""
        curseur = self.connexion.cursor()
        try:
            requete = """
                INSERT INTO fournisseur (code, raison_sociale, email, telephone, adresse)
                VALUES (%s, %s, %s, %s, %s)
            """
            valeurs = (fournisseur.code, fournisseur.raison_sociale,
                       fournisseur.email, fournisseur.telephone, fournisseur.adresse)
            curseur.execute(requete, valeurs)
            self.connexion.commit()
            return curseur.lastrowid
        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors de la création du fournisseur : {erreur}")
            return None
        finally:
            curseur.close()

    def update(self, fournisseur: Fournisseur):
        """Met à jour les informations d'un fournisseur existant."""
        curseur = self.connexion.cursor()
        try:
            requete = """
                UPDATE fournisseur
                SET code = %s, raison_sociale = %s, email = %s,
                    telephone = %s, adresse = %s
                WHERE id = %s
            """
            valeurs = (fournisseur.code, fournisseur.raison_sociale,
                       fournisseur.email, fournisseur.telephone,
                       fournisseur.adresse, fournisseur.id)
            curseur.execute(requete, valeurs)
            self.connexion.commit()
            return curseur.rowcount > 0
        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors de la mise à jour du fournisseur : {erreur}")
            return False
        finally:
            curseur.close()

    def get_by_code(self, code):
        """Récupère un fournisseur à partir de son code unique."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            curseur.execute("SELECT * FROM fournisseur WHERE code = %s", (code,))
            ligne = curseur.fetchone()
            return self._ligne_vers_objet(ligne) if ligne else None
        except Exception as erreur:
            print(f"Erreur lors de la recherche par code : {erreur}")
            return None
        finally:
            curseur.close()

    def rechercher(self, mot_cle):
        """Recherche des fournisseurs par code ou raison sociale (LIKE)."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            requete = """
                SELECT * FROM fournisseur
                WHERE code LIKE %s OR raison_sociale LIKE %s
            """
            motif = f"%{mot_cle}%"
            curseur.execute(requete, (motif, motif))
            lignes = curseur.fetchall()
            return [self._ligne_vers_objet(ligne) for ligne in lignes]
        except Exception as erreur:
            print(f"Erreur lors de la recherche : {erreur}")
            return []
        finally:
            curseur.close()

    def a_des_commandes(self, fournisseur_id):
        """Vérifie si un fournisseur a au moins une commande associée."""
        curseur = self.connexion.cursor()
        try:
            curseur.execute(
                "SELECT COUNT(*) FROM commande WHERE fournisseur_id = %s",
                (fournisseur_id,),
            )
            (nombre,) = curseur.fetchone()
            return nombre > 0
        except Exception as erreur:
            print(f"Erreur lors de la vérification des commandes : {erreur}")
            return True  # Par sécurité, on empêche la suppression en cas d'erreur.
        finally:
            curseur.close()
