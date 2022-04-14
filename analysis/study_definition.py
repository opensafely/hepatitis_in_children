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
