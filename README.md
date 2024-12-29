# Backend Prototype: Flask + NLP Risk Analysis

## Description
Ce projet est un prototype de backend développé avec Flask. Il a pour but de :

- Récupérer et afficher les projets analysés ainsi que les risques associés.
- Intégrer un processus d'intelligence artificielle (NLP) pour analyser les messages provenant d'une API connectée (dans ce cas, un JSON Server pour le prototype).
- Identifier les risques à partir des messages analysés via des techniques de traitement du langage naturel (NLP).

## Fonctionnalités

- **API RESTful avec Flask** :
  - Récupération des données de projets et des risques associés.
  - Endpoint pour analyser les messages API et détecter les risques.

- **Analyse NLP** :
  - Traitement des messages récupérés via une API connectée.
  - Application d'un algorithme basique de traitement du langage naturel pour la recherche de risques.

## Axes d'Amélioration

1. **Optimisation de l'algorithme NLP** :
   - Intégrer un modèle comme **BERT** pour une meilleure compréhension des ontologies et un contexte plus précis.

2. **Optimisation des performances** :
   - Actuellement, le processus NLP consomme trop de ressources, provoquant un **débordement de pile (stack overflow)**.
   - Migrer vers une architecture plus robuste (ex. : Celery pour la gestion asynchrone des tâches ou un serveur spécialisé pour les traitements intensifs).


## Installation et Exécution

### Prérequis
- Python 3.12+
- Flask
- Flask-SQLAlchemy
- Flask-Migration
- Bibliothèques NLP nécessaires : Spacy

### Installation

1. Clonez ce dépôt :
   ```bash
   git clone <url-du-repo>
   cd <nom-du-repo>
   ```

2. Installez les dépendances Python :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez le serveur Flask :
   ```bash
   python app.py
   ```
   
NB : le serveur JSONServer doit être lancé

### Utilisation

1. Accédez aux endpoints disponibles via un outil comme Postman ou cURL.
   - Exemple : Récupération des projets
     ```bash
     curl http://127.0.0.1:5000/projects
     ```

2. Analysez des messages API pour détecter les risques.

## Problèmes Connus

- Le processus NLP est trop gourmand en ressources, ce qui entraîne une saturation des capacités du serveur Flask.
- Limitation de l'architecture Flask pour des traitements intensifs.





