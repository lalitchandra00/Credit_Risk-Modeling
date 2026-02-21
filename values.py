from pydantic import BaseModel

class Values(BaseModel):

    # numeric
    age: int
    campaign: int
    pdays: int
    previous: int

    # mapped categorical (already encoded as numbers)
    job: str
    marital_status: str
    education: str
    month: str
    week: str

    # default
    default_no: int
    default_other: int
    default_yes: int

    # house
    house_no: int
    house_other: int
    house_yes: int

    # loan
    loan_no: int
    loan_other: int
    loan_yes: int

    # poutcome
    poutcome_failure: int
    poutcome_nonexistent: int
    poutcome_success: int