from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA


study = StudyDefinition(
    index_date="2019-01-01",
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
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
    ),
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "0-5": """ age >= 0 AND age <= 5""",
            "6-10": """ age >  5 AND age <= 10""",
            "11-20": """ age > 10 AND age <= 20""",
            "21-30": """ age > 20 AND age <= 30""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.05,
                    "0-5": 0.25,
                    "6-10": 0.25,
                    "11-20": 0.25,
                    "21-30": 0.2
                }
            },
        },

    ),
)

