import fastf1
import pandas as pd

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
        fastest = clean_laps.pick_fastest().loc['LapTime']
        return driver, team, fastest

print(session.name)
print(session.event['EventName'])
print(session.date)

drivers = ['LEC', 'HAM']

for i in drivers:
    driver, team, driver_lap = get_fastest(i, session)
    print(f"Driver: {driver} for {team}")
    total_seconds = driver_lap.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds - 60 * minutes
    lap_str = f"{minutes}:{seconds:06.3f}"
    print(f"Time: {lap_str}")

