# F1 Telemetry Driver Performance Predictor

A machine learning pipeline that predicts F1 qualifying lap time deltas between driver pairs using telemetry data. The model uses Q1 session telemetry features (speed, throttle, braking) to predict Q2 lap time deltas for the same driver pairings, making it a genuinely predictive cross-session model.

---

## Overview

Given two drivers who both competed in Q1 and Q2 of the same qualifying session, the model answers: **based on how each driver drove in Q1, who will be faster in Q2 and by how much?**

The pipeline:
1. Ingests raw F1 telemetry via the [FastF1](https://docs.fastf1.dev/) API
2. Cleans and aligns multi-driver telemetry to a common distance grid
3. Engineers speed, throttle, and braking features per driver
4. Builds a labeled dataset of pairwise driver comparisons across multiple race weekends
5. Trains a Random Forest regression model to predict Q2 lap time delta
6. Evaluates against a hand-tuned weighted baseline model

---

## Project Structure
```
f1/
├── src/
│   ├── data_loader.py       # FastF1 session and lap retrieval
│   ├── preprocess.py        # Telemetry cleaning and grid alignment
│   ├── features.py          # Per-lap and pairwise feature engineering
│   ├── pipeline.py          # Builds one comparison row from two sessions
│   ├── baseline_model.py    # Hand-tuned weighted scoring baseline
│   ├── visualize.py         # Speed, throttle, brake, and delta plots
│   └── checking_data.py     # Model training and evaluation
├── notebooks/
│   └── exploration.ipynb    # Exploratory analysis
├── outputs/
│   ├── tables/              # Generated dataset CSV
│   └── figures/             # Generated plots
├── run_compare.py           # Main script to build the dataset
├── requirements.txt
└── README.md
```

---

## How It Works

### Data Pipeline

For each race weekend, the pipeline loads both the Q1 and Q2 sessions. It finds all drivers who have a valid clean lap in **both** sessions (drivers eliminated in Q1 are excluded). For every valid driver pairing it:

- Extracts the fastest clean lap from Q1 for each driver
- Retrieves and cleans the telemetry (distance, speed, throttle, brake)
- Aligns both drivers' telemetry to a common 1000-point distance grid using linear interpolation
- Computes per-lap features and pairwise feature differences
- Records the Q2 lap time delta as the prediction target

### Features

All features are computed as **Driver A minus Driver B** differences:

| Feature | Description |
|---|---|
| `mean_speed_diff` | Difference in average speed over the lap |
| `top_speed_diff` | Difference in maximum speed |
| `min_speed_diff` | Difference in minimum speed |
| `std_speed_diff` | Difference in speed variance |
| `full_throttle_diff` | Difference in % of lap at full throttle (>95%) |
| `avg_throttle_diff` | Difference in average throttle application |
| `brake_event_diff` | Difference in number of distinct braking zones |
| `q1_lap_time_diff` | Difference in Q1 lap times (seconds) |

### Target

`target_delta_s = lap_time_A_q2 - lap_time_B_q2`

Negative values mean Driver A was faster in Q2, positive means Driver B was faster.

### Model

A `RandomForestRegressor` trained on pairwise telemetry features from Q1 to predict Q2 lap time delta. Evaluation uses `GroupShuffleSplit` to ensure entire race weekends are held out during testing, preventing data leakage across sessions from the same event.

Metrics reported:
- **MAE** — mean absolute error in seconds
- **RMSE** — root mean squared error
- **R²** — variance explained
- **Winner prediction accuracy** — percentage of pairs where the model correctly predicts which driver was faster in Q2, compared against baseline accuracy

---

## Setup

### Requirements

- Python 3.9+
- See `requirements.txt` for full dependencies

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

This loops through the specified race rounds, loads Q1 and Q2 for each, generates all valid driver pairings, and appends results to `outputs/tables/dataset.csv`. Duplicate comparisons are automatically deduplicated on re-runs.

### Train and Evaluate the Model
```bash
python src/checking_data.py
```

Outputs MAE, RMSE, R², baseline accuracy, ML accuracy, and the improvement over baseline on the held-out test set.

---

## Results

The model is evaluated on race weekends fully held out from training (group-based split). Winner prediction accuracy is compared against a hand-tuned weighted baseline that scores pairs using fixed weights on the telemetry features.

Expected accuracy range: **65–80%** — lower than a naive same-session model by design, since cross-session prediction is a genuinely harder problem.

---

## Dependencies

Key packages:

- [`fastf1`](https://docs.fastf1.dev/) — F1 session and telemetry data
- `pandas`, `numpy` — data manipulation and grid alignment
- `scikit-learn` — Random Forest model and evaluation
- `matplotlib` — telemetry and delta visualizations

---

## License