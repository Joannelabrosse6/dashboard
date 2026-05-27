# Script de Soutenance : Projet Analyse VOD

*(Ce document te sert de guide étape par étape pour ta présentation en distanciel.)*

## 1. La Problématique Métier
"Bonjour à tous. Pour ce projet final, j'ai décidé de travailler sur l'analyse de données pour une plateforme de VOD. 
L'enjeu métier est simple : pour qu'une équipe marketing puisse cibler efficacement ses campagnes (newsletters, recommandations), elle a besoin de savoir quelles sont les séries les plus performantes. 
J'ai donc croisé des données de popularité internes avec les notes mondiales des spectateurs, récupérées en temps réel via l'API publique de TVMaze, pour générer un 'Score Marketing' pondéré."

## 2. Le Schéma de la Base et les Choix de Modélisation
*(Affiche la capture d'écran de ton schéma dbdiagram ici)*

"Pour stocker ces informations proprement, j'ai modélisé une base de données MySQL.
Le cœur de la structure est une relation **Many-to-Many** entre les Séries (table `movies`) et les Genres (table `genres`). 
J'ai donc créé une table de jointure `movie_genres`. Cela permet de respecter les standards de modélisation : une série peut avoir plusieurs genres (Action, Drame) et un genre peut appartenir à plusieurs séries. J'ai ajouté des contraintes `FOREIGN KEY` avec un `ON DELETE CASCADE` pour assurer l'intégrité de mes données."

## 3. Démo du Dashboard
*(Partage ton écran sur la fenêtre du navigateur http://127.0.0.1:8050)*

"Voici l'interface utilisateur que j'ai développée avec **Dash (Plotly)**. 
J'ai choisi Dash pour sa puissance de personnalisation et sa gestion précise des callbacks réactifs.
En haut, j'ai implémenté un filtre interactif pour sélectionner les plateformes de VOD. 
-> *Observez comment les trois graphiques se mettent à jour instantanément :*
1. Le premier montre le **Top 10 des séries** selon la note globale récupérée par l'API.
2. Le deuxième illustre la **distribution des genres** dans notre catalogue.
3. Le graphique de dispersion en bas permet de visualiser le rapport entre l'année de sortie et la note, avec la taille des points représentant le score de popularité interne."

## 4. Code Intéressant (Focus Technique)
*(Affiche ton fichier `dashboard.py` ou `pipeline.py`)*

"D'un point de vue technique, j'aimerais mettre en valeur l'intégration de **Dash avec SQLAlchemy**. 
Pour assurer la stabilité des échanges entre Python et MySQL, j'utilise un moteur SQLAlchemy. Cela permet à Pandas de lire les données proprement tout en respectant les standards de sécurité et de performance actuels.

Côté Python, j'ai aussi construit l'algorithme qui calcule le fameux Score Marketing. Il gère intelligemment les données manquantes et utilise des clauses `ON DUPLICATE KEY UPDATE` pour maintenir la base de données à jour sans créer de doublons."

*(Fin de présentation, questions/réponses)*
