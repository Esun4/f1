import numpy as np
import pandas as pd

# this function cleans the telemetry data
def clean_telem(telem):
    sorted_telem = telem.sort_values(by='Distance')
    sorted_telem.drop_duplicates(inplace=True)
    no_dups = sorted_telem
    no_dups.dropna(subset=['Distance'], inplace=True)
    no_nan = no_dups
    final = no_nan[['Distance', 'Speed', 'Throttle', 'Brake', 'X', 'Y', 'Time']]
    return final

# pass the cleaned data into this function
def create_grid(driver1, driver2):
    maxA = driver1['Distance'].max()
    maxB = driver2['Distance'].max()
    max_common = min(maxA, maxB)

    # when doing normalized distance
    # DistanceNorm = Distance / max_distance
    
    even_array = np.linspace(0, max_common, 1000)

    return even_array

# align a drivers telemetry to a grid
def align_to_grid(telem, grid):
    columns = ("Speed", "Throttle", "Brake", "X", "Y")

    x = telem["Distance"].to_numpy()
    
    aligned = pd.DataFrame({"Distance": grid})

    for c in columns:
        if c not in telem.columns:
            raise KeyError(f"Telemetry missing required column: {c}")
        y = telem[c].to_numpy()

        in_range = (grid >= x[0]) & (grid <= x[-1])
        y_new = np.full_like(grid, np.nan, dtype=float)
        y_new[in_range] = np.interp(grid[in_range], x, y)
        
        aligned[c] = y_new
    return aligned