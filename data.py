import streamlit as st
import pandas as pd
import plotly.express as px

#Load the datasets
df_definition = pd.read_csv('Pisa mean performance scores 2013 - 2015 Definition and Source.csv')
df_data = pd.read_csv('Pisa mean perfromance scores 2013 - 2015 Data.csv')
st.write(df_data)

#Remove all the 'None' and Useless data from columns 'Country Name','Country Code','Series Name','Series Code','2013 [YR2013]','2014 [YR2014]',and '2015 [YR2015]'.

# Split the column into two new columns 'Series Name' and 'Gender'
df_data[['SeriesName', 'Gender']] = df_data['Series Name'].str.split(' . ', expand=True)


