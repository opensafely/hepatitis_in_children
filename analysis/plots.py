import pandas as pd
from utilities import OUTPUT_DIR, ANALYSIS_DIR, plot_measures, redact_small_numbers

for frequency in ["monthly", "weekly"]:
    for test in ["alt", "ast", "bilirubin", "gi_illness"]:
        
        # plot rates
        df = pd.read_csv(
            OUTPUT_DIR / f"{frequency}/measure_{test}_rate.csv", parse_dates=["date"]
        )
        df["rate"] = df[f"value"] * 100

        plot_measures(
            df=df,
            filename=f"{frequency}/plot_{test}",
            title=test,
            column_to_plot="rate",
            y_label="Proportion",
            as_bar=False,
        )

        # plot out of range rates
        if test in ["alt", "ast", "bilirubin"]:
            df_oor = pd.read_csv(
                OUTPUT_DIR / f"{frequency}/measure_{test}_oor_rate.csv",
                parse_dates=["date"],
            )
            df_oor["rate"] = df_oor[f"value"] * 100

            plot_measures(
                df=df_oor,
                filename=f"{frequency}/plot_{test}_oor",
                title=test,
                column_to_plot="rate",
                y_label="Proportion",
                as_bar=False,
            )

            for d in ["age_band", "region"]:
                demographic_df = pd.read_csv(
                    OUTPUT_DIR / f"monthly/measure_{test}_{d}_rate.csv",
                    parse_dates=["date"],
                )
                if d == "age_band":
                    demographic_df = demographic_df[demographic_df["age_band"] != "missing"]

                elif d == "region":
                    demographic_df = demographic_df[demographic_df["region"].notnull()]

                demographic_df["rate"] = demographic_df[f"value"] * 100
                demographic_df = redact_small_numbers(
                    demographic_df, 10, test, "population", "rate", "date"
                )

                plot_measures(
                    df=demographic_df,
                    filename=f"{frequency}/plot_{test}_{d}",
                    title=f"{test} by {d}",
                    column_to_plot="rate",
                    y_label="Proportion",
                    as_bar=False,
                    category=d,
                )
