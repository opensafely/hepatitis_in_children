from cohortextractor import StudyDefinition, patients
from codelists import *


study = StudyDefinition(
    index_date="2022-04-01",
    default_expectations={
        "date": {"earliest": "2017-04-01", "latest": "2022-04-01"},
        "rate": "exponential_increase",
        "incidence": 0.1,
    },
    population=patients.all(),
    dob=patients.date_of_birth(
        "YYYY-MM",
        return_expectations={
            "date": {"earliest": "1992-01-01", "latest": "today"},
            "rate": "uniform",
        },
    ),
)
