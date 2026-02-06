import requests
import time
from pymongo import MongoClient
import os

page_number = 1
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27018/")
client = MongoClient(MONGO_URI)
db = client['openfoodfacts_db']
collection = db['products_collection']

for page_number in range(1, 201):
    url = "https://world.openfoodfacts.org/api/v2/search?&fields=product_name_en,categories_tags_en,nutriscore_grade,nova_group,ecoscore_grade&page_size=40&page={page_number}"
    
    response = requests.get(url.format(page_number=page_number))
    
    if response.status_code != 200:
        print(f"Erreur lors de la récupération des données à la page : {page_number} + {response.status_code}")
        break
    try: 
        data = response.json()
    except ValueError:
        print(f"Erreur lors de la conversion des données en JSON à la page : {page_number}")
        break
    
    produits = data['products']
    valid_products_count = 0
    if produits == []:
        break
    
    
    for product in produits:
        
        nutriscore = None
        NOVA_group = None
        green_score = None
        
        product_name = product.get("product_name_en", "").strip()
        if not product_name:
            continue
        
        categories_en = [
            cat.replace("-", " ")
            for cat in product.get("categories_tags_en", [])
            if cat and cat != "unknown"
        ]

        if not categories_en:
            continue

        if 'nutriscore_grade' not in product:
            continue
        if product['nutriscore_grade']  in ["a", "b", "c", "d", "e", "not-applicable"]:
            nutriscore = product['nutriscore_grade'].lower() 
                
        if 'nova_group' not in product:
            continue
        if product['nova_group']  in [1, 2, 3, 4]:
            NOVA_group = product['nova_group']
            
        if 'ecoscore_grade' not in product:
            continue
        green_score = product['ecoscore_grade']
        
        produit_dict={
            'product_name': product_name,
            'categories_en': categories_en,
            'nutriscore_grade': nutriscore,
            'nova_group': NOVA_group,
            'ecoscore_grade': green_score
        }
        collection.update_one(
            {'product_name': product_name},
            {'$set': {
                'categories_en': categories_en,
                'nutriscore_grade': nutriscore,
                'nova_group': NOVA_group,
                'ecoscore_grade': green_score
            }},
            upsert=True
        )
        valid_products_count += 1


    print(f"Page {page_number} : {valid_products_count} produits valides")    
    time.sleep(2)  
