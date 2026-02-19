import fastf1

session = fastf1.get_session(2024, 8, 'Q')

session.load()

driver1 = session.get_driver('LEC')

lec_laps = session.laps.pick_driver('LEC')
lec_fastest = lec_laps.pick_fastest()

driver2 = session.get_driver('HAM')

ham_laps = session.laps.pick_driver('HAM')
ham_fastest = ham_laps.pick_fastest()


print(session.name)
print(session.date)
print(session.event['EventName'])

# driver 1 (leclerc)
print(driver1['DriverId'])
print(lec_fastest.loc['LapTime'])

# driver 2 (hamilton)
print(driver2['DriverId'])
print(ham_fastest.loc['LapTime'])
