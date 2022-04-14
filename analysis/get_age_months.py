import pandas as pd
from datetime import datetime
from utilities import OUTPUT_DIR, match_input_files, get_date_input_file

dob = pd.read_csv(OUTPUT_DIR / "input_dob.csv.gz")

for file in (OUTPUT_DIR / "monthly").iterdir():
    if match_input_files(file.name):
        df = pd.read_csv((OUTPUT_DIR / "monthly/joined") / file.name)
        date = get_date_input_file(file.name)


        
