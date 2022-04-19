from cohortextractor import codelist_from_csv

alt_codelist = codelist_from_csv(
    "codelists/opensafely-alanine-aminotransferase-alt-tests.csv",
    system="snomed",
    column="code",
)

alt_numeric_value_codelist = codelist_from_csv(
    "codelists/opensafely-alanine-aminotransferase-alt-tests-numerical-value.csv",
    system="snomed",
    column="code",
)

# to change
ast_codelist = codelist_from_csv(
    "codelists/user-Louis-aspartate-aminotransferase.csv",
    system="snomed",
    column="code",
)


ast_numeric_value_codelist = codelist_from_csv(
    "codelists/user-Louis-aspartate-aminotransferase.csv.csv",
    system="snomed",
    column="code",
)

# to change
bilirubin_codelist = codelist_from_csv(
    "codelists/user-Louis-bilirubin-tests.csv",
    system="snomed",
    column="code",
)


bilirubin_numeric_value_codelist = codelist_from_csv(
    "codelists/user-Louis-bilirubin-tests.csv",
    system="snomed",
    column="code",
)

hepatitis_codelist = codelist_from_csv(
    "codelists/user-brian-mackenna-inflammatory-disease-of-the-liver.csv",
    system="snomed",
    column="code",
)

gi_illness_codelist = codelist_from_csv(
    "codelists/user-kate-mansfield-disorder-of-digestive-system-all-descendants.csv",
    system="snomed",
    column="code",
)
