from pydantic import BaseModel

class Values(BaseModel):
    age: int
    campaign: int
    pdays: int
    previous: int
    no_previous_contact: int

    not_working: int

    job_admin_: int
    job_blue_collar: int
    job_entrepreneur: int
    job_housemaid: int
    job_management: int
    job_retired: int
    job_self_employed: int
    job_services: int
    job_student: int
    job_technician: int
    job_unemployed: int
    job_unknown: int

    marital_divorced: int
    marital_married: int
    marital_single: int
    marital_unknown: int

    education_basic_4y: int
    education_basic_6y: int
    education_basic_9y: int
    education_high_school: int
    education_illiterate: int
    education_professional_course: int
    education_university_degree: int
    education_unknown: int

    default_no: int
    default_unknown: int
    default_yes: int

    housing_no: int
    housing_unknown: int
    housing_yes: int

    loan_no: int
    loan_unknown: int
    loan_yes: int

    contact_cellular: int
    contact_telephone: int

    month_apr: int
    month_aug: int
    month_dec: int
    month_jul: int
    month_jun: int
    month_mar: int
    month_may: int
    month_nov: int
    month_oct: int
    month_sep: int

    day_of_week_fri: int
    day_of_week_mon: int
    day_of_week_thu: int
    day_of_week_tue: int
    day_of_week_wed: int

    poutcome_failure: int
    poutcome_nonexistent: int
    poutcome_success: int
