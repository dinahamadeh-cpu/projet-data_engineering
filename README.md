# Projet data engineering E4DSIA
Voici le projet de data engineering que nous avons fait au premier semestre en 4eme année à l'ESIEE Paris.

Membres du groupes : APPUDURAI Achveiya et HAMADEH Dina

## Description du Projet
Ce projet consiste en la création d'un site web interactif affichant la liste d'alimennt (anglais), ressencer sur Open Food Fact, et montrer des informations liées à ces mêmes aliments. Les données ont été scrappé depuis l'API publique du site et ont été rajouter sur une base de donnée MongoDB pour, enfin, être mises sur l'application développer en Python.
Le tableau de bord permet de visualiser les données 


## Prérequis Techniques 
* Docker
* Docker compose
* MongoDB

# Documentation Fonctionnelle
## Lancement du projet 
Pour pouvoir lancer le projet veuillez suivre les étapes suivantes : textuelle
* Télécharger le repo git comme si dessous puis lancer le docker: 
```
git clone https://github.com/dinahamadeh-cpu/projet-data_engineering.git
cd projet-data_engineering
docker-compose up --build
```
Les dockers seront lancés de la manière suivante : 
* mongodb fonctionne en premier
* le scraper se lance, rempli la base de donnée 
* une fois l'application se lance pour avoir l'entièreté des données

Accès à l'application : `http://localhost:8501/`


# Documentation Technique 
Dans cette partie, nous vous expliquerons les choix que nous avons fait tout au long du projet, ainsi que certains détails dans les codes qui semblent important à savoir. 

## Scraping 
Pour ce projet, nous avons choisit de travailler sur le site Openfoodfacts, qui contient une API public. Nous avons donc récuperer les informations depuis l'API public afin d'avoir l'entièreté des informations à disposition pour les produits existant. 

Quels sont les informations que nous avons gardé et pourquoi ? Qu'avons nous décider d'enlever ou garder lors du scraping ? 
| Information gardée | Explication | Nettoyage|
|:-------- |:--------:| ------:|
| Nom du produit en anglais   | Nous permet de trier avec les noms de produits écrit dans un alphabet qui n'est pas latin (ex : arabe, cyrilique ...)  | suppression des noms vides|
|Category |Nous permets d'analyser les types de produits | Nous allons enlever les tags 'undefined' ainsi que les élèments qui ne sont pas en anglais afin d'avoir une cahérence tout du long du projet|
|Nutriscore| Indicateur nutritionnel clé| Nous avons enlevé les produits sans informations sur le Nutriscore en dehors des produit avec la notion 'not applicable'|
|NOVA group|Niveau de transformation de l'aliment/produit| Nous allons enlever les produits avec les mentions 'unknown' |
|Greenscore | Impact environnemental | Nous ne trions pas les proudits de cette catégorie |

### Fonction de tri et de nettoyage 

Le nettoyage s'effectue directement lors du scrapping de la manière suivante : 
* Suppresion des produits sans nom
* Suppresion des vatégories vides
* Filtrage des Nutriscores valides (a à e)
* Filtrage des NOVA groupe valides (1 à 4)

## Base de données
Nous avons choisi d'utiliser MongoDB pour sa flexibilité de schéma, son utilisation dans le monde professionel ainsi que sa rapidité d'insertion et exploitation. 

## Application web
### Recherche et Filtrage

    Recherche textuelle : Localisation de produits par nom.

    Filtres multicritères :

        Classification nutritionnelle (Nutriscore).

        Degré de transformation des aliments (Groupe NOVA).

        Impact environnemental (Ecoscore).

### Analyses et Visualisations

    Analyses graphiques :

        Histogramme de répartition des Nutriscores.

        Graphique de répartition des groupes NOVA.

        Étude de corrélation entre le niveau de transformation (NOVA) et la qualité nutritionnelle (Nutriscore).

        Analyse de la distribution énergétique (calories).

### Indicateurs Clés (KPI)

    Décompte total des produits filtrés.

    Identification du Nutriscore dominant au sein de la sélection.

    Recensement des produits considérés comme ultra-transformés.
