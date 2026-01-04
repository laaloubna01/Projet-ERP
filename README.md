
Module Odoo 17 pour la gestion complète des formations universitaires : inscriptions, formateurs, ressources pédagogiques et workflow de validation.
Fonctionnalités:

 -Création et planification des formations
 -Gestion des formateurs et participants
 -Centralisation des documents pédagogiques
 -Workflow de validation (Brouillon → Planifié → En cours → Terminé)
 -Vues multiples (Liste, Formulaire, Kanban)
 -Recherche et filtrage avancés

Technologies:

-Odoo 17.0
-Python 3.10+
-PostgreSQL 16
-Docker Latest

Prérequis:

Docker Desktop installé
4 GB RAM minimum
10 GB d'espace disque

Installation:

Cloner le projet

bashgit clone <url-du-repo>
cd gestion_formation

Démarrer les conteneurs

bashdocker-compose up -d

Accéder à Odoo


URL : http://localhost:8069
Email : admin
Mot de passe : admin


Installer le module:


Menu Apps → Rechercher "Gestion des Formations"
Cliquer sur Installer

📁 Structure du Projet
gestion_formations/
├── models/          # Modèles de données (Python)
├── views/           # Interfaces utilisateur (XML)
├── security/        # Droits d'accès
├── data/            # Données initiales
└── __manifest__.py  # Configuration du module
💡 Utilisation

Créer une formation : Menu Formations → Nouveau
Ajouter des formateurs : Onglet "Formateurs"
Gérer les inscrits : Onglet "Inscrits"
Uploader des documents : Onglet "Documents"
Suivre le workflow : Boutons en haut du formulaire

Aperçu:

Vue Liste : Tableau récapitulatif de toutes les formations
Vue Formulaire : Détails complets avec onglets
Vue Kanban : Organisation par statut
