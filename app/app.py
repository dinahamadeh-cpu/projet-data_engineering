import streamlit as st
from pymongo import MongoClient
import pandas as pd
import os

st.set_page_config(page_title="OpenFoodFacts Data", layout="wide")

st.title("OpenFoodFacts - Data Visualization Dashboard")
st.write("This dashboard allows you to explore the data collected from the OpenFoodFacts API.")

@st.cache_resource
def get_data_from_mongodb():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
    client = MongoClient(MONGO_URI)
    db = client["openfoodfacts_db"]
    collection = db["products_collection"]
    return collection

collection = get_data_from_mongodb()

@st.cache_data
def load_data():
    data = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(data)

df = load_data()

if df.empty:
    st.warning("No data available in the MongoDB collection.")
    st.stop()
    
st.sidebar.header("Filter Options")

search_name = st.sidebar.text_input("Rechercher un produit")

# Filtre Nutriscore
nutriscore_options = sorted(df["nutriscore_grade"].dropna().unique())
selected_nutriscore = st.sidebar.multiselect(
    "Nutriscore",
    nutriscore_options
)

# Filtre NOVA
nova_options = sorted(df["nova_group"].dropna().unique())
selected_nova = st.sidebar.multiselect(
    "NOVA group",
    nova_options
)

# Filtre Ecoscore
ecoscore_options = sorted(df["ecoscore_grade"].dropna().unique())
selected_ecoscore = st.sidebar.multiselect(
    "Ecoscore",
    ecoscore_options
)

# -----------------------
# Application des filtres
# -----------------------
filtered_df = df.copy()

if search_name:
    filtered_df = filtered_df[
        filtered_df["product_name"]
        .str.contains(search_name, case=False, na=False)
    ]

if selected_nutriscore:
    filtered_df = filtered_df[
        filtered_df["nutriscore_grade"].isin(selected_nutriscore)
    ]

if selected_nova:
    filtered_df = filtered_df[
        filtered_df["nova_group"].isin(selected_nova)
    ]

if selected_ecoscore:
    filtered_df = filtered_df[
        filtered_df["ecoscore_grade"].isin(selected_ecoscore)
    ]

# -----------------------
# Résultats
# -----------------------
st.subheader("📊 Résultats")

st.write(f"Nombre de produits affichés : **{len(filtered_df)}**")

st.dataframe(
    filtered_df[
        [
            "product_name",
            "categories_en",
            "nutriscore_grade",
            "nova_group",
            "ecoscore_grade",
        ]
    ],
    use_container_width=True
)
st.subheader("Analyses globales")

st.markdown("### 🥗 Répartition des Nutriscores")
st.caption("Nutriscore A : meilleur score nutritionnel | Nutriscore E : moins bon score nutritionnel")
nutriscore_counts = (
    filtered_df["nutriscore_grade"]
    .value_counts()
    .sort_index()
)
st.bar_chart(nutriscore_counts)

####
st.markdown("### 🧪 Répartition des groupes NOVA")

nova_counts = (
    filtered_df["nova_group"]
    .value_counts()
    .sort_index()
)

st.bar_chart(nova_counts)

