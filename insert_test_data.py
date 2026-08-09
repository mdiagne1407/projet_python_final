"""Script d'insertion de données de test cohérentes."""

from dao.fournisseur_dao import FournisseurDAO
from dao.produit_dao import ProduitDAO
from dao.commande_dao import CommandeDAO
from models.fournisseur import Fournisseur
from models.produit import Produit


def inserer_donnees_test():
    fournisseur_dao = FournisseurDAO()
    produit_dao = ProduitDAO()
    commande_dao = CommandeDAO()

    fournisseurs = [
        Fournisseur(code="F001", raison_sociale="Dakar Informatique",
                    email="contact@dakarinfo.sn", telephone="221771234567",
                    adresse="Rue 10, Plateau, Dakar"),
        Fournisseur(code="F002", raison_sociale="Sénégal Bureautique",
                    email="contact@senbureau.sn", telephone="221781234567",
                    adresse="Zone Industrielle, Dakar"),
        Fournisseur(code="F003", raison_sociale="TechDistrib Sénégal",
                    email="contact@techdistrib.sn", telephone="221701234567",
                    adresse="Almadies, Dakar"),
    ]
    ids_fournisseurs = []
    for f in fournisseurs:
        fid = fournisseur_dao.create(f)
        if fid:
            ids_fournisseurs.append(fid)
            print(f"Fournisseur créé : {f.code} (id={fid})")

    produits = [
        Produit(reference="REF001", designation="Ordinateur portable HP 15", prix_unitaire=350000, stock=25),
        Produit(reference="REF002", designation="Souris sans fil Logitech", prix_unitaire=8500, stock=100),
        Produit(reference="REF003", designation="Clavier mécanique", prix_unitaire=25000, stock=40),
        Produit(reference="REF004", designation="Écran 24 pouces Dell", prix_unitaire=95000, stock=15),
        Produit(reference="REF005", designation="Disque dur externe 1To", prix_unitaire=45000, stock=3),
        Produit(reference="REF006", designation="Imprimante Canon", prix_unitaire=120000, stock=8),
    ]
    ids_produits = []
    for p in produits:
        pid = produit_dao.create(p)
        if pid:
            ids_produits.append(pid)
            print(f"Produit créé : {p.reference} (id={pid})")

    if len(ids_fournisseurs) >= 2 and len(ids_produits) >= 4:
        commande_id_1 = commande_dao.creer_commande(
            "CMD001", ids_fournisseurs[0],
            [(ids_produits[0], 2), (ids_produits[1], 5)],
        )
        print(f"Commande créée : CMD001 (id={commande_id_1})")

        commande_id_2 = commande_dao.creer_commande(
            "CMD002", ids_fournisseurs[1],
            [(ids_produits[2], 3), (ids_produits[3], 1)],
        )
        print(f"Commande créée : CMD002 (id={commande_id_2})")

        if commande_id_2:
            commande_dao.changer_statut(commande_id_2, "VALIDEE")
            commande_dao.changer_statut(commande_id_2, "LIVREE")

    print("Insertion des données de test terminée.")


if __name__ == "__main__":
    inserer_donnees_test()
