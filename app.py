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
st.set_page_config(page_title="Loan Predictor", layout="wide")

st.title("💳 Loan Approval Prediction Dashboard")
st.markdown("---")


with st.form("prediction_form"):

    # ================= PERSONAL =================
    with st.expander("👤 Personal Information", expanded=True):

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            age = st.number_input("Age", 0, 120, 30)
        with col2:
            campaign = st.number_input("Campaign", 0, 100, 1)
        with col3:
            pdays = st.number_input("Pdays", -1, 999, 0)
        with col4:
            previous = st.number_input("Previous Contacts", 0, 100, 0)

        col5, col6, col7 = st.columns(3)

        with col5:
            job = st.selectbox("Job", list(job_map.keys()))
        with col6:
            marital_status = st.selectbox("Marital Status", list(marital_map.keys()))
        with col7:
            education = st.selectbox("Education", list(education_map.keys()))


    # ================= DATE =================
    with st.expander("📅 Contact Timing", expanded=False):

        col8, col9 = st.columns(2)

        with col8:
            month = st.selectbox("Month", list(month_map.keys()))
        with col9:
            week = st.selectbox("Day of Week", list(week_map.keys()))


    # ================= CREDIT FLAGS =================
    with st.expander("🏦 Credit Information", expanded=False):

        st.markdown("##### Default History")
        c1, c2, c3 = st.columns(3)
        default_no = c1.selectbox("No", [0,1])
        default_other = c2.selectbox("Other", [0,1])
        default_yes = c3.selectbox("Yes", [0,1])

        st.markdown("##### Housing Loan")
        h1, h2, h3 = st.columns(3)
        house_no = h1.selectbox("No ", [0,1])
        house_other = h2.selectbox("Other ", [0,1])
        house_yes = h3.selectbox("Yes ", [0,1])

        st.markdown("##### Personal Loan")
        l1, l2, l3 = st.columns(3)
        loan_no = l1.selectbox("No  ", [0,1])
        loan_other = l2.selectbox("Other  ", [0,1])
        loan_yes = l3.selectbox("Yes  ", [0,1])

        st.markdown("##### Previous Campaign Result")
        p1, p2, p3 = st.columns(3)
        poutcome_failure = p1.selectbox("Failure", [0,1])
        poutcome_nonexistent = p2.selectbox("Nonexistent", [0,1])
        poutcome_success = p3.selectbox("Success", [0,1])


    st.markdown("---")
    submit = st.form_submit_button("🚀 Predict Loan Approval")
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