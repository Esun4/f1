
# this function cleans the telemetry data
def clean_telem(telem):
    sorted_telem = telem.sort_values(by='Distance')
    no_dups = sorted_telem.drop_duplicates(inplace=True)
    print(f"this: {no_dups}")
    # no_nan = no_dups.dropna(inplace=True)
    # final = no_dups[['Distance', 'Speed', 'Throttle', 'Brake', 'X', 'Y', 'Time']]
    # return sorted_telem

# pass the cleaned data into this function
def create_grid(driver1, driver2):
    maxA = driver1['Distance'].max()
    maxB = driver2['Distance'].max()