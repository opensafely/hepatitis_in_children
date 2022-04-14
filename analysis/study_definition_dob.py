from cohortextractor import StudyDefinition, patients
from codelists import *


study = StudyDefinition(
    index_date="2019-01-01",
    default_expectations={
        "date": {"earliest": "2017-04-01", "latest": "2022-04-01"},
        "rate": "exponential_increase",
        "incidence": 0.1,
    },
    
    population=patients.satisfying(
        """
        registered AND
        (NOT died) AND
        (age >=0 AND age <=30) AND 
        (sex = 'M' OR sex = 'F')
        """,

        registered = patients.registered_as_of(
        "index_date",
        return_expectations={"incidence": 0.9},
        ),

        died = patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1}
        ),
        age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
        ),
        sex=patients.sex(
            return_expectations={
                "rate": "universal",
                "category": {"ratios": {"M": 0.49, "F": 0.5, "U": 0.01}},
            }
        ),
    ),
    
    dob=patients.date_of_birth(
    "YYYY-MM",
    return_expectations={
        "date": {"earliest": "1950-01-01", "latest": "today"},
        "rate": "uniform",
    }
    ),
    
)

