import fastf1
import pandas as pd
from pathlib import Path
from src.pipeline import build_comparison_row
from src.data_loader import get_fastest

fastf1.Cache.enable_cache("/Users/ethan/Documents/coding/F1_telem/cache/fastf1")

sessions = [1, 2, 3, 4, 5]

# create a loop to go through the sessions

for i in sessions:
    session = fastf1.get_session(2024, i, 'Q') # this goes through the list of sessions and gets the qualifying session for each race

    session.load()

    driver_numbers = session.drivers

    rows = []
    driver_list = []
    for num in driver_numbers:
        driver_list.append(session.get_driver(num)["Abbreviation"])

    # remove duplicates
    driver_list = list(dict.fromkeys(driver_list))

    valid_drivers = []

    # find the valid drivers
    for ID in driver_list:
        if get_fastest(ID, session) is not None:
            valid_drivers.append(ID)
        else:
            print(f"Skipping {ID}: no valid clean lap")

    print(f"Valid drivers in session: {len(valid_drivers)}")

    for i in range(len(valid_drivers)):
        for j in range(i + 1, len(valid_drivers)):
            try:
                print(f"Processing {valid_drivers[i]} and {valid_drivers[j]}")
                row = build_comparison_row(session, valid_drivers[i], valid_drivers[j], mk_plot=False)
                rows.append(row)
            except Exception as e:
                print(f"The pair {valid_drivers[i]} and {valid_drivers[j]} failed")
                print(f"Error: {e}")
                print(f"Skipping {valid_drivers[i]} and {valid_drivers[j]}")
                continue

    # create outputs/tables if it doesn't exist
    out_dir = Path("outputs") / "tables"
    out_dir.mkdir(parents=True, exist_ok=True)

    dataset_path = out_dir / "dataset.csv"

    if not rows:
        print("No rows were generated.")
    else:
        # coverts the rows into a dataframe
        session_df = pd.DataFrame(rows)


        # columns that define one unique comparison
        key_cols = ["year", "event_name", "session_name", "driverA_code", "driverB_code"]

        if dataset_path.exists():
            existing_df = pd.read_csv(dataset_path)

            combined_df = pd.concat([existing_df, session_df], ignore_index=True)

            # keep the newest copy of any repeated comparison
            combined_df = combined_df.drop_duplicates(subset=key_cols, keep="last")

            combined_df.to_csv(dataset_path, index=False)
        else:
            session_df.to_csv(dataset_path, index=False)

        print(f"Saved dataset to: {dataset_path}")
        print(f"Rows saved this run: {len(session_df)}")
