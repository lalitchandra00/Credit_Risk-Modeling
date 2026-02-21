import streamlit as st
import pickle
import pandas as pd
from values import Values


# -------- LOAD MODEL -------- #
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("encoder_bundle.pkl", "rb") as f:
    encoder = pickle.load(f)

# bundle itself is dict
job_map = encoder["job_map"]
marital_map = encoder["marital_map"]
education_map = encoder["education_map"]
month_map = encoder["month_map"]
week_map = encoder["week_map"]


# -------- ENCODER FUNCTION -------- #
def encode_inputs(data: dict):
    data["job"] = job_map.get(data["job"], -1)
    data["marital_status"] = marital_map.get(data["marital_status"], -1)
    data["education"] = education_map.get(data["education"], -1)
    data["month"] = month_map.get(data["month"], -1)
    data["week"] = week_map.get(data["week"], -1)
    return data


# -------- UI -------- #
st.title("Bank Marketing Prediction App")
st.write("Enter customer details below:")

with st.form("prediction_form"):

    st.subheader("Personal Details")
    age = st.number_input("Age", 0, 120, 30)
    campaign = st.number_input("Campaign", 0, 100, 1)
    pdays = st.number_input("Pdays", -1, 999, 0)
    previous = st.number_input("Previous Contacts", 0, 100, 0)

    st.subheader("Personal Details")

    job = st.selectbox("Job", list(job_map.keys()))
    marital_status = st.selectbox("Marital Status", list(marital_map.keys()))
    education = st.selectbox("Education", list(education_map.keys()))

    st.subheader("Date")

    month = st.selectbox("Month", list(month_map.keys()))
    week = st.selectbox("Day of Week", list(week_map.keys()))

    # -------- DEFAULT -------- #
    st.subheader("Default")
    default_no = st.selectbox("Default No", [0, 1], index=0)
    default_other = st.selectbox("Default Other", [0, 1], index=0)
    default_yes = st.selectbox("Default Yes", [0, 1], index=0)


    # -------- HOUSING -------- #
    st.subheader("Housing Loan")
    house_no = st.selectbox("House No", [0, 1], index=0)
    house_other = st.selectbox("House Other", [0, 1], index=0)
    house_yes = st.selectbox("House Yes", [0, 1], index=0)


    # -------- PERSONAL LOAN -------- #
    st.subheader("Personal Loan")
    loan_no = st.selectbox("Loan No", [0, 1], index=0)
    loan_other = st.selectbox("Loan Other", [0, 1], index=0)
    loan_yes = st.selectbox("Loan Yes", [0, 1], index=0)


    # -------- PREVIOUS OUTCOME -------- #
    st.subheader("Previous Outcome")
    poutcome_failure = st.selectbox("Failure", [0, 1], index=0)
    poutcome_nonexistent = st.selectbox("Nonexistent", [0, 1], index=0)
    poutcome_success = st.selectbox("Success", [0, 1], index=0)

    submit = st.form_submit_button("Predict")


# -------- PREDICTION -------- #
if submit:
    try:
        input_data = Values(
            age=age,
            campaign=campaign,
            pdays=pdays,
            previous=previous,
            job=job,
            marital_status=marital_status,
            education=education,
            month=month,
            week=week,
            default_no=default_no,
            default_other=default_other,
            default_yes=default_yes,
            house_no=house_no,
            house_other=house_other,
            house_yes=house_yes,
            loan_no=loan_no,
            loan_other=loan_other,
            loan_yes=loan_yes,
            poutcome_failure=poutcome_failure,
            poutcome_nonexistent=poutcome_nonexistent,
            poutcome_success=poutcome_success
        )

        data_dict = input_data.model_dump()

        # encode categorical
        data_dict = encode_inputs(data_dict)

        df = pd.DataFrame([data_dict])

        prediction = model.predict(df)[0]   # extract single value

        if prediction == 0:
            st.success("Prediction: Your loan will not approve")
        else:
            st.success("Prediction: Your loan will be approved")
    except Exception as e:
        st.error(f"Error: {e}")