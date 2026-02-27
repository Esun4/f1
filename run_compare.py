import fastf1
import pandas as pd
from pathlib import Path
from src.data_loader import get_fastest, get_telemetry
from src.preprocess import clean_telem, create_grid, align_to_grid
from src.visualize import plot_one, plot_compare, compute_delta, plot_delta_curve
from src.features import compute_lap, compute_pair_features
from src.baseline_model import compute_score, predict_winner, actual_winner

fastf1.Cache.enable_cache("/Users/ethan/Documents/coding/F1_telem/cache/fastf1")

session = fastf1.get_session(2024, 8, 'Q')

session.load()

print(session.name)
print(session.event['EventName'])
print(session.date)

drivers = ['LEC', 'HAM']
driver_telems = {}
times = []

for i in drivers:
    driver, team, lap = get_fastest(i, session)
    print(f"Driver: {driver} for {team}")
    total_seconds = lap.loc['LapTime'].total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds - 60 * minutes
    lap_str = f"{minutes}:{seconds:06.3f}"
    times.append(total_seconds)
    print(f"Time: {lap_str}")
    print(f"Lap Number: {lap.loc['LapNumber']}")
    print(f"Tire Compound: {lap.loc['Compound']}")
    
    telem = get_telemetry(lap)
    cleaned = clean_telem(telem)
    driver_telems[driver] = cleaned
    print("\n")


# creating a grid
grid = create_grid(driver_telems['Charles Leclerc'], driver_telems['Lewis Hamilton'])

# aligned dataframes for both drivers
alignedA = align_to_grid(driver_telems['Charles Leclerc'], grid)
alignedB = align_to_grid(driver_telems['Lewis Hamilton'], grid)

# Distance vs Speed plot
plot_compare(alignedA, alignedB, y_col="Speed", labelA='LEC', labelB='HAM', title="SVD")

# Distance vs Throttle plot
plot_compare(alignedA, alignedB, y_col="Throttle", labelA='LEC', labelB='HAM', title="TVD")

# Distance vs Brake plot
plot_compare(alignedA, alignedB, y_col="Brake", labelA='LEC', labelB='HAM', title="BVD")

# craete the deltaplot and save the image
delta_df = compute_delta(alignedA, alignedB)
plot_delta_curve(delta_df, labelA="LEC", labelB="HAM")

# this is the final delta value
approx_delta = delta_df["delta_s"].iloc[-1]

max_gain = float(delta_df["delta_s"].min())
max_loss = float(delta_df["delta_s"].max())

gain_index = delta_df['delta_s'].idxmin()
gain_peak_distance = float(delta_df.loc[gain_index, "Distance"])
loss_index = delta_df["delta_s"].idxmax()
loss_peak_distance = float(delta_df.loc[loss_index, "Distance"])

featA = compute_lap(alignedA)
featB = compute_lap(alignedB) 

pair_feats = compute_pair_features(featA, featB)

year = session.event.year
event_name = session.event['EventName']
session_name = session.name

driverA = drivers[0]
driverB = drivers[1]
driverA_name = "Charles Leclerc"
driverB_name = "Lewis Hamilton"

lap_time_A_s = float(times[0])
lap_time_B_s = float(times[1])
target_delta_s = lap_time_A_s - lap_time_B_s

delta_summaries = {
    "approx_delta_s": float(approx_delta),
    "target_delta_s": float(target_delta_s),
    "max_gain_s": float(max_gain),
    "max_loss_s": float(max_loss),
    "gain_peak_distance_m": float(gain_peak_distance),
    "loss_peak_distance_m": float(loss_peak_distance),
}

identifiers = {
    "year": year,
    "event_name": event_name,
    "session_name": session_name,
    "driverA_code": driverA,
    "driverB_code": driverB,
    "driverA_name": driverA_name,
    "driverB_name": driverB_name,
    "lap_time_A_s": lap_time_A_s,
    "lap_time_B_s": lap_time_B_s,
}

row = {}
row.update(identifiers)
row.update(pair_feats)
row.update(delta_summaries)


predicted = compute_score(pair_feats)
predicted_winner = predict_winner(predicted)
actual = actual_winner(target_delta_s)

baseline_correct = predicted_winner == actual

print(f"Baseline score: {predicted}")
print(f"Predicted winner: {predicted_winner}")
print(f"Actual winner: {actual}")
print(f"Baseline correct: {baseline_correct}")

baseline_results = {
    "baseline_score": float(predicted),
    "predicted_winner": predicted_winner,
    "actual_winner": actual,
    "baseline_correct": baseline_correct,
}

row.update(baseline_results)

# create outputs/tables if it doesn't exist
out_dir = Path("outputs") / "tables"
out_dir.mkdir(parents=True, exist_ok=True)

dataset_path = out_dir / "dataset.csv"

# make a one-row dataframe from the current run
df_row = pd.DataFrame([row])

# columns that define one unique comparison
key_cols = ["year", "event_name", "session_name", "driverA_code", "driverB_code"]

if dataset_path.exists():
    # load old dataset
    existing_df = pd.read_csv(dataset_path)

    # combine old + new
    combined_df = pd.concat([existing_df, df_row], ignore_index=True)

    # if the same comparison already exists, keep the LAST one (the new run)
    combined_df = combined_df.drop_duplicates(subset=key_cols, keep="last")

    # save cleaned dataset back
    combined_df.to_csv(dataset_path, index=False)
else:
    # first run: just create the file
    df_row.to_csv(dataset_path, index=False)

print(f"\nSaved comparison row to: {dataset_path}")