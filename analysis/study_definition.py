from cohortextractor import StudyDefinition, patients, Measure
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

    recent_positive_covid_test=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        between=[
            "index_date - 3 months" ,
            "last_day_of_month(index_date)",
        ],
        returning="binary_flag",
        return_expectations={
            "date": {"earliest": "2021-01-01", "latest": "2021-02-01"},
            "rate": "exponential_increase",
        },
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
    alt_ref_range_lower=patients.reference_range_lower_bound_from(
        "alt_numeric_value",
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        }
    ),
    alt_ref_range_upper=patients.reference_range_upper_bound_from(
        "alt_numeric_value",
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        }
    ),
    alt_operator=patients.comparator_from(
        "alt_numeric_value",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {  # ~, =, >= , > , < , <=
                    None: 0.10,
                    "~": 0.05,
                    "=": 0.65,
                    ">=": 0.05,
                    ">": 0.05,
                    "<": 0.05,
                    "<=": 0.05,
                }
            },
            "incidence": 0.80,
        },
    ),
    alt_numeric_value_out_of_range=patients.satisfying(
        """
        (alt_numeric_value > 90) AND
        (
            (alt_operator = '>') OR
            (alt_operator = '=') OR
            (alt_operator = '>=')
        )
        """
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
    ast_ref_range_lower=patients.reference_range_lower_bound_from(
        "ast_numeric_value",
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        }
    ),
    ast_ref_range_upper=patients.reference_range_upper_bound_from(
        "ast_numeric_value",
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        }
    ast_operator=patients.comparator_from(
        "ast_numeric_value",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {  # ~, =, >= , > , < , <=
                    None: 0.10,
                    "~": 0.05,
                    "=": 0.65,
                    ">=": 0.05,
                    ">": 0.05,
                    "<": 0.05,
                    "<=": 0.05,
                }
            },
            "incidence": 0.80,
        },
    ),
    ast_numeric_value_out_of_range=patients.satisfying(
        """
        (ast_numeric_value > 90) AND
        (
            (ast_operator = '>') OR
            (ast_operator = '=') OR
            (ast_operator = '>=')
        )
        """
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
    bilirubin_ref_range_lower=patients.reference_range_lower_bound_from(
        "bilirubin_numeric_value",
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        }
    ),
    bilirubin_ref_range_upper=patients.reference_range_upper_bound_from(
        "bilirubin_numeric_value",
        return_expectations={
            "float": {"distribution": "normal", "mean": 45.0, "stddev": 20},
            "incidence": 0.5,
        }
    bilirubin_operator=patients.comparator_from(
        "bilirubin_numeric_value",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {  # ~, =, >= , > , < , <=
                    None: 0.10,
                    "~": 0.05,
                    "=": 0.65,
                    ">=": 0.05,
                    ">": 0.05,
                    "<": 0.05,
                    "<=": 0.05,
                }
            },
            "incidence": 0.80,
        },
    ),
    bilirubin_numeric_value_out_of_range=patients.satisfying(
        """
        (bilirubin_numeric_value > 90) AND
        (
            (bilirubin_operator = '>') OR
            (bilirubin_operator = '=') OR
            (bilirubin_operator = '>=')
        )
        """
    ),
)

measures = [
]

for test in ["alt", "ast", "bilirubin"]:
    m = Measure(
        id=f"{test}_rate",
        numerator=test,
        denominator="population",
        group_by="population"
    )
    
    m_oor = Measure(
        id=f"{test}_oor_rate",
        numerator=f"{test}_numeric_value_out_of_range",
        denominator="population",
        group_by="population"
    )
    

    measures.extend([m, m_oor])

    

    for d in ["age_band", "region", "practice"]:
        m_d = Measure(
            id=f"{test}_{d}_rate",
            numerator=test,
            denominator="population",
            group_by=d
        )
        measures.append(m_d)