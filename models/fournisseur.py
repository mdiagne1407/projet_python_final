"""Modèle représentant un fournisseur."""


class Fournisseur:
    """Représente un fournisseur de matériel informatique."""

    def __init__(self, id=None, code="", raison_sociale="", email="",
                 telephone="", adresse="", date_creation=None):
        self.id = id
        self.code = code
        self.raison_sociale = raison_sociale
        self.email = email
        self.telephone = telephone
        self.adresse = adresse
        self.date_creation = date_creation

    def __repr__(self):
        return (f"Fournisseur(id={self.id}, code='{self.code}', "
                f"raison_sociale='{self.raison_sociale}')")

    def __str__(self):
        return (f"[{self.code}] {self.raison_sociale} | "
                f"Email: {self.email} | Tél: {self.telephone}")
