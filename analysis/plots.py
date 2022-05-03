import pandas as pd
from pathlib import Path
from ebmdatalab import charts
from utilities import (
    OUTPUT_DIR, 
    ANALYSIS_DIR, 
    plot_measures, 
    redact_small_numbers, 
    convert_binary,
    calculate_rate
)

Path("output/monthly/joined/redacted").mkdir(parents=True, exist_ok=True)
Path("output/weekly/joined/redacted").mkdir(parents=True, exist_ok=True)

for frequency in ["monthly", "weekly"]:
    for test in ["alt", "ast", "bilirubin", "gi_illness"]:

        # plot rates
        df = pd.read_csv(
            OUTPUT_DIR / f"{frequency}/joined/measure_{test}_rate.csv", parse_dates=["date"]
        )
        df["rate"] = calculate_rate(df, "value")
        df = redact_small_numbers(
                    df, 5, test, "population", "rate", "date"
                )
        df.to_csv(
            OUTPUT_DIR / f"{frequency}/joined/redacted/measure_{test}_rate.csv", index=False
        )
        plot_measures(
            df=df,
            filename=f"{frequency}/plot_{test}",
            column_to_plot="rate",
            title="",
            y_label="Rate per 1000",
            as_bar=False,
        )

        # plot count
        plot_measures(
            df=df,
            filename=f"{frequency}/joined/plot_{test}_count",
            column_to_plot=test,
            title="",
            y_label="Count",
            as_bar=False,
        )

        # deciles chart
        df_practice = pd.read_csv(
            OUTPUT_DIR / f"{frequency}/joined/measure_{test}_practice_rate.csv",
            parse_dates=["date"],
        )
        df_practice["rate"] = calculate_rate(df_practice, "value")
        print(df_practice)
        decile_chart = charts.deciles_chart(
            df_practice,
            period_column="date",
            column="rate",
            show_outer_percentiles=False,
            ylabel="Rate per 1000",
        )
        decile_chart.savefig(
            OUTPUT_DIR / f"{frequency}/joined/deciles_chart_{test}.png", bbox_inches="tight"
        )

        # plot out of range rates
        if test in ["alt", "ast", "bilirubin"]:
            if test == "bilirubin":
                input_file = f"{frequency}/joined/measure_{test}_oor_ref_rate.csv"
                numerator = f"{test}_numeric_value_out_of_ref_range"
                output_file = f"measure_{test}_oor_ref_rate.csv"
            else:
                input_file = f"{frequency}/joined/measure_{test}_oor_rate.csv"
                numerator = f"{test}_numeric_value_out_of_range"
                output_file = f"measure_{test}_oor_rate.csv"
            
            df_oor = pd.read_csv(
                OUTPUT_DIR / input_file,
                parse_dates=["date"],
            )
            df_oor = redact_small_numbers(
                df_oor, 5, numerator, test, "value", "date"
            )
            df_oor.to_csv(
                OUTPUT_DIR / f"{frequency}/joined/redacted/{output_file}", index=False
            )
            
            df_oor["rate"] = calculate_rate(df_oor,"value")
            
            plot_measures(
                df=df_oor,
                filename=f"{frequency}/joined/plot_{test}_oor",
                column_to_plot="rate",
                title="",
                y_label="Rate per 1000",
                as_bar=False,
            )

            # plot counts
            plot_measures(
                df=df_oor,
                filename=f"{frequency}/joined/plot_{test}_oor_count",
                column_to_plot=numerator,
                title="",
                y_label="Count",
                as_bar=False,
            )
            

            # chart for those with recent test and out of range

    
            df_oor_cov = pd.read_csv(
                OUTPUT_DIR / f"{frequency}/joined/measure_{test}_oor_recent_cov_rate.csv",
                parse_dates=["date"],
            )

            df_oor_cov = redact_small_numbers(
                df_oor_cov, 5, numerator, test, "value", "date"
            )
            
            df_oor_cov.to_csv(
                OUTPUT_DIR / f"{frequency}/joined/redacted/measure_{test}_oor_recent_cov_rate.csv",index=False
            )

            df_oor_cov["rate"] = calculate_rate(df_oor_cov, "value")

            convert_binary(df_oor_cov, "recent_positive_covid_test", "Yes", "No")

                        
            plot_measures(
                df=df_oor_cov,
                filename=f"{frequency}/joined/plot_{test}_oor_recent_cov",
                column_to_plot="rate",
                title="",
                y_label="Rate per 1000",
                as_bar=False,
                category="recent_positive_covid_test",
            )

            # plot count
            plot_measures(
                df=df_oor_cov,
                filename=f"{frequency}/joined/plot_{test}_oor_recent_cov_count",
                column_to_plot=numerator,
                title="",
                y_label="Count",
                as_bar=False,
                category="recent_positive_covid_test",
            )
            
           
            for d in ["age_band", "region"]:
                demographic_df = pd.read_csv(
                    OUTPUT_DIR / f"{frequency}/joined/measure_{test}_{d}_rate.csv",
                    parse_dates=["date"],
                )
                if d == "age_band":
                    demographic_df = demographic_df[
                        demographic_df["age_band"] != "missing"
                    ]

                elif d == "region":
                    demographic_df = demographic_df[demographic_df["region"].notnull()]

                demographic_df["rate"] = calculate_rate(demographic_df, "value")
                demographic_df = redact_small_numbers(
                    demographic_df, 5, test, "population", "rate", "date"
                )

                demographic_df.to_csv(
                    OUTPUT_DIR / f"{frequency}/joined/redacted/measure_{test}_{d}_rate.csv",index=False
                )

                plot_measures(
                    df=demographic_df,
                    filename=f"{frequency}/joined/plot_{test}_{d}",
                    column_to_plot="rate",
                    title="",
                    y_label="Rate per 1000",
                    as_bar=False,
                    category=d,
                )

                #count

                plot_measures(
                    df=demographic_df,
                    filename=f"{frequency}/joined/plot_{test}_{d}_count",
                    column_to_plot=test,
                    title="",
                    y_label="Count",
                    as_bar=False,
                    category=d,
                )
