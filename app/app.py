import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px 
import os

st.set_page_config(page_title="OpenFoodFacts Pro", layout="wide", page_icon="🥗")

st.markdown("""
    <style>
    /* Fond principal sombre */
    .main { background-color: #0e1117; color: #fafafa; }
    
    /* Cartes de métriques style néon/glassmorphism */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s ease-in-out;
    }
    
    /* Petit effet de survol sur les métriques */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #58a6ff;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_collection():
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
    client = MongoClient(MONGO_URI)
    return client["openfoodfacts_db"]["products_collection"]

@st.cache_data
def load_data():
    collection = get_collection()
    fields = {
        "_id": 0, "product_name": 1, "categories_en": 1, 
        "nutriscore_grade": 1, "nova_group": 1, "ecoscore_grade": 1, 
        "image_url": 1, "energy_100g": 1
    }
    data = list(collection.find({}, fields))
    return pd.DataFrame(data)

df = load_data()

st.sidebar.title(" Filtres")
search_name = st.sidebar.text_input("Rechercher un produit", placeholder="ex: Granola")

with st.sidebar.expander("Scores & Grades", expanded=True):
    selected_nutriscore = st.multiselect("Nutriscore", sorted(df["nutriscore_grade"].dropna().unique()))
    selected_nova = st.multiselect("Groupe NOVA", sorted(df["nova_group"].dropna().unique()))
    selected_ecoscore = st.multiselect("Ecoscore", sorted(df["ecoscore_grade"].dropna().unique()))

filtered_df = df.copy()
if search_name:
    filtered_df = filtered_df[filtered_df["product_name"].str.contains(search_name, case=False, na=False)]
if selected_nutriscore:
    filtered_df = filtered_df[filtered_df["nutriscore_grade"].isin(selected_nutriscore)]
if selected_nova:
    filtered_df = filtered_df[filtered_df["nova_group"].isin(selected_nova)]
if selected_ecoscore:
    filtered_df = filtered_df[filtered_df["ecoscore_grade"].isin(selected_ecoscore)]

st.title(" OpenFoodFacts Insights")

col1, col2, col3 = st.columns(3)
col1.metric("Produits filtrés", len(filtered_df))
col2.metric("Nutriscore Moyen", filtered_df["nutriscore_grade"].mode()[0].upper() if not filtered_df.empty else "N/A")
col3.metric("Ultra-transformés (NOVA 4)", f"{len(filtered_df[filtered_df['nova_group'] == 4])}")

tab1, tab2, tab3 = st.tabs([" Données", " Analyses Graphiques", " Focus Nutriments"])

with tab1:
    st.subheader("Liste des produits")
    st.dataframe(filtered_df, use_container_width=True)

with tab2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("###  Répartition Nutriscore")
        color_map = {'a': '#038141', 'b': '#85BB2F', 'c': '#FECB02', 'd': '#EE8100', 'e': '#E63E11'}
        fig_nutri = px.histogram(filtered_df, x="nutriscore_grade", 
                               category_orders={"nutriscore_grade": ["a", "b", "c", "d", "e"]},
                               color="nutriscore_grade", color_discrete_map=color_map)
        st.plotly_chart(fig_nutri, use_container_width=True)

    with col_b:
        st.markdown("###  Répartition NOVA")
        fig_nova = px.pie(filtered_df, names="nova_group", hole=0.4, title="Proportion des groupes NOVA")
        st.plotly_chart(fig_nova, use_container_width=True)

with tab3:
    st.markdown("###  Nutriscore vs NOVA")
    fig_scatter = px.box(filtered_df, x="nutriscore_grade", y="nova_group", 
                         color="nutriscore_grade", color_discrete_map=color_map,
                         category_orders={"nutriscore_grade": ["a", "b", "c", "d", "e"]})
    st.plotly_chart(fig_scatter, use_container_width=True)