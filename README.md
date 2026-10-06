# AeroFlow — Manufacturing Performance & Data Analytics Dashboard

AeroFlow is a personal data analytics project designed to monitor manufacturing performance through interactive dashboards.

The project simulates an industrial manufacturing environment and transforms raw production, quality and planning data into meaningful KPIs to support performance monitoring and decision-making.

> **Note:** This project uses synthetic data generated with Python. It is a personal portfolio project and does not use confidential or proprietary industrial data.

---

## Overview

In an industrial environment, production teams need to monitor whether manufacturing activities are meeting their targets and identify potential performance degradation.

AeroFlow addresses this problem by centralizing production, quality and planning data into a single interactive dashboard.

The dashboard allows users to:

- Monitor production achievement against targets
- Track quality indicators and defect rates
- Monitor average production cycle time
- Analyze production delays
- Compare performance across production lines
- Visualize KPI evolution over time
- Identify lines showing a degradation in performance

The objective is not to automatically determine the root cause of a problem, but to highlight abnormal or deteriorating performance so that further investigation can be carried out.

---

## Project Objectives

The main objectives of AeroFlow are to:

1. Generate and structure industrial-like data
2. Clean and combine multiple data sources
3. Calculate relevant manufacturing KPIs
4. Build interactive data visualizations
5. Detect potential performance degradation
6. Provide a clear dashboard for operational monitoring

---

## Data Pipeline

The project follows a simple data analytics pipeline:

text
Raw data
   │
   ├── Production data
   ├── Quality data
   └── Planning data
   │
   ▼
Data processing
Python/Pandas
   │
   ▼
 KPI calculation
   │
   ▼
Interactive dashboard
Streamlit + Plotly
   │
   ▼
Performance monitoring
    & alerts





The project therefore covers the main stages of a small Data Analytics workflow:

data generation → data processing → KPI calculation → visualization → performance analysis

Manufacturing Scenario

The project simulates a fictional industrial manufacturing environment with three production lines:

LINE_A
LINE_B
LINE_C

The dataset also contains three fictitious product categories:

A320
A330
A350

The product names are used only to create an aerospace-inspired manufacturing scenario.

They do not represent real Airbus production data.

Simulated performance degradation

To demonstrate the monitoring capabilities of the dashboard, a controlled performance degradation is introduced on LINE_B after March 20, 2027.

During this period:

Production achievement decreases
Cycle time increases
Defect rate increases
Production delays increase

The purpose is to simulate a situation where several operational indicators begin to deteriorate.

AeroFlow can then make this degradation visible through its KPIs and visualizations.

Key Performance Indicators

AeroFlow calculates several KPIs to monitor production performance.

Production Achievement

Measures actual production compared with the production target.

Production Achievement =
Units Produced / Target Units × 100

A value close to 100% means that the production target is being achieved.

Defect Rate

Measures the proportion of defective units among inspected units.

Defect Rate =
Defective Units / Inspected Units × 100

A lower defect rate indicates better quality performance.

Quality Rate

The dashboard also presents a quality rate derived from the defect rate.

Quality Rate =
100 - Defect Rate
Rework Rate

Measures the proportion of inspected units requiring rework.

Rework Rate =
Rework Units / Inspected Units × 100
Schedule Achievement

Compares actual production with planned production.

Schedule Achievement =
Actual Units / Planned Units × 100

This indicator helps monitor whether production is keeping pace with the planning target.

Cycle Time

Measures the average time required to produce a unit.

An increase in cycle time can indicate a potential degradation in production performance.

Production Delays

Measures production delays in hours.

This indicator helps identify situations where production is falling behind the expected schedule.

Dashboard

The AeroFlow dashboard is organized into several sections.

Production

The production section provides visual monitoring of:

Production versus target
Production achievement
Performance by production line
KPI evolution over time

This allows users to quickly identify differences between expected and actual production.

Quality & Operations

This section focuses on operational and quality indicators, including:

Quality rate
Defect rate
Rework rate
Cycle time
Production delays

These indicators provide a broader view of manufacturing performance rather than focusing only on production volume.

Data

The data section provides access to the processed operational dataset.

Users can inspect the calculated indicators and export the processed data as CSV for further analysis.

Filters

The dashboard allows the user to filter the analysis according to the available operational dimensions.

The main filters include:

Date
Production line
Product

This makes it possible to move from an overall performance view to a more specific analysis.

For example:

All production lines
        ↓
     LINE_B
        ↓
March 20 → March 30

This can help investigate a specific period or production line.

Technologies
Programming & Data Analytics
Python
Pandas
NumPy
Data Visualization
Plotly
Dashboard
Streamlit
Data Storage
CSV
Development Tools
Visual Studio Code
Git
GitHub
Project Structure
AeroFlow/
│
├── data/
│   ├── production.csv
│   ├── quality.csv
│   └── planning.csv
│
├── src/
│   ├── generate_data.py
│   └── data_processing.py
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│
├── README.md
├── requirements.txt
└── .gitignore
data/

Contains the datasets used by the project.

production.csv — production volumes, targets and cycle time
quality.csv — inspected units, defective units and rework
planning.csv — planned production, actual production and delays
src/

Contains the data generation and processing scripts.

generate_data.py — generates the synthetic datasets
data_processing.py — loads, merges and transforms the datasets and calculates the KPIs
dashboard/

Contains the Streamlit dashboard.

app.py — main dashboard application
notebooks/

Reserved for exploratory data analysis and future experimentation.

*Installation

1. Clone the repository

git clone https://github.com/YOUR_USERNAME/AeroFlow.git
cd AeroFlow

2. Create a virtual environment

python -m venv .venv

3. Activate the virtual environment

On Windows PowerShell:
.venv\Scripts\Activate.ps1

On macOS/Linux:
source .venv/bin/activate

4. Install dependencies

pip install -r requirements.txt
Generate the Data

The project includes a Python script for generating the synthetic datasets.

Run:

python src/generate_data.py

The script generates:

data/production.csv
data/quality.csv
data/planning.csv

The generated datasets simulate daily manufacturing activity across the three production lines.

Process the Data

Run:

python src/data_processing.py

The processing script:

Loads the production dataset
Loads the quality dataset
Loads the planning dataset
Merges the datasets
Calculates production achievement
Calculates defect rate
Calculates rework rate
Calculates schedule achievement
Returns the processed dataset
Run the Dashboard

Start the Streamlit application:

streamlit run dashboard/app.py

Streamlit will launch the dashboard in your web browser.

The dashboard can then be used to explore the simulated manufacturing data interactively.

Example Analysis

One of the scenarios simulated by the project is the degradation of LINE_B.

*Before the simulated degradation:

Production performance  → Normal
Cycle time              → Stable
Defect rate             → Low
Delays                  → Limited

*After March 20:

Production performance  → ↓
Cycle time              → ↑
Defect rate             → ↑
Delays                  → ↑

The dashboard makes these changes visible through the different KPIs and charts.

The purpose is to demonstrate how a dashboard can help an operational team identify a potential performance issue and decide where further investigation may be needed.

Synthetic Data

All data used in AeroFlow is synthetic.

The datasets were generated with Python specifically for this project.

The synthetic data was designed to reproduce a simplified manufacturing scenario containing:

Production targets
Actual production
Quality inspections
Defective units
Rework
Production planning
Cycle time
Production delays

No confidential or proprietary industrial data is used.

In particular, this project does not use:

SAP data
Airbus production data
Skywise data
Palantir Foundry data
Confidential company information

The aerospace-inspired context is purely illustrative.

*Why Synthetic Data?

Real industrial datasets are often confidential and cannot be publicly shared.

Using synthetic data makes it possible to:

-Build a complete end-to-end analytics workflow
-Reproduce the project locally
-Publish the project on GitHub
-Demonstrate data processing and visualization skills
-Simulate specific operational scenarios
-Experiment with different performance patterns

The goal of the project is therefore to demonstrate the Data Analytics workflow and dashboard architecture, rather than to reproduce the performance of a real manufacturing company.

Future Improvements

Possible future developments include:

-Add OEE / TRS calculation
-Add more manufacturing KPIs
-Add advanced anomaly detection
-Add predictive analysis
-Add statistical monitoring
-Connect the dashboard to a relational database
-Work with larger datasets
-Add automated reporting
-Improve alert management
-Add role-based dashboard views
-Explore integration with enterprise data platforms
-Explore real public industrial datasets
-Deploy the dashboard online
-What This Project Demonstrates

AeroFlow demonstrates practical skills in:

-Python programming
-Data generation
-Data cleaning
-Data integration
-Data transformation
-KPI calculation
-Exploratory data analysis
-Interactive data visualization
-Dashboard development
-Performance monitoring
-Git and GitHub
-Communicating data through visual interfaces

The project also illustrates how raw operational data can be transformed into information that supports decision-making.

Project Context

AeroFlow was developed as a personal portfolio project to explore the application of Data Analytics to industrial performance monitoring.


The project is particularly interested in the following workflow:

Raw operational data
        ↓
Data transformation
        ↓
KPI calculation
        ↓
Visualization
        ↓
Performance monitoring
        ↓
Decision support



The project is not intended to reproduce a real company's internal systems.


Author : Islem Souissi - L3 MIAGE - Université Côte d'Azur





This project is intended for educational and portfolio purposes.
