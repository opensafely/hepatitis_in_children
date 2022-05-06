import pandas as pd
import numpy as np
from pathlib import Path
from utilities import (
    OUTPUT_DIR,
    match_input_files,
    match_input_files_weekly,
    get_date_input_file,
    get_date_input_file_weekly,
    redact_small_numbers
)

Path("output/monthly/joined/redacted").mkdir(parents=True, exist_ok=True)
Path("output/weekly/joined/redacted").mkdir(parents=True, exist_ok=True)

mean_ages_months = []

for file in (OUTPUT_DIR / "monthly/joined").iterdir():
    if match_input_files(file.name):
        df = pd.read_csv(
            (OUTPUT_DIR / "monthly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file(file.name)

        age_by_group = df.groupby("age_band_months")[["alt_numeric_value", "ast_numeric_value", "bilirubin_numeric_value"]].mean()
        age_by_group["date"] = date
        age_by_group["population"] = df.groupby("age_band_months").size()

        for i in ["alt", "ast", "bilirubin"]:
            age_by_group[f"{i}_numeric_value_count"] = df.groupby("age_band_months")[[f"{i}_numeric_value"]].count()
        mean_ages_months.append(age_by_group)
        

mean_ages_months_concat = pd.concat(mean_ages_months)

# redact any mean values where calculated from low n

mean_ages_months_concat = redact_small_numbers(mean_ages_months_concat, 5, "alt_numeric_value_count", "population", "alt_numeric_value", "date")
mean_ages_months_concat = redact_small_numbers(mean_ages_months_concat, 5, "ast_numeric_value_count", "population", "ast_numeric_value", "date")
mean_ages_months_concat = redact_small_numbers(mean_ages_months_concat, 5, "bilirubin_numeric_value_count", "population", "bilirubin_numeric_value", "date")

mean_ages_months_concat.to_csv(OUTPUT_DIR / "monthly/joined/redacted/mean_test_value_by_age.csv")



mean_ages_weeks = []

for file in (OUTPUT_DIR / "weekly/joined").iterdir():
    if match_input_files_weekly(file.name):
        df = pd.read_csv(
            (OUTPUT_DIR / "weekly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file_weekly(file.name)

        age_by_group = df.groupby("age_band_months")[["alt_numeric_value", "ast_numeric_value", "bilirubin_numeric_value"]].mean()
        age_by_group["date"] = date
        age_by_group["population"] = df.groupby("age_band_months").size()

        for i in ["alt", "ast", "bilirubin"]:
            age_by_group[f"{i}_numeric_value_count"] = df.groupby("age_band_months")[[f"{i}_numeric_value"]].count()
        mean_ages_weeks.append(age_by_group)
        

mean_ages_weeks_concat = pd.concat(mean_ages_weeks)

# redact any mean values where calculated from low n

mean_ages_weeks_concat = redact_small_numbers(mean_ages_weeks_concat, 5, "alt_numeric_value_count", "population", "alt_numeric_value", "date")
mean_ages_weeks_concat = redact_small_numbers(mean_ages_weeks_concat, 5, "ast_numeric_value_count", "population", "ast_numeric_value", "date")
mean_ages_weeks_concat = redact_small_numbers(mean_ages_weeks_concat, 5, "bilirubin_numeric_value_count", "population", "bilirubin_numeric_value", "date")

mean_ages_weeks_concat.to_csv(OUTPUT_DIR / "weekly/joined/redacted/mean_test_value_by_age.csv")