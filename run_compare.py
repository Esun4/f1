import fastf1
from src.data_loader import get_fastest, get_telemetry

fastf1.Cache.enable_cache("/Users/ethan/Documents/coding/F1_telem/cache/fastf1")

session = fastf1.get_session(2024, 8, 'Q')

session.load()

print(session.name)
print(session.event['EventName'])
print(session.date)

drivers = ['LEC', 'HAM']

for i in drivers:
    driver, team, lap = get_fastest(i, session)
    print(f"Driver: {driver} for {team}")
    total_seconds = lap.loc['LapTime'].total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds - 60 * minutes
    lap_str = f"{minutes}:{seconds:06.3f}"
    print(f"Time: {lap_str}")
    print(f"Lap Number: {lap.loc['LapNumber']}")
    print(f"Tire Compound: {lap.loc['Compound']}")
    
    telem = get_telemetry(lap)

    print(telem[['Distance', 'Speed', 'Throttle', 'Brake', 'X', 'Y', 'Time']].head())
    print("\n")

