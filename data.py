import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


def generate_filtered_df(original_df, subject=None, gender=None):
    gender_mapping = {'Mathematics': 'mathematics scale',
                      'Reading': 'reading scale',
                      'Science': 'science scale'}

    if subject is None and gender is None:
        return original_df

    if subject is None:
        return original_df[original_df['Gender'] == gender]

    if gender is None:
        if subject == 'All Subjects':
            return original_df

        return original_df[original_df['Performance'] == gender_mapping['subject']]

    if subject == 'All Subjects':
        return original_df[(original_df['Gender'] == gender)]
    else:
        return original_df[(original_df['Gender'] == gender) & (original_df['Performance'] == gender_mapping[subject])]


# Step 1: Create an interface for the website.
st.set_page_config(layout="wide")

# Step 2: Load and preprocess my dataset.
# Load the dataset and convert the '..' data to 'Nah'.
data = pd.read_csv('Pisa mean perfromance scores 2013 - 2015 Data.csv', na_values=['..'])
# Clean up my data.
# Seperate the column of 'Series Name',where begin with 'PISA: Mean performance on', following with 'subject' plus 'gender' at the end,for those did not mark gender stands for 'Average'.
data[['Performance', 'Gender']] = data['Series Name'].str.split('.', expand=True)
# st.write(data)

# Clean up the 'Performance' column to keep only the subjects.
data['Performance'] = data['Performance'].str.replace('PISA: Mean performance on the ', '', regex=False).str.strip()

# Handle missing gender values, and rename it 'Average'.
data['Gender'] = data['Gender'].fillna('Average').str.strip()
df = data.drop('Series Name', axis=1)

# Remove columns of '2013 [YR2013]' and '2014 [YR2014]'
data.drop(['2013 [YR2013]', '2014 [YR2014]'], axis=1, inplace=True)
# Remove rows where 'Country Name' is None.
data = data.dropna(subset=['Country Name'])
# Reset index and remove rows where written 'Data from database: Education Statistics: Learning Outcomes' and 'Last Updated: 12/12/2016' and reset data.
data.reset_index(drop=True, inplace=True)
data.drop(index=[1161, 1162], inplace=True)
# st.write(data)

# Clean up all the rows where '2015 [YR2015]' is None and rename it to '2015'
data = data.dropna(subset=['2015 [YR2015]'])
data.rename(columns={'2015 [YR2015]': 'Year of 2015'}, inplace=True)
# st.write(data)

# Hide the column of 'Series Name' to see the final data I need.
data_view = data.drop(columns=['Series Name'])
#st.write(data_view)

# Group the data by country and performance, then calculate the mean of the scores.
mean_scores = data_view.groupby(['Country Name', 'Performance'])['Year of 2015'].mean().reset_index()

# Step 3: List out questions and set up conditions.
st.sidebar.markdown('**PISA Mean Performance Scores 2015 Data**')
# List of questions
questions = [
    "Question 1: Top 10 countries with the highest average scores in 2015",
    "Question 2: Performance gender gap analysis in 2015",
    "Question 3: Subject score variability across countries in 2015"
]
selected_question = st.sidebar.radio("Choose a question to see detailed data:", questions)

# Add more conditions for additional questions

# Step 4: Add multiselect using st.siderbar.multiselect.
# filter for subjects
selected_subjects = st.sidebar.selectbox(
    'Select Subjects',
    options=['Mathematics', 'Science', 'Reading', 'All Subjects'],

)

selected_genders = st.sidebar.selectbox(
    'Select Genders',
    options=['Female', 'Male', 'Average'],
)
# if selected_genders == 'Average' or selected_genders == 'Male' or selected_genders == 'Female':
#     filtered_data = filtered_data[filtered_data['Gender'] == selected_genders]

filtered_data = generate_filtered_df(data_view, selected_subjects, selected_genders)

# Calculate the mean scores for the filtered subjects and genders
mean_scores = filtered_data.groupby('Country Name', as_index=False)['Year of 2015'].mean()
# # Get the top 10 country with the highest average scores in 2015
# top_countries = mean_scores.sort_values(by='Year of 2015', ascending=False).head(10)
# if len(top_countries) > 10:
#     top_countries = top_countries.head(10)


filtered_data = filtered_data.sort_values(by=['Year of 2015', 'Country Code'], ascending=False).head(10)

# Create the bar chart using px.bar() plotly express.
fig = px.bar(
    filtered_data,
    x='Country Name',
    y='Year of 2015',
    title=f'Top 10 countries with the highest average scores in 2015'
)
# st.plotly_chart(fig, use_container_width=True)
# st.write(data)
if selected_question == "Question 1: Top 10 countries with the highest average scores in 2015":
    # display the graphic for question #1
    st.plotly_chart(fig, use_container_width=True)

elif selected_question == 'Question 2: Performance gender gap analysis in 2015':
    # st.write("Top 10 countries with greatest gap of overall scores between gender")

    total_score_by_gender_df = data_view[(data_view['Gender'] == 'Male') | (data_view['Gender'] == 'Female')].groupby(['Country Code', 'Gender'])['Year of 2015'].sum().reset_index()
    male_total_score_df = total_score_by_gender_df[total_score_by_gender_df['Gender'] == 'Male'].sort_values('Country Code')
    female_total_score_df = total_score_by_gender_df[total_score_by_gender_df['Gender'] == 'Female'].sort_values('Country Code')

    # male_total_score_df = male_total_score_df[male_total_score_df['Country Code'].isin(female_total_score_df['Country Code'])]
    # female_total_score_df = female_total_score_df[female_total_score_df['Country Code'].isin(male_total_score_df['Country Code'])]


    joined_df = male_total_score_df.merge(female_total_score_df, how='inner', on='Country Code')

    joined_df['male_female_diff'] = joined_df['Year of 2015_x'] - joined_df['Year of 2015_y']

    joined_df = joined_df.sort_values(['male_female_diff'])
    joined_df['male_female_diff'].head(10)


    # st.write(joined_df)

    fig = px.bar(
        joined_df,
        x='Country Code',
        y='male_female_diff',
        title=f'Countries with gender gap',
        color="male_female_diff",
        color_continuous_scale='Bluered_r'
    )

    st.plotly_chart(fig, use_container_width=True)


elif selected_question == "Question 3: Subject score variability across countries in 2015":
    # Code to display the relevant chart or data
    # Create a bar chart to visualize the gap in performance for the selected subject(the interaction) .
    df3 = data_view[(data_view['Gender'] == 'Average')]


    fig1 = px.histogram(df3[df3['Performance'] == 'mathematics scale'], x="Year of 2015")
    st.plotly_chart(fig1, use_container_width=True)
    st.write('mathematics score, std dev={}'.format(df3[df3['Performance'] == 'mathematics scale']['Year of 2015'].std()))

    fig2 = px.histogram(df3[df3['Performance'] == 'reading scale'], x="Year of 2015")
    st.plotly_chart(fig2, use_container_width=True)
    st.write('reading score, std dev={}'.format(df3[df3['Performance'] == 'reading scale']['Year of 2015'].std()))


    fig3 = px.histogram(df3[df3['Performance'] == 'science scale'], x="Year of 2015")
    st.plotly_chart(fig3, use_container_width=True)
    st.write('science score, std dev={}'.format(df3[df3['Performance'] == 'science scale']['Year of 2015'].std()))

