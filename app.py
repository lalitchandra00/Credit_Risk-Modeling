import pickle
import numpy as np
import streamlit as st
from sklearn.exceptions import NotFittedError

st.set_page_config(page_title="Loan Prediction App", page_icon="💰")

# Exact feature order used during training (loan_detection.csv minus target)
FEATURE_ORDER = [
    "age",
    "campaign",
    "pdays",
    "previous",
    "no_previous_contact",
    "not_working",
    "job_admin.",
    "job_blue-collar",
    "job_entrepreneur",
    "job_housemaid",
    "job_management",
    "job_retired",
    "job_self-employed",
    "job_services",
    "job_student",
    "job_technician",
    "job_unemployed",
    "job_unknown",
    "marital_divorced",
    "marital_married",
    "marital_single",
    "marital_unknown",
    "education_basic.4y",
    "education_basic.6y",
    "education_basic.9y",
    "education_high.school",
    "education_illiterate",
    "education_professional.course",
    "education_university.degree",
    "education_unknown",
    "default_no",
    "default_unknown",
    "default_yes",
    "housing_no",
    "housing_unknown",
    "housing_yes",
    "loan_no",
    "loan_unknown",
    "loan_yes",
    "contact_cellular",
    "contact_telephone",
    "month_apr",
    "month_aug",
    "month_dec",
    "month_jul",
    "month_jun",
    "month_mar",
    "month_may",
    "month_nov",
    "month_oct",
    "month_sep",
    "day_of_week_fri",
    "day_of_week_mon",
    "day_of_week_thu",
    "day_of_week_tue",
    "day_of_week_wed",
    "poutcome_failure",
    "poutcome_nonexistent",
    "poutcome_success",
]

JOB_OPTIONS = [
    "admin.",
    "blue-collar",
    "entrepreneur",
    "housemaid",
    "management",
    "retired",
    "self-employed",
    "services",
    "student",
    "technician",
    "unemployed",
    "unknown",
]

MARITAL_OPTIONS = ["divorced", "married", "single", "unknown"]
EDU_OPTIONS = [
    "basic.4y",
    "basic.6y",
    "basic.9y",
    "high.school",
    "illiterate",
    "professional.course",
    "university.degree",
    "unknown",
]

DEFAULT_OPTIONS = ["no", "unknown", "yes"]
HOUSING_OPTIONS = ["no", "unknown", "yes"]
LOAN_OPTIONS = ["no", "unknown", "yes"]
CONTACT_OPTIONS = ["cellular", "telephone"]
MONTH_OPTIONS = ["apr", "aug", "dec", "jul", "jun", "mar", "may", "nov", "oct", "sep"]
DAY_OPTIONS = ["fri", "mon", "thu", "tue", "wed"]
POUTCOME_OPTIONS = ["failure", "nonexistent", "success"]

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("Loan Prediction System")
st.write("Enter applicant details and click Predict")


def build_feature_vector(inputs: dict) -> np.ndarray:
    """Return a 1D numpy array ordered to match training columns."""
    row = [inputs[name] for name in FEATURE_ORDER]
    return np.array(row, dtype=float)


with st.form("loan-form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input("Age", 18, 100, 30, help="Applicant age in years")
        campaign = st.number_input("Campaign Contacts", 0, 50, 1)
        pdays = st.number_input("Days Since Last Contact", 0, 999, 999)
        previous = st.number_input("Previous Contacts", 0, 50, 0)
    with col2:
        no_previous_contact = st.selectbox("No Previous Contact", [0, 1])
        not_working = st.selectbox("Currently Not Working", [0, 1])
        job = st.selectbox("Job", JOB_OPTIONS)
        marital = st.selectbox("Marital Status", MARITAL_OPTIONS)
        education = st.selectbox("Education", EDU_OPTIONS)
    with col3:
        default = st.selectbox("Has Credit In Default?", DEFAULT_OPTIONS)
        housing = st.selectbox("Housing Loan", HOUSING_OPTIONS)
        loan = st.selectbox("Personal Loan", LOAN_OPTIONS)
        contact = st.selectbox("Contact Type", CONTACT_OPTIONS)
        month = st.selectbox("Last Contact Month", MONTH_OPTIONS)
        day = st.selectbox("Last Contact Day", DAY_OPTIONS)
        poutcome = st.selectbox("Previous Campaign Outcome", POUTCOME_OPTIONS)

    predict_request = st.form_submit_button("Predict")

if predict_request:
    features = {
        "age": age,
        "campaign": campaign,
        "pdays": pdays,
        "previous": previous,
        "no_previous_contact": no_previous_contact,
        "not_working": not_working,
    }

    # one-hot blocks
    for option in JOB_OPTIONS:
        features[f"job_{option}"] = 1 if job == option else 0

    for option in MARITAL_OPTIONS:
        features[f"marital_{option}"] = 1 if marital == option else 0

    for option in EDU_OPTIONS:
        features[f"education_{option}"] = 1 if education == option else 0

    for option in DEFAULT_OPTIONS:
        features[f"default_{option}"] = 1 if default == option else 0

    for option in HOUSING_OPTIONS:
        features[f"housing_{option}"] = 1 if housing == option else 0

    for option in LOAN_OPTIONS:
        features[f"loan_{option}"] = 1 if loan == option else 0

    for option in CONTACT_OPTIONS:
        features[f"contact_{option}"] = 1 if contact == option else 0

    for option in MONTH_OPTIONS:
        features[f"month_{option}"] = 1 if month == option else 0

    for option in DAY_OPTIONS:
        features[f"day_of_week_{option}"] = 1 if day == option else 0

    for option in POUTCOME_OPTIONS:
        features[f"poutcome_{option}"] = 1 if poutcome == option else 0

    input_array = build_feature_vector(features).reshape(1, -1)

    try:
        prediction = model.predict(input_array)[0]
    except NotFittedError:
        st.error("Model file is not trained. Retrain and save a fitted model.pkl.")
    except ValueError as exc:
        st.error(f"Input shape mismatch: {exc}")
    else:
        if int(prediction) == 1:
            st.success("Customer is likely to Accept Loan")
        else:
            st.error("Customer is NOT likely to Accept Loan")
