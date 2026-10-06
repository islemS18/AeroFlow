import pandas as pd
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_data():

    production = pd.read_csv(
        DATA_DIR / "production.csv",
        parse_dates=["date"]
    )

    quality = pd.read_csv(
        DATA_DIR / "quality.csv",
        parse_dates=["date"]
    )

    planning = pd.read_csv(
        DATA_DIR / "planning.csv",
        parse_dates=["date"]
    )

    return production, quality, planning


def prepare_data():

    production, quality, planning = load_data()

    df = production.merge(
        quality,
        on=["date", "line", "product"],
        how="left"
    )

    df = df.merge(
        planning,
        on=["date", "line", "product"],
        how="left"
    )

    # KPI production
    df["production_rate"] = (
        df["units_produced"] / df["target_units"] * 100
    )

    # KPI qualité
    df["defect_rate"] = (
        df["defective_units"] / df["units_inspected"] * 100
    )

    # KPI retouche
    df["rework_rate"] = (
        df["rework_units"] / df["units_inspected"] * 100
    )

    # KPI respect du planning
    df["schedule_rate"] = (
        df["actual_units"] / df["planned_units"] * 100
    )

    return df



if __name__ == "__main__":

    df = prepare_data()

    print(df.head())
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nAverage production rate:")
    print(df["production_rate"].mean())

    print("\nAverage defect rate:")
    print(df["defect_rate"].mean())