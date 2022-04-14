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
        (age_band != "missing")
        """,
        registered=patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
        ),
        died=patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1},
        ),
    ),
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "0-5": """ age >= 0 AND age <= 5""",
            "6-10": """ age >  5 AND age <= 10""",
            "11-20": """ age > 10 AND age <= 20""",
            "21-30": """ age > 20 AND age <= 30""",
        },
        age=patients.age_as_of(
            "index_date",
            return_expectations={
                "rate": "universal",
                "int": {"distribution": "population_ages"},
            },
        ),
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.05,
                    "0-5": 0.25,
                    "6-10": 0.25,
                    "11-20": 0.25,
                    "21-30": 0.2,
                }
            },
        },
    ),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49, "F": 0.5, "U": 0.01}},
        }
    ),
    region=patients.registered_practice_as_of(
        "index_date",
        returning="nuts1_region_name",
        return_expectations={
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and the Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East of England": 0.1,
                    "London": 0.2,
                    "South East": 0.2,
                }
            }
        },
    ),
    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
    hepatitis=patients.with_these_clinical_events(
        codelist=hepatitis_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        find_last_match_in_period=True,
        return_expectations={"incidence": 0.5},
    ),
    gi_illness=patients.with_these_clinical_events(
        codelist=hepatitis_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        find_last_match_in_period=True,
        return_expectations={"incidence": 0.5},
    ),
    alt=patients.with_these_clinical_events(
        codelist=alt_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        find_last_match_in_period=True,
        return_expectations={"incidence": 0.5},
    ),
    alt_code=patients.with_these_clinical_events(
        codelist=alt_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        find_last_match_in_period=True,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"1000731000000107": 0.5, "1000981000000109": 0.5}},
        },
    ),
    alt_numeric_value=patients.with_these_clinical_events(
        codelist=alt_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="numeric_value",
        find_last_match_in_period=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        },
    ),
    ast=patients.with_these_clinical_events(
        codelist=ast_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        find_last_match_in_period=True,
        return_expectations={"incidence": 0.5},
    ),
    ast_code=patients.with_these_clinical_events(
        codelist=ast_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        find_last_match_in_period=True,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"1000731000000107": 0.5, "1000981000000109": 0.5}},
        },
    ),
    ast_numeric_value=patients.with_these_clinical_events(
        codelist=ast_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="numeric_value",
        find_last_match_in_period=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        },
    ),
    bilirubin=patients.with_these_clinical_events(
        codelist=bilirubin_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="binary_flag",
        find_last_match_in_period=True,
        return_expectations={"incidence": 0.5},
    ),
    bilirubin_code=patients.with_these_clinical_events(
        codelist=bilirubin_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="code",
        find_last_match_in_period=True,
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"1000731000000107": 0.5, "1000981000000109": 0.5}},
        },
    ),
    bilirubin_numeric_value=patients.with_these_clinical_events(
        codelist=bilirubin_codelist,
        between=["index_date", "last_day_of_month(index_date)"],
        returning="numeric_value",
        find_last_match_in_period=True,
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        },
    ),
)
