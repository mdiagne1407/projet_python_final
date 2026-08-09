"""DAO responsable des opérations CRUD sur la table produit."""

from dao.base_dao import BaseDAO
from models.produit import Produit


class ProduitDAO(BaseDAO):

    table = "produit"

    def _ligne_vers_objet(self, ligne):
        return Produit(
            id=ligne["id"],
            reference=ligne["reference"],
            designation=ligne["designation"],
            prix_unitaire=ligne["prix_unitaire"],
            stock=ligne["stock"],
            date_creation=ligne["date_creation"],
        )

    def create(self, produit: Produit):
        """Ajoute un nouveau produit et retourne son id."""
        curseur = self.connexion.cursor()
        try:
            requete = """
                INSERT INTO produit (reference, designation, prix_unitaire, stock)
                VALUES (%s, %s, %s, %s)
            """
            valeurs = (produit.reference, produit.designation,
                       produit.prix_unitaire, produit.stock)
            curseur.execute(requete, valeurs)
            self.connexion.commit()
            return curseur.lastrowid
        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors de la création du produit : {erreur}")
            return None
        finally:
            curseur.close()

    def update(self, produit: Produit):
        """Met à jour un produit existant (désignation, prix, stock)."""
        curseur = self.connexion.cursor()
        try:
            requete = """
                UPDATE produit
                SET reference = %s, designation = %s, prix_unitaire = %s, stock = %s
                WHERE id = %s
            """
            valeurs = (produit.reference, produit.designation,
                       produit.prix_unitaire, produit.stock, produit.id)
            curseur.execute(requete, valeurs)
            self.connexion.commit()
            return curseur.rowcount > 0
        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors de la mise à jour du produit : {erreur}")
            return False
        finally:
            curseur.close()

    def get_by_reference(self, reference):
        """Récupère un produit à partir de sa référence unique."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            curseur.execute("SELECT * FROM produit WHERE reference = %s", (reference,))
            ligne = curseur.fetchone()
            return self._ligne_vers_objet(ligne) if ligne else None
        except Exception as erreur:
            print(f"Erreur lors de la recherche par référence : {erreur}")
            return None
        finally:
            curseur.close()

    def rechercher_par_designation(self, mot_cle):
        """Recherche des produits dont la désignation contient le mot-clé."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            requete = "SELECT * FROM produit WHERE designation LIKE %s"
            curseur.execute(requete, (f"%{mot_cle}%",))
            lignes = curseur.fetchall()
            return [self._ligne_vers_objet(ligne) for ligne in lignes]
        except Exception as erreur:
            print(f"Erreur lors de la recherche : {erreur}")
            return []
        finally:
            curseur.close()

    def produits_sous_seuil(self, seuil):
        """Retourne les produits dont le stock est inférieur au seuil donné."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            curseur.execute("SELECT * FROM produit WHERE stock < %s", (seuil,))
            lignes = curseur.fetchall()
            return [self._ligne_vers_objet(ligne) for ligne in lignes]
        except Exception as erreur:
            print(f"Erreur lors de la vérification des stocks : {erreur}")
            return []
        finally:
            curseur.close()

    def est_dans_une_commande(self, produit_id):
        """Vérifie si un produit apparaît dans au moins une ligne de commande."""
        curseur = self.connexion.cursor()
        try:
            curseur.execute(
                "SELECT COUNT(*) FROM ligne_commande WHERE produit_id = %s",
                (produit_id,),
            )
            (nombre,) = curseur.fetchone()
            return nombre > 0
        except Exception as erreur:
            print(f"Erreur lors de la vérification : {erreur}")
            return True
        finally:
            curseur.close()

    def ajuster_stock(self, produit_id, variation, curseur=None):
        """
        Ajoute (ou retire si négatif) `variation` au stock d'un produit.
        Accepte un curseur externe pour s'inscrire dans une transaction
        globale (utilisé par CommandeDAO).
        """
        curseur_local = curseur or self.connexion.cursor()
        try:
            requete = "UPDATE produit SET stock = stock + %s WHERE id = %s"
            curseur_local.execute(requete, (variation, produit_id))
            if curseur is None:
                self.connexion.commit()
            return True
        except Exception as erreur:
            if curseur is None:
                self.connexion.rollback()
            print(f"Erreur lors de l'ajustement du stock : {erreur}")
            return False
        finally:
            if curseur is None:
                curseur_local.close()
