# Projet data engineering E4DSIA
Voici le projet de data engineering que nous avons fait au premier semestre en 4eme année à l'ESIEE Paris.

## Description du Projet
Ce projet consiste en la création d'un site web interactif affichant la liste d'alimennt (anglais), ressencer sur Open Food Fact, et montrer des informations liées à ces mêmes aliments. Les données ont été scrappé depuis l'API publique du site et ont été rajouter sur une base de donnée MongoDB pour, enfin, être mises sur l'application développer en Python.
Le tableau de bord pert de : 
* on verra plus tard 

## Prérequis Techniques 
* Docker
* MongoDB
* pipenv

# Documentation Fonctionnelle
## Lancement du projet 
Pour pouvoir lancer le projet veuillez suivre les étapes suivantes : 
* Télécharger le repo git comme si dessous  : 
```
git clone https://github.com/dinahamadeh-cpu/projet-data_engineering.git
cd projet-data_engineering
```
* Activer l'environnement virtuel :
```
pipenv install
pipenv shell
```

* Si vous souhaitez lancer le scrapping du site Open food Fact, lancer le document scrapper.py depuis le terminal. Ici, le scrapping a déjà été réalisé dans le dossier. 
* Nettoyage
* Lancer MongoDB avec Docker : 


# Documentation Technique 
Dans cette partie, nous vous expliquerons les choix que nous avons fait tout au long du projet, ainsi que certains détails dans les codes qui semblent important à savoir. 