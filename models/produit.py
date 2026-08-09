"""Modèle représentant un produit."""


class Produit:
    """Représente un produit du catalogue."""

    def __init__(self, id=None, reference="", designation="",
                 prix_unitaire=0.0, stock=0, date_creation=None):
        self.id = id
        self.reference = reference
        self.designation = designation
        self.prix_unitaire = prix_unitaire
        self.stock = stock
        self.date_creation = date_creation

    def __repr__(self):
        return (f"Produit(id={self.id}, reference='{self.reference}', "
                f"designation='{self.designation}')")

    def __str__(self):
        return (f"[{self.reference}] {self.designation} | "
                f"Prix: {self.prix_unitaire} FCFA | Stock: {self.stock}")
