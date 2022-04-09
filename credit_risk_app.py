"""
credit_risk_app -- Arhum Zafar

A Streamlit web application that takes in a user's financial background and loan information
and returns whether the user will default on their loan.
"""

import streamlit as st 
import pandas as pd
import pickle

# load in the trained model
pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)

# function that produces the default prediction
def prediction(age, income, emp_length, loan_amount, int_rate, default_history, credit_length, home_ownership, loan_intent):

    # Processing user inputs

    ## Default History
    if default_history == "Yes":
        default_history = 1
    else:
        default_history = 0
    

    ## Home Ownership
    if home_ownership == "Mortgage":
        pho_Mortgage = 1
        pho_Other = 0
        pho_Own = 0
        pho_Rent = 0
    elif home_ownership == "Other":
        pho_Mortgage = 0
        pho_Other = 1
        pho_Own = 0
        pho_Rent = 0
    elif home_ownership == "Own":
        pho_Mortgage = 0
        pho_Other = 0
        pho_Own = 1
        pho_Rent = 0
    elif home_ownership == "Rent":
        pho_Mortgage = 0
        pho_Other = 0
        pho_Own = 0
        pho_Rent = 1

    ## Loan Intent
    if loan_intent == "Debt Consolidation":
        intent_DC = 1
        intent_Education = 0
        intent_Home_Improvement = 0
        intent_Medical = 0
        intent_Personal = 0
        intent_Venture = 0
    elif loan_intent == "Education":
        intent_DC = 0
        intent_Education = 1
        intent_Home_Improvement = 0
        intent_Medical = 0
        intent_Personal = 0
        intent_Venture = 0
    elif loan_intent == "Home Improvement":
        intent_DC = 0
        intent_Education = 0
        intent_Home_Improvement = 1
        intent_Medical = 0
        intent_Personal = 0
        intent_Venture = 0
    elif loan_intent == "Medical":
        intent_DC = 0
        intent_Education = 0
        intent_Home_Improvement = 0
        intent_Medical = 1
        intent_Personal = 0
        intent_Venture = 0
    elif loan_intent == "Personal":
        intent_DC = 0
        intent_Education = 0
        intent_Home_Improvement = 0
        intent_Medical = 0
        intent_Personal = 1
        intent_Venture = 0
    elif loan_intent == "Venture":
        intent_DC = 0
        intent_Education = 0
        intent_Home_Improvement = 0
        intent_Medical = 0
        intent_Personal = 0
        intent_Venture = 1

    ## Loan Percent Income
    loan_percent_income = loan_amount / income
    
    # Creating a dataframe with the user's inputs
    user_inputs = pd.DataFrame([[age, income, emp_length, loan_amount, int_rate, 
                                loan_percent_income, default_history, credit_length, pho_Mortgage, pho_Other,
                                pho_Own, pho_Rent, intent_DC, intent_Education, intent_Home_Improvement, intent_Medical,
                                intent_Personal, intent_Venture]])

    #make prediction
    prediction = classifier.predict(user_inputs)

    if prediction == 0:
        prediction = "Not Default"
    else:
        prediction = "Default"

    return prediction

# function that defines our app
def main():
    """Credit Risk App"""
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:Beige;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Credit Risk App </h1> 
    <h3 style ="color:black;text-align:center;"> arhum zafar </h3> 
    </div> 
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    st.title("Welcome!")
    st.subheader("Begin entering your financial information on the left.")
    st.subheader("The app will then predict whether you will default on your loan.")
    st.write("If there are no fields on the left, click the arrow in the upper left corner.")
    st.write("")
    st.write("")



    # define the user inputs
    age = st.sidebar.slider("Enter your age", 21, 99, 25)
    income = st.sidebar.slider("Income in Dollars:", 0, 150000, 55000)
    emp_length = st.sidebar.slider("Employment length in years", 0, 50, 5)
    int_rate = st.sidebar.slider("Interest Rate - between 5-15%", 5.0, 15.0, 10.0)
    loan_amount = st.sidebar.slider("Loan Amount in dollars:", 0, 100000, 15000)
    credit_length = st.sidebar.slider("Credit history length in years:", 0, 50, 5)
    default_history = st.sidebar.radio("Have you defaulted on a loan before?", ("Yes", "No"))
    home_ownership = st.sidebar.radio("Select your home ownership status:", ("Mortgage", "Rent", "Own", "Other"))
    loan_intent = st.sidebar.radio("Select your loan intent:", ("Debt Consolidation", "Education", "Home Improvement", "Medical",
    "Personal", "Venture"))

    # display the user inputs
    st.write("Your Age: ", int(age))
    st.write("Your Income: ", int(income))
    st.write("Employment Length: ", emp_length)
    st.write("Interest Rate: ", float(int_rate))
    st.write("Loan Amount: ", int(loan_amount))
    st.write("Credit history Length in years: ", int(credit_length))
    st.selectbox("Default History: ", default_history)
    st.selectbox("Home Ownership: ", home_ownership)
    st.selectbox("Loan Intent: ", loan_intent)
    result = ""

    if st.button("Predict"):
        result = prediction(age, income, emp_length, loan_amount, int_rate, default_history, credit_length, home_ownership, loan_intent)
        if result == "Default":
            st.write("")
            st.success("Unfortunately, you are likely to default on your loan.")
        else:
            st.write("")
            st.success("Congrats! You are not likely to default on your loan.")
            st.write("")

        st.write("Thank you for using the credit risk app!")
    


if __name__ == "__main__":
    main()
