import pandas as pd
import numpy as np
from pathlib import Path
from utilities import (
    OUTPUT_DIR,
    match_input_files,
    match_input_files_weekly,
    get_date_input_file,
    get_date_input_file_weekly,
    redact_small_numbers,
)

Path("output/monthly/joined/redacted").mkdir(parents=True, exist_ok=True)
Path("output/weekly/joined/redacted").mkdir(parents=True, exist_ok=True)

mean_ages_months = {}

for file in (OUTPUT_DIR / "monthly/joined").iterdir():
    if match_input_files(file.name):
        df = pd.read_csv(
            (OUTPUT_DIR / "monthly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file(file.name)

        for test in ["alt", "ast", "bilirubin"]:
            mean_ages_months[test] = []
            # only want those who have had a test
            df_subset = df.loc[df[test] == 1, :]

            age_by_group = df_subset.groupby("age_band_months")[
                [f"{test}_numeric_value"]
            ].mean()

            age_by_group["date"] = date
            age_by_group["population"] = df.groupby("age_band_months").size()

            age_by_group[f"{test}_numeric_value_count"] = df.groupby("age_band_months")[
                [f"{test}_numeric_value"]
            ].count()

            mean_ages_months[test].append(age_by_group)

for test in ["alt", "ast", "bilirubin"]:
    mean_ages_months_concat = pd.concat(mean_ages_months[test])

    # redact any mean values where calculated from low n

    mean_ages_months_concat = redact_small_numbers(
        mean_ages_months_concat,
        5,
        f"{test}_numeric_value_count",
        "population",
        f"{test}_numeric_value",
        "date",
        "age_band_months",
    )

    mean_ages_months_concat.to_csv(
        OUTPUT_DIR / "monthly/joined/redacted/mean_test_value_{test}_by_age.csv"
    )


mean_ages_weeks = {}

for file in (OUTPUT_DIR / "weekly/joined").iterdir():
    if match_input_files_weekly(file.name):
        df = pd.read_csv(
            (OUTPUT_DIR / "weekly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file_weekly(file.name)

        for test in ["alt", "ast", "bilirubin"]:

            mean_ages_weeks[test] = []
            # only want those who have had a test
            df_subset = df.loc[df[test] == 1, :]

            age_by_group = df_subset.groupby("age_band_months")[
                [f"{test}_numeric_value"]
            ].mean()

            age_by_group["date"] = date
            age_by_group["population"] = df.groupby("age_band_months").size()

            age_by_group[f"{test}_numeric_value_count"] = df.groupby("age_band_months")[
                [f"{test}_numeric_value"]
            ].count()

            mean_ages_weeks[test].append(age_by_group)

for test in ["alt", "ast", "bilirubin"]:
    mean_ages_weeks_concat = pd.concat(mean_ages_weeks[test])

    # redact any mean values where calculated from low n

    mean_ages_weeks_concat = redact_small_numbers(
        mean_ages_weeks_concat,
        5,
        f"{test}_numeric_value_count",
        "population",
        f"{test}_numeric_value",
        "date",
        "age_band_months",
    )

    mean_ages_weeks_concat.to_csv(
        OUTPUT_DIR / "weekly/joined/redacted/mean_test_value_{test}_by_age.csv"
    )
