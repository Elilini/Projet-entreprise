# Projet Algorithmique L2 - Projet entreprise

Ce projet permet de générer un diagnostic stratégique d'entreprise à partir d'un numéro SIREN. 
Le système récupère les données d'identification, analyse le contexte actuel via le web et utilise une IA (Mistral) pour produire un bilan complet.

**Membres du groupe :**

* IDHAYAKUMAR Elilini (44011065)
* YAHYA LABCHIRI Rania (44008335)

---

## 1. Installation

Il faut **Python 3.11.9** installé sur la machine.

Pour l'IA, il faut installer **Ollama**. Une fois l'installation finie, il faut télécharger le modèle Mistral pour que le code puisse l'appeler. Pour ça, ouvrir un terminal (powershell) et taper :
`ollama pull mistral`

---

## 2. Structure du projet et rôle des fichiers

**Dossier backend :**

* **main.py** : C'est le cœur du serveur (FastAPI). Il reçoit le SIREN du frontend et appelle les autres scripts pour regrouper les informations avant de renvoyer le résultat final.
* **sirene.py** : Ce fichier s'occupe de l'extraction des données. Il parcourt le fichier `sirene.csv` pour récupérer le nom et les informations administratives de l'entreprise si elle est dans la base locale.
* **analyse.py** : Ce module définit la manière dont on va analyser l'entreprise. Il va chercher des informations récentes sur le web si besoin et prépare le "prompt" pour que l'IA Mistral sache comment rédiger le diagnostic (santé financière, perspectives 2050).
* **data/sirene.csv** : Le fichier qui contient la base de données des entreprises.

**Dossier frontend :**

* **index.html** et **style.css** : L'interface utilisateur pour afficher le formulaire de recherche et le tableau de bord.
* **script.js** : Il fait le lien avec le backend. Il récupère les données JSON de l'analyse et pilote les graphiques.
* **chart.js** : C'est une bibliothèque JavaScript externe utilisée pour dessiner les graphiques de manière dynamique (courbes de croissance, jauge de santé et barres de pollution CO2).

---

## 3. Comment lancer le projet

### Étape 1 : Préparer l'environnement

Ouvrir un terminal powershell dans le dossier du projet et taper :

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install fastapi uvicorn requests duckduckgo_search

```

### Étape 2 : Lancer le serveur

Pour lancer ou relancer le serveur rapidement :

```powershell
.\venv\Scripts\activate
cd backend
python main.py

```

*Le serveur sera actif sur [http://127.0.0.1:8000](http://127.0.0.1:8000).*

### Étape 3 : Lancer l'interface

Ouvrir le fichier `frontend/index.html` dans un navigateur. On saisit un SIREN et on lance l'analyse.

---

## 4. Précisions supplémentaires

Si le SIREN n'est pas trouvé dans le fichier CSV, le script `analyse.py` bascule automatiquement sur une recherche via l'API DuckDuckGo pour ne pas bloquer l'utilisateur.
Le diagnostic est généré en temps réel par Mistral via Ollama.

