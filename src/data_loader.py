import fastf1
import pandas as pd

fastf1.Cache.enable_cache("/Users/ethan/Documents/coding/F1_telem/cache/fastf1")

session = fastf1.get_session(2024, 8, 'Q')

session.load()

# function to get the fastest lap of a given driver
def get_fastest(driverId, session):
    driver = session.get_driver(driverId)['FullName']
    team = session.get_driver(driverId)['TeamName']
    laps = session.laps.pick_drivers(driverId)

    # filtering out the inaccurate and deleted laps
    acc = laps[laps['IsAccurate'] == True]
    clean_laps = acc[acc['Deleted'] == False]

    if clean_laps.empty:
        print("There are no clean laps to use")
        return None
    else:
        fastest_lap = clean_laps.pick_fastest()
        return driver, team, fastest_lap

print(session.name)
print(session.event['EventName'])
print(session.date)

drivers = ['LEC', 'HAM']

for i in drivers:
    driver, team, lap = get_fastest(i, session)
    print(f"Driver: {driver} for {team}")

