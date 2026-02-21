
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


# function to retrieve the telemetry data from a lap
def get_telemetry(lap_info):
    telemetry = lap_info.get_telemetry()
    return telemetry