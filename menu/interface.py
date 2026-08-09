"""Interface utilisateur en ligne de commande."""

from dao.fournisseur_dao import FournisseurDAO
from dao.produit_dao import ProduitDAO
from dao.commande_dao import CommandeDAO
from models.fournisseur import Fournisseur
from models.produit import Produit


# ----------------------------------------------------------------------
# Fonctions utilitaires de saisie sécurisée
# ----------------------------------------------------------------------
def saisir_entier(message, min_valeur=None):
    while True:
        valeur = input(message).strip()
        try:
            entier = int(valeur)
            if min_valeur is not None and entier < min_valeur:
                print(f"La valeur doit être supérieure ou égale à {min_valeur}.")
                continue
            return entier
        except ValueError:
            print("Veuillez saisir un nombre entier valide.")


def saisir_decimal(message, min_valeur=None):
    while True:
        valeur = input(message).strip()
        try:
            decimal = float(valeur)
            if min_valeur is not None and decimal <= min_valeur:
                print(f"La valeur doit être strictement supérieure à {min_valeur}.")
                continue
            return decimal
        except ValueError:
            print("Veuillez saisir un nombre valide.")


def saisir_texte(message, obligatoire=True):
    while True:
        valeur = input(message).strip()
        if obligatoire and not valeur:
            print("Ce champ est obligatoire.")
            continue
        return valeur


class Interface:
    """Menu principal de l'application console."""

    def __init__(self):
        self.fournisseur_dao = FournisseurDAO()
        self.produit_dao = ProduitDAO()
        self.commande_dao = CommandeDAO()

    def lancer(self):
        while True:
            print("\n" + "=" * 50)
            print("  GESTION DES COMMANDES FOURNISSEURS")
            print("=" * 50)
            print("1. Gestion des fournisseurs")
            print("2. Gestion des produits")
            print("3. Gestion des commandes")
            print("4. Rapports et statistiques")
            print("0. Quitter")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                self.menu_fournisseurs()
            elif choix == "2":
                self.menu_produits()
            elif choix == "3":
                self.menu_commandes()
            elif choix == "4":
                self.menu_rapports()
            elif choix == "0":
                print("Au revoir !")
                break
            else:
                print("Choix invalide.")

    # ------------------------------------------------------------------
    # FOURNISSEURS
    # ------------------------------------------------------------------
    def menu_fournisseurs(self):
        while True:
            print("\n--- Gestion des fournisseurs ---")
            print("1. Ajouter un fournisseur")
            print("2. Lister les fournisseurs")
            print("3. Afficher un fournisseur (par id ou code)")
            print("4. Modifier un fournisseur")
            print("5. Supprimer un fournisseur")
            print("6. Rechercher un fournisseur")
            print("0. Retour")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                self.ajouter_fournisseur()
            elif choix == "2":
                self.lister_fournisseurs()
            elif choix == "3":
                self.afficher_fournisseur()
            elif choix == "4":
                self.modifier_fournisseur()
            elif choix == "5":
                self.supprimer_fournisseur()
            elif choix == "6":
                self.rechercher_fournisseur()
            elif choix == "0":
                break
            else:
                print("Choix invalide.")

    def ajouter_fournisseur(self):
        code = saisir_texte("Code (ex: F001) : ")
        if self.fournisseur_dao.get_by_code(code):
            print("Ce code existe déjà.")
            return
        raison_sociale = saisir_texte("Raison sociale : ")
        email = saisir_texte("Email : ", obligatoire=False)
        telephone = saisir_texte("Téléphone : ", obligatoire=False)
        adresse = saisir_texte("Adresse : ", obligatoire=False)
        f = Fournisseur(code=code, raison_sociale=raison_sociale,
                         email=email, telephone=telephone, adresse=adresse)
        fid = self.fournisseur_dao.create(f)
        if fid:
            print(f"Fournisseur créé avec succès (id={fid}).")

    def lister_fournisseurs(self):
        fournisseurs = self.fournisseur_dao.get_all()
        if not fournisseurs:
            print("Aucun fournisseur enregistré.")
        for f in fournisseurs:
            print(f"({f.id}) {f}")

    def afficher_fournisseur(self):
        cle = saisir_texte("ID ou code du fournisseur : ")
        fournisseur = None
        if cle.isdigit():
            fournisseur = self.fournisseur_dao.get_by_id(int(cle))
        if fournisseur is None:
            fournisseur = self.fournisseur_dao.get_by_code(cle)
        if fournisseur is None:
            print("Fournisseur introuvable.")
            return
        print(fournisseur)
        print(f"Adresse : {fournisseur.adresse}")
        print(f"Date de création : {fournisseur.date_creation}")

    def modifier_fournisseur(self):
        id_ = saisir_entier("ID du fournisseur à modifier : ")
        fournisseur = self.fournisseur_dao.get_by_id(id_)
        if fournisseur is None:
            print("Fournisseur introuvable.")
            return
        print("Laissez vide pour conserver la valeur actuelle.")
        nouvelle_raison = input(f"Raison sociale [{fournisseur.raison_sociale}] : ").strip()
        nouvel_email = input(f"Email [{fournisseur.email}] : ").strip()
        nouveau_tel = input(f"Téléphone [{fournisseur.telephone}] : ").strip()
        nouvelle_adresse = input(f"Adresse [{fournisseur.adresse}] : ").strip()

        fournisseur.raison_sociale = nouvelle_raison or fournisseur.raison_sociale
        fournisseur.email = nouvel_email or fournisseur.email
        fournisseur.telephone = nouveau_tel or fournisseur.telephone
        fournisseur.adresse = nouvelle_adresse or fournisseur.adresse

        if self.fournisseur_dao.update(fournisseur):
            print("Fournisseur mis à jour avec succès.")

    def supprimer_fournisseur(self):
        id_ = saisir_entier("ID du fournisseur à supprimer : ")
        if self.fournisseur_dao.a_des_commandes(id_):
            print("Impossible : ce fournisseur a des commandes associées.")
            return
        confirmation = input("Confirmer la suppression (o/n) : ").strip().lower()
        if confirmation == "o":
            if self.fournisseur_dao.delete_by_id(id_):
                print("Fournisseur supprimé.")

    def rechercher_fournisseur(self):
        mot_cle = saisir_texte("Mot-clé (code ou raison sociale) : ")
        resultats = self.fournisseur_dao.rechercher(mot_cle)
        if not resultats:
            print("Aucun résultat.")
        for f in resultats:
            print(f"({f.id}) {f}")

    # ------------------------------------------------------------------
    # PRODUITS
    # ------------------------------------------------------------------
    def menu_produits(self):
        while True:
            print("\n--- Gestion des produits ---")
            print("1. Ajouter un produit")
            print("2. Lister les produits")
            print("3. Afficher un produit (par id ou référence)")
            print("4. Modifier un produit")
            print("5. Supprimer un produit")
            print("6. Rechercher par désignation")
            print("7. Alerte réapprovisionnement (stock sous un seuil)")
            print("0. Retour")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                self.ajouter_produit()
            elif choix == "2":
                self.lister_produits()
            elif choix == "3":
                self.afficher_produit()
            elif choix == "4":
                self.modifier_produit()
            elif choix == "5":
                self.supprimer_produit()
            elif choix == "6":
                self.rechercher_produit()
            elif choix == "7":
                self.alerte_stock()
            elif choix == "0":
                break
            else:
                print("Choix invalide.")

    def ajouter_produit(self):
        reference = saisir_texte("Référence (ex: REF001) : ")
        if self.produit_dao.get_by_reference(reference):
            print("Cette référence existe déjà.")
            return
        designation = saisir_texte("Désignation : ")
        prix = saisir_decimal("Prix unitaire : ", min_valeur=0)
        stock = saisir_entier("Stock initial : ", min_valeur=0)
        p = Produit(reference=reference, designation=designation,
                    prix_unitaire=prix, stock=stock)
        pid = self.produit_dao.create(p)
        if pid:
            print(f"Produit créé avec succès (id={pid}).")

    def lister_produits(self):
        produits = self.produit_dao.get_all()
        if not produits:
            print("Aucun produit enregistré.")
        for p in produits:
            print(f"({p.id}) {p}")

    def afficher_produit(self):
        cle = saisir_texte("ID ou référence du produit : ")
        produit = None
        if cle.isdigit():
            produit = self.produit_dao.get_by_id(int(cle))
        if produit is None:
            produit = self.produit_dao.get_by_reference(cle)
        if produit is None:
            print("Produit introuvable.")
            return
        print(produit)

    def modifier_produit(self):
        id_ = saisir_entier("ID du produit à modifier : ")
        produit = self.produit_dao.get_by_id(id_)
        if produit is None:
            print("Produit introuvable.")
            return
        print("Laissez vide pour conserver la valeur actuelle.")
        nouvelle_designation = input(f"Désignation [{produit.designation}] : ").strip()
        nouveau_prix = input(f"Prix unitaire [{produit.prix_unitaire}] : ").strip()
        nouveau_stock = input(f"Stock [{produit.stock}] : ").strip()

        produit.designation = nouvelle_designation or produit.designation
        produit.prix_unitaire = float(nouveau_prix) if nouveau_prix else produit.prix_unitaire
        produit.stock = int(nouveau_stock) if nouveau_stock else produit.stock

        if self.produit_dao.update(produit):
            print("Produit mis à jour avec succès.")

    def supprimer_produit(self):
        id_ = saisir_entier("ID du produit à supprimer : ")
        if self.produit_dao.est_dans_une_commande(id_):
            print("Impossible : ce produit apparaît dans une commande.")
            return
        confirmation = input("Confirmer la suppression (o/n) : ").strip().lower()
        if confirmation == "o":
            if self.produit_dao.delete_by_id(id_):
                print("Produit supprimé.")

    def rechercher_produit(self):
        mot_cle = saisir_texte("Mot-clé (désignation) : ")
        resultats = self.produit_dao.rechercher_par_designation(mot_cle)
        if not resultats:
            print("Aucun résultat.")
        for p in resultats:
            print(f"({p.id}) {p}")

    def alerte_stock(self):
        seuil = saisir_entier("Seuil d'alerte : ", min_valeur=0)
        produits = self.produit_dao.produits_sous_seuil(seuil)
        if not produits:
            print("Aucun produit sous ce seuil.")
        for p in produits:
            print(f"({p.id}) {p}  -- ALERTE STOCK BAS")

    # ------------------------------------------------------------------
    # COMMANDES
    # ------------------------------------------------------------------
    def menu_commandes(self):
        while True:
            print("\n--- Gestion des commandes ---")
            print("1. Créer une commande")
            print("2. Lister toutes les commandes")
            print("3. Afficher le détail d'une commande")
            print("4. Changer le statut d'une commande")
            print("5. Annuler une commande")
            print("6. Supprimer une commande")
            print("0. Retour")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                self.creer_commande()
            elif choix == "2":
                self.lister_commandes()
            elif choix == "3":
                self.detail_commande()
            elif choix == "4":
                self.changer_statut_commande()
            elif choix == "5":
                self.annuler_commande()
            elif choix == "6":
                self.supprimer_commande()
            elif choix == "0":
                break
            else:
                print("Choix invalide.")

    def creer_commande(self):
        numero = saisir_texte("Numéro de commande (ex: CMD003) : ")

        fid = saisir_entier("ID du fournisseur : ")
        if self.fournisseur_dao.get_by_id(fid) is None:
            print("Fournisseur introuvable.")
            return

        lignes = []
        print("Ajout des produits à la commande (laissez l'ID vide pour terminer).")
        while True:
            self.lister_produits()
            cle = input("ID du produit à ajouter (vide pour terminer) : ").strip()
            if not cle:
                break
            if not cle.isdigit():
                print("ID invalide.")
                continue
            produit_id = int(cle)
            if self.produit_dao.get_by_id(produit_id) is None:
                print("Produit introuvable.")
                continue
            quantite = saisir_entier("Quantité : ", min_valeur=1)
            lignes.append((produit_id, quantite))

        if not lignes:
            print("Commande annulée : aucun produit ajouté.")
            return

        commande_id = self.commande_dao.creer_commande(numero, fid, lignes)
        if commande_id:
            print(f"Commande créée avec succès (id={commande_id}).")

    def lister_commandes(self):
        commandes = self.commande_dao.get_all()
        if not commandes:
            print("Aucune commande enregistrée.")
        for c in commandes:
            print(f"({c.id}) {c}")

    def detail_commande(self):
        id_ = saisir_entier("ID de la commande : ")
        commande = self.commande_dao.get_detail(id_)
        if commande is None:
            print("Commande introuvable.")
            return
        print(f"\nCommande {commande.numero} - Statut : {commande.statut}")
        print(f"Montant total : {commande.montant_total} FCFA")
        print("Produits :")
        for ligne in commande.lignes:
            print(f"  - {ligne.designation} ({ligne.reference}) "
                  f"x{ligne.quantite} @ {ligne.prix_unitaire} = {ligne.sous_total} FCFA")

    def changer_statut_commande(self):
        id_ = saisir_entier("ID de la commande : ")
        print("Statuts possibles : EN_ATTENTE, VALIDEE, LIVREE")
        nouveau_statut = saisir_texte("Nouveau statut : ").upper()
        if self.commande_dao.changer_statut(id_, nouveau_statut):
            print("Statut mis à jour avec succès.")

    def annuler_commande(self):
        id_ = saisir_entier("ID de la commande à annuler : ")
        if self.commande_dao.annuler_commande(id_):
            print("Commande annulée, stock restitué.")

    def supprimer_commande(self):
        id_ = saisir_entier("ID de la commande à supprimer : ")
        confirmation = input("Confirmer la suppression (o/n) : ").strip().lower()
        if confirmation == "o":
            if self.commande_dao.delete_by_id(id_):
                print("Commande supprimée.")

    # ------------------------------------------------------------------
    # RAPPORTS
    # ------------------------------------------------------------------
    def menu_rapports(self):
        while True:
            print("\n--- Rapports et statistiques ---")
            print("1. Commandes par fournisseur")
            print("2. Commandes en attente de validation")
            print("3. Valeur totale du stock")
            print("4. Top 5 des produits les plus commandés")
            print("5. Chiffre d'affaires total")
            print("0. Retour")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                fid = saisir_entier("ID du fournisseur : ")
                for c in self.commande_dao.get_by_fournisseur(fid):
                    print(f"({c.id}) {c}")
            elif choix == "2":
                for c in self.commande_dao.get_par_statut("EN_ATTENTE"):
                    print(f"({c.id}) {c}")
            elif choix == "3":
                produits = self.produit_dao.get_all()
                valeur_totale = sum(p.prix_unitaire * p.stock for p in produits)
                print(f"Valeur totale du stock : {valeur_totale} FCFA")
            elif choix == "4":
                for ligne in self.commande_dao.top_5_produits():
                    print(f"{ligne['designation']} ({ligne['reference']}) "
                          f"- {ligne['total_quantite']} unités commandées")
            elif choix == "5":
                ca = self.commande_dao.chiffre_affaires_total()
                print(f"Chiffre d'affaires total (commandes validées/livrées) : {ca} FCFA")
            elif choix == "0":
                break
            else:
                print("Choix invalide.")
