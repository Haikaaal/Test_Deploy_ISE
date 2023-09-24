import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# Load the data
@st.cache
def load_data():
    ise = pd.read_csv("average_hourly_earnings_of_female_and_male_employees_(managers)_local_currency.csv", sep=',')
    return ise

ise = load_data()

# Streamlit app
st.title("MiniProject ISE Data Analysis")

# Display the loaded data
st.subheader("Data Overview")
st.dataframe(ise)

# Data Cleaning
st.subheader("Data Cleaning")
columns_to_drop = ["Unnamed: 0", "gender", "gender_code"]
ise = ise.drop(columns=columns_to_drop)
st.write("Data after dropping unnecessary columns:")
st.dataframe(ise)

# Missing Data
st.subheader("Missing Data")
missing_data = ise.isnull().sum()
st.write("Missing Data Count:")
st.write(missing_data)

# Outlier Analysis (you can add visualizations here)
st.subheader("Outlier Analysis")
st.write("Visualizations of outliers per country can be added here.")

# Data Preprocessing
st.subheader("Data Preprocessing")

# Feature selection and preprocessing can be added here
# For simplicity, we'll use a subset of columns for demonstration
selected_features = ["country", "year", "amount_local_currency"]
ise_preprocessed = ise[selected_features]

# Splitting the data (if necessary)
# You can split the data manually without using scikit-learn

# Display regression or modeling results (if not using scikit-learn)
# You can focus on data exploration and visualization instead

# Visualize additional results and insights as needed

# You can add more Streamlit components, visualizations, and interactive elements as required.
