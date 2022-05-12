import pandas as pd
import numpy as np
import json
from pathlib import Path
from ebmdatalab import charts
from utilities import (
    OUTPUT_DIR,
    ANALYSIS_DIR,
    plot_measures,
    redact_small_numbers,
    convert_binary,
    calculate_rate,
    drop_irrelevant_practices,
    round_values,
)

Path("output/monthly/joined/redacted").mkdir(parents=True, exist_ok=True)
Path("output/weekly/joined/redacted").mkdir(parents=True, exist_ok=True)


for frequency in ["monthly", "weekly"]:

    for test in ["alt", "ast", "bilirubin", "gi_illness", "hepatitis"]:

        if frequency == "monthly":
            if test in ["alt", "ast", "bilirubin"]:
                mean_values = pd.read_csv(
                    OUTPUT_DIR
                    / f"{frequency}/joined/redacted/mean_test_value_{test}_by_age.csv"
                )
            
                mean_values["age_band_months_sorted"] = pd.Categorical(
                    mean_values["age_band_months"],
                    ["0-3 months", "3 months - 5 years", "6-10", "11-20", "21-30"],
                )

                mean_values = mean_values.sort_values(
                    by=["date", "age_band_months_sorted"], ascending=[True, True]
                )
                

        # plot rates
        df = pd.read_csv(
            OUTPUT_DIR / f"{frequency}/joined/measure_{test}_rate.csv",
            parse_dates=["date"],
        )

        df = redact_small_numbers(df, 5, test, "population", "value", "date", None)

        df[test] = df[test].apply(lambda x: round_values(x, base=5))

        df["population"] = df["population"].apply(lambda x: round_values(x, base=5))
        df["value"] = df[test] / df["population"]
        df["rate"] = calculate_rate(df, "value")
        df.to_csv(
            OUTPUT_DIR / f"{frequency}/joined/redacted/measure_{test}_rate.csv",
            index=False,
        )
        plot_measures(
            df=df,
            filename=f"{frequency}/joined/plot_{test}",
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
        df_practice, practice_summary = drop_irrelevant_practices(df_practice)

        with open(
            OUTPUT_DIR / f"{frequency}/joined/practice_count_{test}.json", "w"
        ) as f:
            json.dump({"num_practices": practice_summary}, f)

        decile_chart = charts.deciles_chart(
            df_practice,
            period_column="date",
            column="rate",
            show_outer_percentiles=False,
            ylabel="Rate per 1000",
        )
        decile_chart.savefig(
            OUTPUT_DIR / f"{frequency}/joined/deciles_chart_{test}.png",
            bbox_inches="tight",
        )

        # plot age band rates for hepatitis and gi illness

        if test in ["hepatitis", "gi_illness"]:
            df = pd.read_csv(
                OUTPUT_DIR
                / f"{frequency}/joined/measure_{test}_age_band_months_rate.csv",
                parse_dates=["date"],
            )

            df = redact_small_numbers(
                df, 5, test, "population", "value", "date", "age_band_months"
            )
            df[test] = df[test].apply(lambda x: round_values(x, base=5))
            df["population"] = df["population"].apply(lambda x: round_values(x, base=5))
            df["value"] = df[test] / df["population"]

            df["rate"] = calculate_rate(df, "value")

            df["age_band_months_sorted"] = pd.Categorical(
                df["age_band_months"],
                ["0-3 months", "3 months - 5 years", "6-10", "11-20", "21-30"],
            )

            df = df.sort_values(
                by=["date", "age_band_months_sorted"], ascending=[True, True]
            )
            df.to_csv(
                OUTPUT_DIR
                / f"{frequency}/joined/redacted/measure_{test}_age_band_months_rate.csv",
                index=False,
            )

           
            plot_measures(
                df=df,
                filename=f"{frequency}/joined/plot_{test}_age",
                column_to_plot="rate",
                title="",
                y_label="Rate per 1000",
                as_bar=False,
                category="age_band_months_sorted",
            )

            # plot count
            plot_measures(
                df=df,
                filename=f"{frequency}/joined/plot_{test}_count_age",
                column_to_plot=test,
                title="",
                y_label="Count",
                as_bar=False,
                category="age_band_months_sorted",
            )

        # plot out of range rates
        if test in ["alt", "ast", "bilirubin"]:

            # plot mean value
            if frequency == "monthly":
               
               plot_measures(
                    df=mean_values,
                    filename=f"{frequency}/joined/plot_{test}_mean_value",
                    column_to_plot=f"{test}_numeric_value",
                    title="",
                    y_label="Mean test value",
                    as_bar=False,
                    category="age_band_months_sorted",
                )

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

            # if ast plot quarterly numbers instead

            if test == "ast":
                df_oor = (
                    df_oor.groupby(pd.PeriodIndex(df["date"], freq="q"), axis=0)[
                        [numerator, test]
                    ]
                    .sum()
                    .reset_index()
                )
                df_oor["value"] = df_oor[numerator] / df_oor[test]
                df_oor["date"] = df_oor["date"].astype(str)

            df_oor = redact_small_numbers(
                df_oor, 5, numerator, test, "value", "date", None
            )
            df_oor[numerator] = df_oor[numerator].apply(
                lambda x: round_values(x, base=5)
            )
            df_oor[test] = df_oor[test].apply(lambda x: round_values(x, base=5))
            df_oor["value"] = df_oor[numerator] / df_oor[test]

            df_oor.to_csv(
                OUTPUT_DIR / f"{frequency}/joined/redacted/{output_file}", index=False
            )

            df_oor["rate"] = calculate_rate(df_oor, "value")

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
                OUTPUT_DIR
                / f"{frequency}/joined/measure_{test}_oor_recent_cov_rate.csv",
                parse_dates=["date"],
            )

            df_oor_cov = redact_small_numbers(
                df_oor_cov,
                5,
                numerator,
                test,
                "value",
                "date",
                "recent_positive_covid_test",
            )
            df_oor_cov[numerator] = df_oor_cov[numerator].apply(
                lambda x: round_values(x, base=5)
            )
            df_oor_cov[test] = df_oor_cov[test].apply(lambda x: round_values(x, base=5))
            df_oor_cov["value"] = df_oor_cov[numerator] / df_oor_cov[test]

            df_oor_cov.to_csv(
                OUTPUT_DIR
                / f"{frequency}/joined/redacted/measure_{test}_oor_recent_cov_rate.csv",
                index=False,
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

            # chart for those with out of range broken down by age band

            df_oor_age = pd.read_csv(
                OUTPUT_DIR
                / f"{frequency}/joined/measure_{test}_oor_age_band_months_rate.csv",
                parse_dates=["date"],
            )

            df_oor_age = redact_small_numbers(
                df_oor_age, 5, numerator, test, "value", "date", "age_band_months"
            )

            df_oor_age[numerator] = df_oor_age[numerator].apply(
                lambda x: round_values(x, base=5)
            )
            df_oor_age[test] = df_oor_age[test].apply(lambda x: round_values(x, base=5))
            df_oor_age["value"] = df_oor_age[numerator] / df_oor_age[test]

            df_oor_age["age_band_months_sorted"] = pd.Categorical(
                df_oor_age["age_band_months"],
                ["0-3 months", "3 months - 5 years", "6-10", "11-20", "21-30"],
            )

            df_oor_age = df_oor_age.sort_values(
                by=["date", "age_band_months_sorted"], ascending=[True, True]
            )

            df_oor_age.to_csv(
                OUTPUT_DIR
                / f"{frequency}/joined/redacted/measure_{test}_oor_age_rate.csv",
                index=False,
            )

            df_oor_age["rate"] = calculate_rate(df_oor_age, "value")

            plot_measures(
                df=df_oor_age,
                filename=f"{frequency}/joined/plot_{test}_oor_age",
                column_to_plot="rate",
                title="",
                y_label="Rate per 1000",
                as_bar=False,
                category="age_band_months_sorted",
            )

            # plot count
            plot_measures(
                df=df_oor_age,
                filename=f"{frequency}/joined/plot_{test}_oor_age_count",
                column_to_plot=numerator,
                title="",
                y_label="Count",
                as_bar=False,
                category="age_band_months_sorted",
            )

            for d in ["age_band_months", "region"]:
                demographic_df = pd.read_csv(
                    OUTPUT_DIR / f"{frequency}/joined/measure_{test}_{d}_rate.csv",
                    parse_dates=["date"],
                )
                if d == "age_band_months":
                    demographic_df = demographic_df[
                        demographic_df["age_band_months"] != "missing"
                    ]

                elif d == "region":
                    demographic_df = demographic_df[demographic_df["region"].notnull()]

                # if alt, combine 0-3 months and 3 months-5 yrs

                if (d == "age_band_months") & (((frequency == "weekly") & (test == "alt")) | ((test == "ast"))):
                    demographic_df.loc[
                        demographic_df["age_band_months"].isin(
                            ["0-3 months", "3 months - 5 years"]
                        ),
                        "age_band_months",
                    ] = "0-5"
                    demographic_df = demographic_df.groupby(
                        by=["date", "age_band_months"]
                    )[[test, "population"]].sum().reset_index()
                    
                    demographic_df["value"] = (
                        demographic_df[test] / demographic_df["population"]
                    )

                demographic_df["rate"] = calculate_rate(demographic_df, "value")
                demographic_df = redact_small_numbers(
                    demographic_df, 5, test, "population", "rate", "date", d
                )

                demographic_df[test] = demographic_df[test].apply(
                    lambda x: round_values(x, base=5)
                )
                demographic_df["population"] = demographic_df["population"].apply(
                    lambda x: round_values(x, base=5)
                )
                demographic_df["value"] = (
                    demographic_df[test] / demographic_df["population"]
                )

                demographic_df.to_csv(
                    OUTPUT_DIR
                    / f"{frequency}/joined/redacted/measure_{test}_{d}_rate.csv",
                    index=False,
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

                # count

                plot_measures(
                    df=demographic_df,
                    filename=f"{frequency}/joined/plot_{test}_{d}_count",
                    column_to_plot=test,
                    title="",
                    y_label="Count",
                    as_bar=False,
                    category=d,
                )
