import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

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

# Splitting the data
st.subheader("Splitting Data")

# Add code for splitting the data into train and test sets here
X = ise_preprocessed.drop("amount_local_currency", axis=1)
y = ise_preprocessed["amount_local_currency"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Display the sizes of train and test sets
st.write("Size of Train Set:", X_train.shape[0])
st.write("Size of Test Set:", X_test.shape[0])

# Regression and Model Evaluation
st.subheader("Regression and Model Evaluation")

# Add your regression model and evaluation code here

# Display confusion matrix
st.write("Confusion Matrix:")
st.write("Confusion matrix visualizations can be added here.")

# Display model evaluation metrics (accuracy, precision, recall)
st.write("Model Evaluation Metrics:")
st.write("Accuracy:")
st.write("Precision:")
st.write("Recall:")

# Visualize additional results and insights as needed

# You can add more Streamlit components, visualizations, and interactive elements as required.
