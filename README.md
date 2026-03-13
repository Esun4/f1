# F1 Telemetry Driver Performance Analysis

A machine learning pipeline that models F1 qualifying lap time deltas between driver pairs using telemetry data. The project uses telemetry-derived features from the same qualifying session to estimate lap time differences and identify which driver was faster.

---

## Overview

Given two drivers from the same qualifying session, the model answers: **based on how each driver drove their fastest lap, who was faster and by how much?**

The pipeline:
1. Ingests raw F1 telemetry via the [FastF1](https://docs.fastf1.dev/) API
2. Cleans and aligns multi-driver telemetry to a common distance grid
3. Engineers speed, throttle, and braking features for each lap
4. Builds a labeled dataset of pairwise driver comparisons across multiple race weekends
5. Trains a Random Forest regression model to estimate lap time delta between driver pairs
6. Evaluates performance using grouped train/test splits by race weekend

---

## Overview of the Approach

For each qualifying session, the pipeline finds drivers with valid clean laps. For every driver pairing, it:

- extracts the fastest clean lap for each driver
- retrieves and cleans the telemetry data
- aligns both drivers' telemetry to a shared distance grid
- computes per-lap features and pairwise feature differences
- records the actual lap time delta as the target

This project is best interpreted as a **same-session telemetry analysis and performance modeling tool**, rather than a forward-looking predictor across different sessions.

---

## Project Structure

```text
f1/
├── src/
│   ├── data_loader.py       # FastF1 lap retrieval and telemetry extraction
│   ├── preprocess.py        # Telemetry cleaning and grid alignment
│   ├── features.py          # Per-lap and pairwise feature engineering
│   ├── pipeline.py          # Builds one comparison row from a qualifying session
│   ├── visualize.py         # Speed, throttle, brake, and delta plots
│   ├── baseline_model.py    # Optional baseline utilities
│   └── checking_data.py     # Model training and evaluation
├── outputs/
│   ├── tables/              # Generated dataset CSVs
│   └── figures/             # Generated plots
├── run_compare.py           # Main script to build the dataset
├── requirements.txt
└── README.md
```

---

## Features

All pairwise features are computed as **Driver A minus Driver B** differences.

| Feature | Description |
|---|---|
| `mean_speed_diff` | Difference in average speed over the lap |
| `top_speed_diff` | Difference in maximum speed |
| `min_speed_diff` | Difference in minimum speed |
| `std_speed_diff` | Difference in speed variability |
| `full_throttle_diff` | Difference in percentage of lap at full throttle (>95%) |
| `pct_brake_diff` | Difference in percentage of lap spent braking |
| `avg_throttle_diff` | Difference in average throttle application |
| `brake_event_diff` | Difference in number of distinct braking zones |

---

## Target

The regression target is the lap time delta between the two drivers:

```text
target_delta_s = lap_time_A_s - lap_time_B_s
```

- Negative values mean **Driver A was faster**
- Positive values mean **Driver B was faster**

The model also supports a derived winner prediction task by checking the sign of the predicted delta.

---

## Model and Evaluation

The current model is a `RandomForestRegressor` trained on telemetry-based pairwise features.

To avoid leaking information between rows from the same race weekend, evaluation uses `GroupShuffleSplit`, grouping by qualifying session / event. This ensures that entire sessions are held out together during testing.

Reported metrics include:

- **MAE** — mean absolute error in seconds
- **RMSE** — root mean squared error
- **R²** — variance explained
- **Winner prediction accuracy** — percentage of driver pairs where the model correctly predicts who was faster

Example grouped split output from the current version:

- **MAE:** 0.2228 s
- **RMSE:** 0.3222 s
- **R²:** 0.7229
- **Winner prediction accuracy:** 98.95%

---

## Setup

### Requirements

- Python 3.9+
- See `requirements.txt` for the full dependency list

### Installation

```bash
git clone https://github.com/Esun4/f1.git
cd f1
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Cache Setup

FastF1 caches session data locally to avoid repeated API calls. Create a cache directory and update the path in `run_compare.py`:

```python
fastf1.Cache.enable_cache("path/to/your/cache")
```

---

## Usage

### Build the Dataset

```bash
python run_compare.py
```

This loops through the specified qualifying rounds, generates all valid driver pairings, and writes the comparison dataset to `outputs/tables/dataset.csv`.

### Train and Evaluate the Model

```bash
python src/checking_data.py
```

This prints grouped train/test split information, regression metrics, and winner prediction accuracy on the held-out test sessions.

---

## Current Results

On held-out qualifying sessions, the current version produces strong same-session performance:

- **MAE:** 0.2228 s
- **RMSE:** 0.3222 s
- **R²:** 0.7229
- **Winner prediction accuracy:** 98.95%

These results show that telemetry-derived lap features capture a large amount of the variation in within-session lap time differences.

---

## Limitations

This project currently uses telemetry features and lap-time targets derived from the **same qualifying session**. That makes it better suited for **same-session performance modeling and telemetry analysis** than for true future-session forecasting.

A future extension would be to restructure the pipeline so that earlier-session telemetry is used to predict later-session performance.

---

## Dependencies

Key packages:

- [`fastf1`](https://docs.fastf1.dev/) — F1 session and telemetry data
- `pandas`, `numpy` — data manipulation and numerical operations
- `scikit-learn` — model training and evaluation
- `matplotlib` — telemetry and delta visualizations

---

## License
