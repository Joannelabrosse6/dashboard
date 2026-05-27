# 🎬 Projet Final : Analyse de Tendances VOD

## 🎯 Sujet et Problématique Métier
Ce projet vise à analyser les tendances des séries télévisées pour une plateforme de Video On Demand (VOD). L'objectif est d'aider les équipes marketing à cibler leurs prochaines campagnes et recommandations en comprenant quelles séries sont les plus performantes. 

Pour cela, nous combinons des données internes de popularité (fictives, issues de `tv_shows.csv`) avec la note globale attribuée par les spectateurs dans le monde entier (récupérée en temps réel via l'**API publique TVMaze**). Un algorithme attribue ensuite un "Score Marketing" pondéré à chaque série pour guider la stratégie d'acquisition.

## ⚙️ Démarche Technique
Le projet s'articule autour des technologies suivantes :
1. **Base de Données (MySQL)** : Stockage structuré des séries et de leurs genres.
2. **Pipeline de Données (Python & Pandas)** : Lecture des données, nettoyage, requêtes API et calcul de l'algorithme métier.
3. **Dashboard Interactif (Dash & Plotly)** : Visualisation interactive des KPIs et des graphiques.

## 🗄️ Modélisation de la Base de Données
Nous avons opté pour un modèle relationnel permettant de gérer la cardinalité *many-to-many* entre les séries (`movies`) et leurs catégories (`genres`).

![Schéma de la base de données](lien_image_a_remplacer_par_votre_capture_dbdiagram)

## 🚀 Comment lancer le projet ?

### 1. Base de données
Assurez-vous que MySQL est lancé. Importez la structure de la base via le script fourni :
```bash
mysql -u root -p < init_db.sql
```

### 2. Environnement virtuel
Activez l'environnement virtuel et installez les dépendances :
```bash
# Windows
.\venv\Scripts\activate
# Installation des paquets
pip install pandas mysql-connector-python sqlalchemy plotly dash dash-bootstrap-components requests
```

### 3. Lancer le Pipeline
Exécutez le pipeline pour enrichir vos données et peupler la base :
```bash
python pipeline.py
```

### 4. Lancer le Dashboard
Lancez l'interface graphique :
```bash
python dashboard.py
```
