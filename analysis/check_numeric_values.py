import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
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
        if file.name == "input_2017-04-01.csv.gz"
        df = pd.read_csv(
            (OUTPUT_DIR / "monthly/joined") / file.name, parse_dates=["dob"]
        )
        date = get_date_input_file(file.name)
        
        plt.boxplot(df["alt_numeric_value"])
        plt.savefig(OUTPUT_DIR/"alt_check.png")