import pandas as pd
import numpy as np
from utilities import (
    OUTPUT_DIR,
    match_input_files,
    match_input_files_weekly,
    get_date_input_file,
    get_date_input_file_weekly,
)

for file in (OUTPUT_DIR / "monthly/joined").iterdir():
    if match_input_files(file.name):
        df = pd.read_csv(
            (OUTPUT_DIR / "monthly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file(file.name)
        date = pd.to_datetime(date).strftime("%Y-%m")
        df["date"] = date
        df["date"] = pd.to_datetime(df["date"])

        # get age in months
        df["age_months"] = df["date"] - df["dob"]

        df["age_months"] = (df["age_months"] / np.timedelta64(1, "M")).round(0)

        df["age_band_months"] = df["age_band"].copy()

        # recategorise age bands
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] <= 3), "age_band_months"
        ] = "0-3 months"
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] > 3), "age_band_months"
        ] = "3 months - 5 years"
        df.to_csv((OUTPUT_DIR / "monthly/joined") / file.name)


for file in (OUTPUT_DIR / "weekly/joined").iterdir():
    if match_input_files_weekly(file.name):
        df = pd.read_csv(
            (OUTPUT_DIR / "weekly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file_weekly(file.name)
        date = pd.to_datetime(date).strftime("%Y-%m-%d")

        df["date"] = date
        df["date"] = pd.to_datetime(df["date"])

        df["age_days"] = df["date"] - df["dob"]

        df["age_months"] = (df["age_days"] / np.timedelta64(1, "M")).round(0)

        df["age_band_months"] = df["age_band"].copy()
        # recategorise age bands
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] <= 3), "age_band_months"
        ] = "0-3 months"
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] > 3), "age_band_months"
        ] = "3 months - 5 years"

        df.to_csv((OUTPUT_DIR / "weekly/joined") / file.name)
