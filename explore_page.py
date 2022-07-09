from enum import auto
import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 


# function to cutoff countries with low number of respondents
def shortener(cats, cutoff):
    cat_map = {}
    for i in range(len(cats)):
        if cats.values[i] >= cutoff:
            cat_map[cats.index[i]] = cats.index[i]
        else:
            cat_map[cats.index[i]] = 'Others'
    return cat_map

# function to clean years column
def clean_years(X):
    if X == 'More than 50 years':
        return 50
    if X == 'Less than 1 year':
        return 0.5
    return float(X)

# function to clean education
def clean_edu(X):
    if "Bachelor’s degree" in X:
        return 'Bachelors degree'
    if "Master’s degree" in X:
        return 'Masters degree'
    if 'Professional degree' in X or 'Other doctoral' in X:
        return 'Post Grad'
    return 'Pre Bachelors'


@st.cache
def load_data():
    url = "./dataset/survey_results_public.csv"
    data = pd.read_csv(url)
    df = data.copy()
    features = ['Country','EdLevel','YearsCodePro','CompTotal']
    df = df[features]
    df = df.rename({'CompTotal':'Salary'}, axis=1)
    df = df[df["Salary"].notnull()]
    df.dropna(inplace=True)
    # country
    country_map = shortener(df.Country.value_counts(), 1000) # 1000 respondents limit
    df['Country'] = df['Country'].map(country_map)
    # salary
    df = df[df["Salary"] <= 300000] 
    df = df[df["Salary"] >= 10000] # min for full time employment
    df = df[df["Country"] != "Others"]
    # years
    df.YearsCodePro = df.YearsCodePro.apply(clean_years) 
    # education
    df["EdLevel"] = df["EdLevel"].apply(clean_edu)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    
    st.write("""### Welcome to Stack Overflow Developer Survey 2021""")

    data = df["Country"].value_counts()

    # pie chart 
    explode = (0, 0.1, 0, 0.1, 0, 0.2, 0, 0.2, 0, 0.2)
    fig1, ax1 = plt.subplots(figsize=(10,10))
    ax1.pie(data, explode=explode, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal") # equal aspect ratio: pie will be drawn as a circle
    st.write(
        """#### Data from different countries"""
    )
    st.pyplot(fig1)

    # bar chart 
    st.write(
        """#### Mean Salary by countries"""
    )
    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    # fig2, ax2 = plt.subplots()
    st.bar_chart(data)

    st.write(
        """#### Mean Salary by Experience"""
    )
    data = df.groupby(['YearsCodePro'])['Salary'].mean().sort_values(ascending=True)
    # fig2, ax2 = plt.subplots()
    st.line_chart(data)
