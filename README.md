# Projet data engineering E4DSIA
Voici le projet de data engineering que nous avons fait au premier semestre en 4eme année à l'ESIEE Paris.

## Description du Projet
Ce projet consiste en la création d'un site web interactif affichant la liste d'alimennt (anglais), ressencer sur Open Food Fact, et montrer des informations liées à ces mêmes aliments. Les données ont été scrappé depuis l'API publique du site et ont été rajouter sur une base de donnée MongoDB pour, enfin, être mises sur l'application développer en Python.
Le tableau de bord permet de visualiser les données 


## Prérequis Techniques 
* Docker
* MongoDB
* pipenv

# Documentation Fonctionnelle
## Lancement du projet 
Pour pouvoir lancer le projet veuillez suivre les étapes suivantes : 
* Télécharger le repo git comme si dessous puis lancer les dockers: 
```
git clone https://github.com/dinahamadeh-cpu/projet-data_engineering.git
cd projet-data_engineering
docker-compose up --build
```
Les dockers seront lancés de la manière suivante : 
* mongodb fonctionne en premier
* le scraper se lance, rempli la base de donnée 
* une fois l'application se lance pour avoir l'entièreté des données

# Documentation Technique 
Dans cette partie, nous vous expliquerons les choix que nous avons fait tout au long du projet, ainsi que certains détails dans les codes qui semblent important à savoir. 

## Scraping 
Pour ce projet, nous avons choisit de travailler sur le site Openfoodfacts, qui contient une API public. Nous avons donc récuperer les informations depuis l'API public afin d'avoir l'entièreté des informations à disposition pour les produits existant. 

Quels sont les informations que nous avons gardé et pourquoi ? Qu'avons nous décider d'enlever ou garder lors du scraping ? 
| Information gardée | explication | Nettoyage|
|:-------- |:--------:| ------:|
| Nom du produit en anglais   | Nous permet de trier avec les noms de produits écrit dans un alphabet qui n'est pas latin (ex : arabe, cyrilique ...)  | -|
|Category |Nous permets de savoir [...]|Nous allons enlever les tags 'undefined' ainsi que les élèments qui ne sont pas en anglais afin d'avoir une cahérence tout du long du projet|
|Nutriscore| Information intéressante, qui peut être utilisée pour entrainer une IA | Nous avons enlevé les produits sans informations sur le Nutriscore en dehors des produit avec la notion 'not applicable'|
|NOVA group| Voir si il y a un lien avec le nutriscore et les categories | Nous allons enlever les produits avec les mentions 'unknown' |
|greenscore | même explication | Nous ne trions pas les proudits de cette catégorie |

### Fonction de tri et de nettoyage 
