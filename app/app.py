import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="OpenFoodFacts Data", layout="wide")

st.title("OpenFoodFacts - Data Visualization Dashboard")
st.write("This dashboard allows you to explore the data collected from the OpenFoodFacts API.")

@st.cache_resource
def get_data_from_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["openfoodfacts"]
    collection = db["products"]
    data = list(collection.find())
    return data

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
