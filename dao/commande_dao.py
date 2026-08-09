"""DAO responsable des commandes et de leurs lignes."""

from dao.base_dao import BaseDAO
from dao.produit_dao import ProduitDAO
from models.commande import Commande, LigneCommande, STATUTS


class StockInsuffisantError(Exception):
    """Levée quand la quantité demandée dépasse le stock disponible."""


class TransitionStatutError(Exception):
    """Levée quand on tente de faire reculer le statut d'une commande."""


class CommandeDAO(BaseDAO):

    table = "commande"

    def __init__(self):
        super().__init__()
        self.produit_dao = ProduitDAO()

    def _ligne_vers_objet(self, ligne):
        return Commande(
            id=ligne["id"],
            numero=ligne["numero"],
            date_commande=ligne["date_commande"],
            fournisseur_id=ligne["fournisseur_id"],
            montant_total=ligne["montant_total"],
            statut=ligne["statut"],
            date_creation=ligne["date_creation"],
        )

    # ------------------------------------------------------------------
    # Création d'une commande avec ses lignes (transaction complète)
    # ------------------------------------------------------------------
    def creer_commande(self, numero, fournisseur_id, lignes_saisies):
        """
        Crée une commande avec ses lignes.
        `lignes_saisies` est une liste de tuples (produit_id, quantite).
        Vérifie la disponibilité du stock, calcule le montant total et
        met à jour le stock, le tout dans une seule transaction.
        """
        curseur = self.connexion.cursor()
        try:
            # 1. Vérification du stock disponible pour chaque produit.
            produits = {}
            for produit_id, quantite in lignes_saisies:
                produit = self.produit_dao.get_by_id(produit_id)
                if produit is None:
                    raise ValueError(f"Produit introuvable (id={produit_id})")
                if quantite <= 0:
                    raise ValueError("La quantité doit être supérieure à 0")
                if quantite > produit.stock:
                    raise StockInsuffisantError(
                        f"Stock insuffisant pour '{produit.designation}' "
                        f"(demandé : {quantite}, disponible : {produit.stock})"
                    )
                produits[produit_id] = produit

            # 2. Calcul du montant total.
            montant_total = sum(
                produits[pid].prix_unitaire * qte for pid, qte in lignes_saisies
            )

            # 3. Insertion de la commande.
            requete_commande = """
                INSERT INTO commande (numero, fournisseur_id, montant_total, statut)
                VALUES (%s, %s, %s, 'EN_ATTENTE')
            """
            curseur.execute(requete_commande, (numero, fournisseur_id, montant_total))
            commande_id = curseur.lastrowid

            # 4. Insertion des lignes de commande et mise à jour du stock.
            requete_ligne = """
                INSERT INTO ligne_commande (commande_id, produit_id, quantite, prix_unitaire)
                VALUES (%s, %s, %s, %s)
            """
            for produit_id, quantite in lignes_saisies:
                prix = produits[produit_id].prix_unitaire
                curseur.execute(requete_ligne, (commande_id, produit_id, quantite, prix))
                self.produit_dao.ajuster_stock(produit_id, -quantite, curseur=curseur)

            self.connexion.commit()
            return commande_id

        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors de la création de la commande : {erreur}")
            return None
        finally:
            curseur.close()

    # ------------------------------------------------------------------
    # Détail d'une commande (lignes incluses)
    # ------------------------------------------------------------------
    def get_detail(self, commande_id):
        """Retourne la commande avec ses lignes chargées."""
        commande = self.get_by_id(commande_id)
        if commande is None:
            return None

        curseur = self.connexion.cursor(dictionary=True)
        try:
            requete = """
                SELECT lc.id, lc.commande_id, lc.produit_id, lc.quantite,
                       lc.prix_unitaire, p.designation, p.reference
                FROM ligne_commande lc
                JOIN produit p ON p.id = lc.produit_id
                WHERE lc.commande_id = %s
            """
            curseur.execute(requete, (commande_id,))
            for ligne in curseur.fetchall():
                lc = LigneCommande(
                    id=ligne["id"],
                    commande_id=ligne["commande_id"],
                    produit_id=ligne["produit_id"],
                    quantite=ligne["quantite"],
                    prix_unitaire=ligne["prix_unitaire"],
                )
                lc.designation = ligne["designation"]
                lc.reference = ligne["reference"]
                commande.lignes.append(lc)
            return commande
        except Exception as erreur:
            print(f"Erreur lors de la récupération du détail : {erreur}")
            return commande
        finally:
            curseur.close()

    def get_by_fournisseur(self, fournisseur_id):
        """Retourne toutes les commandes d'un fournisseur donné."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            curseur.execute(
                "SELECT * FROM commande WHERE fournisseur_id = %s", (fournisseur_id,)
            )
            lignes = curseur.fetchall()
            return [self._ligne_vers_objet(ligne) for ligne in lignes]
        except Exception as erreur:
            print(f"Erreur lors de la récupération des commandes : {erreur}")
            return []
        finally:
            curseur.close()

    def get_par_statut(self, statut):
        """Retourne toutes les commandes ayant un statut donné."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            curseur.execute("SELECT * FROM commande WHERE statut = %s", (statut,))
            lignes = curseur.fetchall()
            return [self._ligne_vers_objet(ligne) for ligne in lignes]
        except Exception as erreur:
            print(f"Erreur lors de la récupération des commandes : {erreur}")
            return []
        finally:
            curseur.close()

    # ------------------------------------------------------------------
    # Changement de statut (empêche tout retour en arrière)
    # ------------------------------------------------------------------
    def changer_statut(self, commande_id, nouveau_statut):
        """Fait progresser le statut d'une commande (jamais en arrière)."""
        if nouveau_statut not in STATUTS:
            print("Statut invalide.")
            return False

        commande = self.get_by_id(commande_id)
        if commande is None:
            print("Commande introuvable.")
            return False

        ordre = ["EN_ATTENTE", "VALIDEE", "LIVREE"]
        if commande.statut in ordre and nouveau_statut in ordre:
            if ordre.index(nouveau_statut) < ordre.index(commande.statut):
                print("Impossible de faire reculer le statut d'une commande.")
                return False
        if commande.statut in ("LIVREE", "ANNULEE"):
            print(f"Une commande {commande.statut} ne peut plus changer de statut.")
            return False

        curseur = self.connexion.cursor()
        try:
            curseur.execute(
                "UPDATE commande SET statut = %s WHERE id = %s",
                (nouveau_statut, commande_id),
            )
            self.connexion.commit()
            return curseur.rowcount > 0
        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors du changement de statut : {erreur}")
            return False
        finally:
            curseur.close()

    # ------------------------------------------------------------------
    # Annulation (remet le stock à jour)
    # ------------------------------------------------------------------
    def annuler_commande(self, commande_id):
        """Annule une commande et restitue les quantités au stock."""
        commande = self.get_detail(commande_id)
        if commande is None:
            print("Commande introuvable.")
            return False
        if commande.statut in ("LIVREE", "ANNULEE"):
            print(f"Une commande {commande.statut} ne peut pas être annulée.")
            return False

        curseur = self.connexion.cursor()
        try:
            for ligne in commande.lignes:
                self.produit_dao.ajuster_stock(ligne.produit_id, ligne.quantite, curseur=curseur)
            curseur.execute(
                "UPDATE commande SET statut = 'ANNULEE' WHERE id = %s", (commande_id,)
            )
            self.connexion.commit()
            return True
        except Exception as erreur:
            self.connexion.rollback()
            print(f"Erreur lors de l'annulation : {erreur}")
            return False
        finally:
            curseur.close()

    # ------------------------------------------------------------------
    # Rapports et statistiques
    # ------------------------------------------------------------------
    def top_5_produits(self):
        """Retourne les 5 produits les plus commandés (en quantité)."""
        curseur = self.connexion.cursor(dictionary=True)
        try:
            requete = """
                SELECT p.designation, p.reference, SUM(lc.quantite) AS total_quantite
                FROM ligne_commande lc
                JOIN produit p ON p.id = lc.produit_id
                GROUP BY lc.produit_id, p.designation, p.reference
                ORDER BY total_quantite DESC
                LIMIT 5
            """
            curseur.execute(requete)
            return curseur.fetchall()
        except Exception as erreur:
            print(f"Erreur lors du calcul du top produits : {erreur}")
            return []
        finally:
            curseur.close()

    def chiffre_affaires_total(self):
        """Somme des montants des commandes VALIDEE ou LIVREE."""
        curseur = self.connexion.cursor()
        try:
            curseur.execute(
                """SELECT COALESCE(SUM(montant_total), 0) FROM commande
                   WHERE statut IN ('VALIDEE', 'LIVREE')"""
            )
            (total,) = curseur.fetchone()
            return total
        except Exception as erreur:
            print(f"Erreur lors du calcul du chiffre d'affaires : {erreur}")
            return 0
        finally:
            curseur.close()
