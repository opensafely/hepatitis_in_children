import pandas as pd
import numpy as np
from utilities import OUTPUT_DIR, match_input_files, get_date_input_file

dob_df = pd.read_csv(OUTPUT_DIR / "input_dob.csv.gz")


for file in (OUTPUT_DIR / "monthly").iterdir():
    if match_input_files(file.name):
        df = pd.read_csv((OUTPUT_DIR / "monthly/joined") / file.name)
        date = get_date_input_file(file.name)
        df["date"] = pd.to_datetime(date).dt.strftime("%Y-%M")
        df["dob"] = pd.to_datetime(df["dob"])

        # get age in months
        df["age_days"] = df["date"] - df["dob"]
        df["age_months"] = (df["age_days"] / np.timedelta64(1, "M")).round(0)

        # recategorise age bands
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] <= 3), "age_band"
        ] = "0-3 months"
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] > 3), "age_band"
        ] = "3 months - 5 years"

        df.to_csv((OUTPUT_DIR / "monthly/joined") / file.name)


for file in (OUTPUT_DIR / "weekly").iterdir():
    if match_input_files(file.name):
        df = pd.read_csv((OUTPUT_DIR / "weekly/joined") / file.name)
        date = get_date_input_file(file.name)
        df["date"] = pd.to_datetime(date).dt.strftime("%Y-%M")
        df["dob"] = pd.to_datetime(df["dob"])

        # get age in months
        df["age_days"] = df["date"] - df["dob"]
        df["age_months"] = (df["age_days"] / np.timedelta64(1, "M")).round(0)

        # recategorise age bands
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] <= 3), "age_band"
        ] = "0-3 months"
        df.loc[
            (df["age_band"] == "0-5") & (df["age_months"] > 3), "age_band"
        ] = "3 months - 5 years"

        df.to_csv((OUTPUT_DIR / "weekly/joined") / file.name)
