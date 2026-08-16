# Gestion des Commandes Fournisseurs

Application console en Python (POO) permettant à une entreprise sénégalaise
de distribution de matériel informatique de gérer ses fournisseurs, ses
produits et ses commandes, avec une base de données **MySQL**.

## Fonctionnalités

- **Fournisseurs** : CRUD complet, recherche par code ou raison sociale,
  suppression protégée si des commandes sont associées.
- **Produits** : CRUD complet, recherche par désignation, alerte de
  réapprovisionnement (stock sous un seuil), suppression protégée si le
  produit apparaît dans une commande.
- **Commandes** : création avec plusieurs lignes de produits, vérification
  automatique du stock disponible, calcul automatique du montant total,
  mise à jour automatique du stock, changement de statut encadré
  (`EN_ATTENTE → VALIDEE → LIVREE`, jamais en arrière), annulation avec
  restitution du stock.
- **Rapports** : commandes par fournisseur, commandes en attente, valeur
  totale du stock, top 5 des produits les plus commandés, chiffre
  d'affaires total (commandes validées/livrées).

## Architecture

```
gestion_commandes/
├── database/       # Configuration + connexion Singleton
├── models/         # Classes métier (Fournisseur, Produit, Commande, LigneCommande)
├── dao/            # BaseDAO abstraite + DAO spécifiques (héritage)
├── menu/           # Interface console
├── create_tables.py
├── insert_test_data.py
└── main.py
```

### Choix techniques

- **Singleton** (`database/connexion.py`) : une seule instance de connexion
  MySQL est créée et réutilisée dans toute l'application.
- **Héritage** (`dao/base_dao.py`) : `BaseDAO` est une classe abstraite
  (`ABC`) qui définit `get_all`, `get_by_id`, `delete_by_id`. Chaque DAO
  spécifique (`FournisseurDAO`, `ProduitDAO`, `CommandeDAO`) en hérite et
  ajoute ses propres méthodes.
- **Sécurité** : toutes les requêtes SQL sont paramétrées (`%s`), aucune
  concaténation de chaînes avec des données utilisateur.
- **Transactions** : `commit()` / `rollback()` sont utilisés systématiquement,
  en particulier lors de la création d'une commande (insertion de la
  commande + des lignes + mise à jour du stock en une seule transaction).
- **Gestion des erreurs** : chaque opération sensible est encapsulée dans un
  bloc `try/except/finally`.

## Installation

1. Cloner le dépôt et se placer à la racine du projet.

2. Créer un environnement virtuel (recommandé) :
   ```bash
   python -m venv venv
   source venv/bin/activate   # Sous Windows : venv\Scripts\activate
   ```

3. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Créer la base de données MySQL :
   ```sql
   CREATE DATABASE gestion_commandes;
   ```

5. Configurer les identifiants de connexion via des variables d'environnement
   (ou modifier directement `database/config.py`) :
   ```bash
   export DB_HOST=localhost
   export DB_USER=root
   export DB_PASSWORD=votre_mot_de_passe
   export DB_NAME=gestion_commandes
   ```

6. Créer les tables :
   ```bash
   python create_tables.py
   ```

7. (Optionnel) Insérer des données de test :
   ```bash
   python insert_test_data.py
   ```

## Utilisation

Lancer l'application :
```bash
python main.py
```

Un menu principal s'affiche, permettant d'accéder à la gestion des
fournisseurs, des produits, des commandes, et aux rapports.

## Captures d'ecran ### Menu principal !
[Menu principal](screenshots/menu-principal.png)

### Liste des fournisseurs ![Liste des fournisseurs](screenshots/liste-fournisseurs.png) 

### Detail d'une commande ![Detail d'une commande](screenshots/detail-commande.png) 

### Rapport top 5 produits ![Rapport top 5](screenshots/rapport-top5.png)

## Auteurs

Projet réalisé dans le cadre du cours de Programmation - POO & Base de
données, Licence 2 Informatique de Gestion (IAGE), Groupe ISI.
