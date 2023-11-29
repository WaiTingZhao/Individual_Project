import streamlit as st
import pandas as pd
import plotly.express as px

#Load the dataset and convert the '..' data to 'Nah'.
data = pd.read_csv('Pisa mean perfromance scores 2013 - 2015 Data.csv', na_values=['..'])

#Seperate the column of 'Series Name',where begin with 'PISA: Mean performance on', following with 'subject' plus 'gender' at the end,for those did not mark gender stands for 'Average'.
data[['Performance', 'Gender']] = data['Series Name'].str.split('.', expand=True)
#st.write(data)

# Clean up the 'Performance' column to keep only the subjects.
data['Performance'] = data['Performance'].str.replace('PISA: Mean performance on the ', '', regex=False).str.strip()

# Handle missing gender values, and rename it 'Average'.
data['Gender'] = data['Gender'].fillna('Average').str.strip()
df = data.drop('Series Name', axis=1)

#Remove columns of '2013 [YR2013]' and '2014 [YR2014]'
data.drop(['2013 [YR2013]', '2014 [YR2014]'], axis=1, inplace=True)

#Remove rows where 'Country Name' is None.
data = data.dropna(subset=['Country Name'])

#Reset index and remove rows where written 'Data from database: Education Statistics: Learning Outcomes' and 'Last Updated: 12/12/2016' and reset data.
data.reset_index(drop=True, inplace=True)
data.drop(index=[1161, 1162], inplace=True)
#st.write(data)

#Clean up all the rows where '2015 [YR2015]' is None and rename it to '2015'
data = data.dropna(subset=['2015 [YR2015]'])
data.rename(columns={'2015 [YR2015]': 'Year of 2015'}, inplace=True)

#st.write(data)

#Hide the column of 'Series Name' to see the final data I need.
data_view = data.drop(columns=['Series Name'])
#Show the cleaned data I will use for my project.
st.write(data_view)

#Group the data by country and performance, then calculate the mean of the scores.
mean_scores = data_view.groupby(['Country Name', 'Performance'])['Year of 2015'].mean().reset_index()
#Create a bar chart
fig = px.bar(mean_scores, x='Country Name', y='Year of 2015', color='Performance', title='PISA Mean Scores by Country and Subject (Year of 2015)')
st.plotly_chart(fig)