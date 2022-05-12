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

Path("output/monthly/joined/isaric").mkdir(parents=True, exist_ok=True)
Path("output/weekly/joined/isaric").mkdir(parents=True, exist_ok=True)

mean_ages_months = {}

rows = []

for file in (OUTPUT_DIR / "weekly/joined").iterdir():
    if match_input_files(file.name):
        df = pd.read_csv(
            (OUTPUT_DIR / "weekly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file(file.name)
        
        #subset the columns we're interested in
        df = df.loc[((df["alt_numeric_value_date"].notnull()) | (df["ast_numeric_value_date"].notnull())), ["patient_id", "dob", "alt_numeric_value_date", "ast_numeric_value_date", "alt_numeric_value", "ast_numeric_value"]]
       
        unique_dates = np.unique(list(df["alt_numeric_value_date"].values) + list(df["ast_numeric_value_date"].values))
        print(date)
        for d in unique_dates:
          
            df_subset = df.loc[(df["alt_numeric_value_date"] == d) | (df["ast_numeric_value_date"] == d),:]
            
            for index, row in df_subset.iterrows():
                
                new_row = {
                    "patient_id": row["patient_id"],
                    "DOB": row["dob"],
                    "sample_date": d,
                    "AST": np.nan,
                    "ALT": np.nan,
                }

                if row["alt_numeric_value_date"] ==d:
                    new_row["ALT"] = row["alt_numeric_value"]
                
                if row["ast_numeric_value_date"] ==d:
                    new_row["AST"] = row["ast_numeric_value"]

             
                rows.append(new_row)

df_summary = pd.DataFrame(rows)
df_summary.to_csv(OUTPUT_DIR / "weekly/joined/isaric/input.csv.gz")

                