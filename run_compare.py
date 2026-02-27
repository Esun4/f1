import fastf1
from src.data_loader import get_fastest, get_telemetry
from src.preprocess import clean_telem, create_grid, align_to_grid
from src.visualize import plot_one, plot_compare, compute_delta, plot_delta_curve


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

approx_delta = delta_df["delta_s"].iloc[-1]
actual_delta = times[0] - times[1]
print(approx_delta)
print(actual_delta)