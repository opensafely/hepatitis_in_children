import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from utilities import (
    OUTPUT_DIR,
)

sns.set_style("darkgrid")

def plot_measures_subplot(
    df,
    ax,
    x_label,
    column_to_plot: str,
    y_label: str,
    as_bar: bool = False,
    category: str = None,
    show_legend=True,
):
    """Produce time series plot from measures table.  One line is plotted for each sub
    category within the category column. Saves output in 'output' dir as jpeg file.
    Args:
        df: A measure table
        title: Plot title
        column_to_plot: Column name for y-axis values
        y_label: Label to use for y-axis
        as_bar: Boolean indicating if bar chart should be plotted instead of line chart. Only valid if no categories.
        category: Name of column indicating different categories
    """
    
    df = df.sort_values(by=["date", "age_band_months_sorted"])
    # mask nan values (redacted)
    mask = np.isfinite(df[column_to_plot])

    if category:
        ages = ["0-3 months", "3 months - 5 years", "6-10", "11-20", "21-30"]
        df = df[df[category].notnull()]

        for unique_category in ages:
            # subset on category column and sort by date
            df_subset = df[df[category] == unique_category].sort_values("date")

            ax.plot(
                df_subset["date"][mask],
                df_subset[column_to_plot][mask],
                marker="o",
                label=unique_category,
            )
    else:
        if as_bar:
            ax.plot.bar("date", column_to_plot, legend=False)
        else:
            ax.plot(df["date"][mask], df[column_to_plot][mask], marker="o")

    
    ax.tick_params(axis="y", labelsize=16)
    ax.set_ylabel(y_label, fontsize=18)
    

    

    
    ax.set_ylim(
        bottom=0,
        top=100
        if df[column_to_plot].isnull().values.all()
        else df[column_to_plot].max() * 1.05,
    )

    
    if x_label:
        x_labels = sorted(df["date"].unique())
        ax.set_xlabel(x_label)
        ax.set_xticks(x_labels)
        
        ax.tick_params(axis="x", labelrotation=90, labelsize=14)
        ax.set_xlabel("Date", fontsize=18)
        ax.set_xlim(x_labels[0], x_labels[-1])
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
       
    if category:
        if show_legend:
            ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left", fontsize=16)
   


# hepatitis and gi illness rates subplot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)

axes = [ax1, ax2]
for i, j in enumerate(["gi_illness", "hepatitis"]):
    df = pd.read_csv(
        OUTPUT_DIR / f"monthly/joined/redacted/measure_{j}_age_band_months_rate.csv",
        parse_dates=["date"],
    )

    if i == 0:
        show_legend = True
        x_label = None

    else:
        show_legend = False
        x_label = "Date"

    plot_measures_subplot(
        df=df,
        ax=axes[i],
        column_to_plot=j,
        x_label=x_label,
        y_label="Count",
        as_bar=False,
        category="age_band_months_sorted",
        show_legend=show_legend,
    )

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "subplot_gi_hep.png", dpi=300)


# lft rates subplot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8), sharex=True)

axes = [ax1, ax2, ax3]
for i, j in enumerate(["alt", "ast", "bilirubin"]):
    df = pd.read_csv(
        OUTPUT_DIR / f"monthly/joined/redacted/measure_{j}_age_band_months_rate.csv",
        parse_dates=["date"],
    )

    if i == 0:
        show_legend = True
        x_label = None

    elif i == 1:
        show_legend = False
        x_label = None
    else:
        show_legend = False
        x_label = "Date"

    plot_measures_subplot(
        df=df,
        ax=axes[i],
        column_to_plot="rate",
        x_label=x_label,
        y_label="Rate per 1000",
        as_bar=False,
        category="age_band_months_sorted",
        show_legend=show_legend,
    )

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "subplot_lft.png", dpi=300)


# lft oor rates subplot
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 8), sharex=True)

axes = [ax1, ax2, ax3]
for i, j in enumerate(["alt", "ast", "bilirubin"]):
    df = pd.read_csv(
        OUTPUT_DIR / f"monthly/joined/redacted/measure_{j}_oor_age_rate.csv",
        parse_dates=["date"],
    )

    df["value"] = df["value"] * 100

    if i == 0:
        show_legend = True
        x_label = None

    elif i == 1:
        show_legend = False
        x_label = None
    else:
        show_legend = False
        x_label = "Date"

    plot_measures_subplot(
        df=df,
        ax=axes[i],
        column_to_plot="value",
        x_label=x_label,
        y_label="% out of range",
        as_bar=False,
        category="age_band_months_sorted",
        show_legend=show_legend,
    )

plt.tight_layout()
plt.savefig(OUTPUT_DIR / "subplot_oor.png", dpi=300)
