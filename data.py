import streamlit as st
import pandas as pd
import plotly.express as px

#Load the dataset and convert the '..' data to 'Nah'.
data = pd.read_csv('Pisa mean perfromance scores 2013 - 2015 Data.csv', na_values=['..'])

#Seperate the column of 'Series Name',where begin with 'PISA: Mean performance on', following with 'subject' plus 'gender' at the end,for those did not mark gender stands for 'in general'.
data[['Performance', 'Gender']] = data['Series Name'].str.split('.', expand=True)

# Clean up the 'Performance' column to keep only the subjects.
data['Performance'] = data['Performance'].str.replace('PISA: Mean performance on the ', '', regex=False).str.strip()

# Handle missing gender values, and rename it 'In General'.
data['Gender'] = data['Gender'].fillna('In General').str.strip()
data = data.drop('Series Name', axis=1)
st.write(data)

