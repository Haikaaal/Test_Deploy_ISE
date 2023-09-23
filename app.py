# -*- coding: utf-8 -*-
"""MiniProject ISE!

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wV9sn9v0HxTe3kWQipcQW3Cp933-QWYD

#1. Import Library and Connect to Your Google Drive
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score

"""#2. Load Data and finding information"""

ise = pd.read_csv("average_hourly_earnings_of_female_and_male_employees_(managers)_local_currency.csv", sep=',')

ise

ise.info()

"""Pada saat penggalian data, kita menemukan masalah yaitu beberapa variabel yang bermasalah dijadikan parameter, variabel yang kami maksudkan adalah :


*   Variabel gender yang tidak lengkap pada tiap negara

*   Variabel tahun beberapa negara tidak mempunyai tahun yang lengkap sehingga tidak valid jika dibandingkan dengan negara lain

* Outlier pada data tidak perlu dilakukan karena data membicarakan average earning per hour based on their local currency

#3. Data Cleaning
"""

columns_to_drop = ["Unnamed: 0", "gender", "gender_code"]
ise = ise.drop(columns=columns_to_drop)

ise

ise.info()

"""#4. Missing Data"""

ise.info()

"""#5. Outlier in the Data

Outlier tidak perlu dilakukan karena data yang dibicarakan adalah data tentang penghasilan per jamnya dan dituliskan pada currency negara masing2. Namun, untuk memastikan lagi dapat kita filtrasi terlebih dan tampilkan terlebih dahulu visualisasinya per negara
"""

# Get a list of unique countries from the 'country' column
unique_countries = ise['country'].unique()

# Create a boxplot for the "amount_local_currency" for each country
for country in unique_countries:
    # Filter the DataFrame for the specific country
    country_data = ise[ise['country'] == country]

    # Extract the "amount_local_currency" data for the country
    country_amount = country_data['amount_local_currency']

    # Create a boxplot for the "amount_local_currency" of that country
    plt.figure(figsize=(8, 4))  # Adjust the figure size if needed
    plt.boxplot(country_amount, vert=False)

    # Set the title and labels
    plt.title(f'Boxplot for {country} - Amount in Local Currency')
    plt.xlabel('Amount in Local Currency')

    # Display the boxplot
    plt.show()

"""Ternyata, setelah dilihat lagi dapat ditemukan negara negara yang masih mempunyai outlier, negara yang dimaksud adalah :

Belgium
Israel
US
Serbia
Bosnia
Turkiye
Uzbekistan
North Macedonia
Greece
Montenegro
Slovenia
Portugal
Switzerland
France
"""

import math

# List of countries to filter
countries_to_filter = ['Belgium', 'Israel', 'United States', 'Serbia', 'Bosnia and Herzegovina', 'TÃ¼rkiye', 'Uzbekistan', 'North Macedonia', 'Greece', 'Montenegro', 'Slovenia', 'Portugal', 'Switzerland', 'France']

# Calculate the number of rows and columns for the grid
num_countries = len(countries_to_filter)
num_columns = 3  # Number of columns in the grid
num_rows = math.ceil(num_countries / num_columns)

# Create subplots for the grid
fig, axes = plt.subplots(num_rows, num_columns, figsize=(12, 8))
axes = axes.flatten()  # Flatten the axes for easier iteration

# Filter the DataFrame for the specified countries and create boxplots
for i, country in enumerate(countries_to_filter):
    # Filter the DataFrame for the specific country
    country_data = ise[ise['country'] == country]

    # Extract the "amount_local_currency" data for the country
    country_amount = country_data['amount_local_currency']

    # Create a boxplot for the "amount_local_currency" of that country on the appropriate subplot
    ax = axes[i]
    ax.boxplot(country_amount, vert=False)
    ax.set_title(f'{country} - Amount in Local Currency')
    ax.set_xlabel('Amount in Local Currency')

# Remove any empty subplots
for i in range(num_countries, num_rows * num_columns):
    fig.delaxes(axes[i])

# Adjust layout and display the grid of boxplots
plt.tight_layout()
plt.show()

"""Cek distribusi normal atau tidak"""

from scipy.stats import skew

# Create a dictionary to store skewness and skewness interpretation for each country
skewness_info = {}

# Filter the DataFrame for the specified countries and calculate skewness
for country in countries_to_filter:
    # Filter the DataFrame for the specific country
    country_data = ise[ise['country'] == country]

    # Extract the "amount_local_currency" data for the country
    country_amount = country_data['amount_local_currency']

    # Calculate the skewness
    skew_value = skew(country_amount)

    # Determine the interpretation based on the range
    if -0.5 <= skew_value <= 0.5:
        skew_interpretation = "Normal"
    else:
        skew_interpretation = "Skewed"

    # Store skewness and interpretation in the dictionary
    skewness_info[country] = {
        "Skewness": skew_value,
        "Interpretation": skew_interpretation
    }

# Print skewness information for each country
for country, info in skewness_info.items():
    skew_value = info["Skewness"]
    interpretation = info["Interpretation"]
    print(f'{country}: Skewness = {skew_value:.2f}, Interpretation = {interpretation}')

# Function to find upper and lower boundaries for normally distributed variables
# Calculate the boundaries outside which sit the outliers for a Gaussian distribution

def find_normal_boundaries(ise, variable):
    upper_boundary = ise[variable].mean() + 3 * ise[variable].std()
    lower_boundary = ise[variable].mean() - 3 * ise[variable].std()

    return upper_boundary, lower_boundary

upper_boundary_age, lower_boundary_age = find_normal_boundaries(ise[(ise['country'] == 'Armenia')], 'amount_local_currency')
upper_boundary_age, lower_boundary_age

def find_skewed_boundaries(ise, variable, distance):
    IQR = ise[variable].quantile(0.75) - ise[variable].quantile(0.25)

    lower_boundary = ise[variable].quantile(0.25) - (IQR * distance)
    upper_boundary = ise[variable].quantile(0.75) + (IQR * distance)

    return upper_boundary, lower_boundary

countries = ['Sweden', 'Hungary', 'Greece', 'Cyprus', 'Portugal']

boundary_results = {}

for country in countries:
    # Filter the data for the current country
    country_data = ise[ise['country'] == country]

    # Find the upper and lower boundaries for the 'amount_local_currency' column
    upper_boundary_currency, lower_boundary_currency = find_skewed_boundaries(country_data, 'amount_local_currency', 3)

    # Store the results in the dictionary
    boundary_results[country] = (upper_boundary_currency, lower_boundary_currency)

for country, (upper, lower) in boundary_results.items():
    print(f"Country: {country}, Upper Boundary: {upper}, Lower Boundary: {lower}")

"""#Trimming or Truncation"""

ise.shape

import numpy as np

def trim_outliers_for_country(data, country, variable, distance):
    country_data = data[data['country'] == country]

    upper_boundary, lower_boundary = find_skewed_boundaries(country_data, variable, distance)

    trimmed_country_data = country_data.loc[(country_data[variable] >= lower_boundary) & (country_data[variable] <= upper_boundary)]

    data_without_country = data[data['country'] != country]

    trimmed_data = pd.concat([data_without_country, trimmed_country_data])

    return trimmed_data

# Initialize ise_trimmed with the original data
ise_trimmed = ise.copy()

country = ['Armenia', 'Sweden', 'Hungary', 'Greece', 'Cyprus', 'Portugal']  # Replace with your list of countries

for selected_country in country:
    ise_trimmed = trim_outliers_for_country(ise_trimmed, selected_country, 'amount_local_currency', 1.5)

# Display the final shape of the trimmed dataset
print('Size dataset - After trimming: ', ise_trimmed.shape)

"""#Splitting data"""

import pandas as pd

average_amounts_by_country = {}

unique_countries = ise_trimmed['country'].unique()
for country in unique_countries:
    country_ise_trimmed = ise_trimmed[ise_trimmed['country'] == country]

    grouped_ise_trimmed = country_ise_trimmed.groupby('year')['amount_local_currency'].mean().reset_index()

    average_amounts_by_country[country] = grouped_ise_trimmed

for country, result_ise_trimmed in average_amounts_by_country.items():
    print(f"Average Transaction Amounts for {country}:\n")
    print(result_ise_trimmed)
    print("\n")

"""Karena beberapa negara mempunyai data tahunan yang kurang lengkap, kami memutuskan untuk memfilter lagi negara yang akan kita pilih. Pada case data ini, kita mendapati banyak negara yang mempunyai year 2010, 2014, 2018. Oleh karena itu, kami menyimpulkan untuk memprediksi kenaikkan amount transaction per 4 tahunnya. Negara yang bisa diambil adalah sebagai berikut :

* Austria
* Bulgaria
* Cyprus
* Denmark
* Estonia
* Germany
* Ireland
* Italy
* Latvia
* Lithuania
* Luxembourg
* Malta
* Netherlands
* Norway
* Slovenia

## Pembuatan train data
"""

# List of countries to filter
countries_to_keep = [
    "Austria", "Bulgaria", "Cyprus", "Denmark", "Estonia",
    "Germany", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Malta", "Netherlands", "Norway", "Slovenia"
]

# Filter rows where the "Country" column is in the list of countries to keep
dataframe_for_train = ise_trimmed[ise_trimmed['country'].isin(countries_to_keep)]

dataframe_for_train.head()

"""## Pembuatan test data"""

# Step 1: Filter ise_trimmed to include only the years 2010, 2014, and 2018
filtered_ise_trimmed = ise_trimmed[ise_trimmed['year'].isin([2010, 2014, 2018])]

# Step 2: Group ise_trimmed by country and year and calculate the average amount
grouped_ise_trimmed = filtered_ise_trimmed.groupby(['country', 'year'])['amount_local_currency'].mean().reset_index()

# Step 3: Create an empty ise_trimmedFrame to store the results
result_df = pd.DataFrame(columns=['country', 'amount_per_4_year'])

# Step 4: Iterate over unique countries
unique_countries = grouped_ise_trimmed['country'].unique()
for country in unique_countries:
    country_ise_trimmed = grouped_ise_trimmed[grouped_ise_trimmed['country'] == country]

    # Step 4a: Check if ise_trimmed is available for the years 2010, 2014, and 2018
    if all(year in country_ise_trimmed['year'].values for year in [2010, 2014, 2018]):
        income_2010 = country_ise_trimmed[country_ise_trimmed['year'] == 2010]['amount_local_currency'].values[0]
        income_2014 = country_ise_trimmed[country_ise_trimmed['year'] == 2014]['amount_local_currency'].values[0]
        income_2018 = country_ise_trimmed[country_ise_trimmed['year'] == 2018]['amount_local_currency'].values[0]
        increased_income = ((income_2014 - income_2010) + (income_2018 - income_2014)) / 2
    else:
        increased_income = None  # Handle the case where ise_trimmed is missing

    # Step 4b: Add the ise_trimmed to the result ise_trimmedFrame
    result_df = result_df.append({'country': country, 'amount_per_4_year': increased_income}, ignore_index=True)

# Step 5: Display the result ise_trimmedFrame
result_df

result_df = result_df.dropna()

result_df

result_df.country.unique()

euro_countries = ['Austria', 'Belgium', 'Cyprus', 'Estonia', 'Germany', 'Greece', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Portugal', 'Slovenia', 'Spain']

result_df = result_df[result_df['country'].isin(euro_countries)]
result_df

"""## Penggabungan data"""

# List of countries to filter
countries_to_keep = ['Austria', 'Belgium', 'Cyprus', 'Estonia', 'Germany', 'Greece', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Portugal', 'Slovenia', 'Spain']

# Filter rows where the "Country" column is in the list of countries to keep
dataframe_for_train = ise_trimmed[ise_trimmed['country'].isin(countries_to_keep)]

# Sample DataFrame2
dataframe2 = result_df

# Create a copy of dataframe_for_train to store the concatenated values
df = dataframe_for_train.copy()

# Iterate through the rows of dataframe_for_train
for index, row in dataframe_for_train.iterrows():
    country = row['country']

    # Check if the country exists in dataframe2
    if country in dataframe2['country'].values:
        # Concatenate the "amount_per_4_year" values from dataframe2
        dataframe2_row = dataframe2[dataframe2['country'] == country]
        df.loc[index, 'amount_per_4_year'] = dataframe2_row['amount_per_4_year'].values[0]

# Print the resulting DataFrame
df

"""## Splitting"""

feature_columns = ["country_id","country", "year", "amount_local_currency"]

x = df[feature_columns]
y = df["amount_per_4_year"]
x

# Split dataset

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

print('Size Train Set : ', X_train.shape)
print('Size Test Set  : ', X_test.shape)
X_train

y_train

num_columns = X_train.select_dtypes(include = np.number).columns.tolist()
cat_columns = X_train.select_dtypes(include = ['object']).columns.tolist()

print('num col', num_columns)
print('cat col', cat_columns)

#split train and test based on column types

X_train_num = X_train[num_columns]
X_train_cat = X_train[cat_columns]

X_test_num = X_test[num_columns]
X_test_cat = X_test[cat_columns]

X_train_num

X_train.country.unique()

"""#Regression dan Model Evaluation"""

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

# Inisiasi model logreg
logreg = LogisticRegression()

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
train_Y = label_encoder.fit_transform(y_train)
test_Y = label_encoder.fit_transform(y_test)
logreg.fit(X_train_num, train_Y)

# Predict model
y_pred = logreg.predict(X_test_num)

# Evaluasi model menggunakan confusion matrix
cnf_matrix = confusion_matrix(test_Y, y_pred)
print('Confusion Matrix:\n', cnf_matrix)

# import required modules
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.clf()
# name  of classes
class_names = [0, 1]
fig, ax = plt.subplots()

tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# create heatmap
sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap='YlGnBu', fmt='g')
ax.xaxis.set_label_position('top')
plt.title('Confusion matrix', y=1.1)
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.tight_layout()
plt.show()

from sklearn.metrics import accuracy_score, precision_score, recall_score

#Menghitung Accuracy, Precision, dan Recall
print('Accuracy :', accuracy_score(test_Y, y_pred))
print('Precision:', precision_score(test_Y, y_pred, average='micro'))
print('Recall   :', recall_score(test_Y, y_pred, average='micro'))

from sklearn.metrics import mean_squared_error

mse = mean_squared_error(test_Y, y_pred)
print(mse)