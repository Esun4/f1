import fastf1

session = fastf1.get_session(2024, 8, 'Q')

session.load()

# function to get the fastest lap of a given driver
def get_fastest(driverId):
    driver = session.get_driver(driverId)['DriverId']
    laps = session.laps.pick_drivers(driverId)

    # filtering out the inaccurate and deleted laps
    acc = laps[laps['IsAccurate'] == True]
    clean_laps = acc[acc['Deleted'] == False]

    fastest = clean_laps.pick_fastest().loc['LapTime']

    return driver, fastest

driver1 = get_fastest('LEC')[0]
driver1_lap = get_fastest('LEC')[1]


print(driver1)
print(driver1_lap)


driver2 = get_fastest('HAM')[0]
driver2_lap = get_fastest('HAM')[1]


print(driver2)
print(driver2_lap)
