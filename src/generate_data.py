import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

dates = pd.date_range("2027-03-01", "2027-03-30")

lines = ["LINE_A", "LINE_B", "LINE_C"]
products = ["A320", "A330", "A350"]

production_rows = []
quality_rows = []
planning_rows = []

for date in dates:
    for line in lines:

        product = np.random.choice(products)

        # Valeurs normales
        target = np.random.randint(130, 170)
        cycle_time = np.random.normal(42, 2)

        # Dégradation volontaire de LINE_B après le 20 mars
        if line == "LINE_B" and date.day >= 20:
            production = int(target * np.random.uniform(0.75, 0.90))
            cycle_time += np.random.uniform(7, 12)
            defect_rate = np.random.uniform(0.035, 0.06)
            delay = np.random.randint(4, 10)

        else:
            production = int(target * np.random.uniform(0.90, 1.05))
            defect_rate = np.random.uniform(0.008, 0.025)
            delay = np.random.randint(0, 4)

        inspected = max(production, int(production * np.random.uniform(0.90, 1.0)))
        defective = int(inspected * defect_rate)
        rework = int(defective * np.random.uniform(0.2, 0.5))

        production_rows.append({
            "date": date,
            "line": line,
            "product": product,
            "units_produced": production,
            "target_units": target,
            "cycle_time_min": round(cycle_time, 2)
        })

        quality_rows.append({
            "date": date,
            "line": line,
            "product": product,
            "units_inspected": inspected,
            "defective_units": defective,
            "rework_units": rework
        })

        planning_rows.append({
            "date": date,
            "line": line,
            "product": product,
            "planned_units": target,
            "actual_units": production,
            "delay_hours": delay
        })


production = pd.DataFrame(production_rows)
quality = pd.DataFrame(quality_rows)
planning = pd.DataFrame(planning_rows)

production.to_csv(DATA_DIR / "production.csv", index=False)
quality.to_csv(DATA_DIR / "quality.csv", index=False)
planning.to_csv(DATA_DIR / "planning.csv", index=False)

print("Data generated successfully!")
print(f"Production: {len(production)} rows")
print(f"Quality: {len(quality)} rows")
print(f"Planning: {len(planning)} rows")