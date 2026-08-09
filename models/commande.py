"""Modèles représentant une commande et ses lignes."""


# Les statuts possibles d'une commande, dans leur ordre de progression.
STATUTS = ["EN_ATTENTE", "VALIDEE", "LIVREE", "ANNULEE"]


class LigneCommande:
    """Représente une ligne d'une commande (un produit commandé)."""

    def __init__(self, id=None, commande_id=None, produit_id=None,
                 quantite=0, prix_unitaire=0.0):
        self.id = id
        self.commande_id = commande_id
        self.produit_id = produit_id
        self.quantite = quantite
        self.prix_unitaire = prix_unitaire

    @property
    def sous_total(self):
        return self.quantite * self.prix_unitaire

    def __repr__(self):
        return (f"LigneCommande(produit_id={self.produit_id}, "
                f"quantite={self.quantite}, prix_unitaire={self.prix_unitaire})")


class Commande:
    """Représente une commande passée à un fournisseur."""

    def __init__(self, id=None, numero="", date_commande=None,
                 fournisseur_id=None, montant_total=0.0,
                 statut="EN_ATTENTE", date_creation=None, lignes=None):
        self.id = id
        self.numero = numero
        self.date_commande = date_commande
        self.fournisseur_id = fournisseur_id
        self.montant_total = montant_total
        self.statut = statut
        self.date_creation = date_creation
        self.lignes = lignes if lignes is not None else []

    def __repr__(self):
        return (f"Commande(id={self.id}, numero='{self.numero}', "
                f"statut='{self.statut}', montant_total={self.montant_total})")

    def __str__(self):
        return (f"[{self.numero}] Statut: {self.statut} | "
                f"Montant total: {self.montant_total} FCFA")
