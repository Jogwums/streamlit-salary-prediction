import streamlit as st
import pandas as pd 
import pickle
import numpy as np 

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data 

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_edu = data["le_edu"]
le_age = data["le_age"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some info to run predictions""")

    countries = (
        "United States of America","Others","India","Germany",
        "United Kingdom of Great Britain and Northern Ireland","Canada","France",
        "Brazil","Poland","Netherlands","Spain","Australia",
        "Italy","Russian Federation","Sweden","Switzerland",
        "Turkey","Israel","Ukraine","Iran, Islamic Republic of...","Mexico",
        "Czech Republic","Austria","Belgium","Norway","Denmark","Argentina")

    age = ('25-34 years old', '35-44 years old', '45-54 years old',
       '18-24 years old', '55-64 years old', '65 years or older',
       'Under 18 years old', 'Prefer not to say')

    education = ('Masters degree', 'Bachelors degree', 'Pre Bachelors', 'Post Grad')

    # User input fields 
    country = st.selectbox("Country", countries)

    age = st.selectbox("Age Group", age)

    education = st.selectbox("Level of Education", education)

    experience = st.slider("Years of Experience",0,50,3)


    code = st.button("Calculate Salary")

    if code:
        X = np.array([[country, education, experience,age]])
        X[:,0] = le_country.transform(X[:,0])
        X[:,1] = le_edu.transform(X[:,1])
        X[:,3] = le_age.transform(X[:,3])
        X = X.astype(float)

        salary = regressor.predict(X)

        st.subheader(f"The estimated salary is ${salary[0]:,.2f}")