-- Script SQL de création des tables - Gestion des Commandes Fournisseurs

CREATE DATABASE IF NOT EXISTS gestion_commandes;
USE gestion_commandes;

CREATE TABLE IF NOT EXISTS fournisseur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    raison_sociale VARCHAR(150) NOT NULL,
    email VARCHAR(150),
    telephone VARCHAR(30),
    adresse VARCHAR(255),
    date_creation DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS produit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reference VARCHAR(20) NOT NULL UNIQUE,
    designation VARCHAR(150) NOT NULL,
    prix_unitaire DECIMAL(12, 2) NOT NULL CHECK (prix_unitaire > 0),
    stock INT NOT NULL DEFAULT 0 CHECK (stock >= 0),
    date_creation DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE IF NOT EXISTS commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(20) NOT NULL UNIQUE,
    date_commande DATE DEFAULT (CURRENT_DATE),
    fournisseur_id INT NOT NULL,
    montant_total DECIMAL(12, 2) NOT NULL DEFAULT 0,
    statut ENUM('EN_ATTENTE', 'VALIDEE', 'LIVREE', 'ANNULEE') NOT NULL DEFAULT 'EN_ATTENTE',
    date_creation DATE DEFAULT (CURRENT_DATE),
    FOREIGN KEY (fournisseur_id) REFERENCES fournisseur(id)
);

CREATE TABLE IF NOT EXISTS ligne_commande (
    id INT AUTO_INCREMENT PRIMARY KEY,
    commande_id INT NOT NULL,
    produit_id INT NOT NULL,
    quantite INT NOT NULL CHECK (quantite > 0),
    prix_unitaire DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (commande_id) REFERENCES commande(id),
    FOREIGN KEY (produit_id) REFERENCES produit(id)
);
