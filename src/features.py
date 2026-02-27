def compute_lap(aligned_df):
    max_speed = aligned_df['Speed'].max()
    min_speed = aligned_df['Speed'].min()
    mean_speed = aligned_df['Speed'].mean()
    std_speed = aligned_df['Speed'].std()

    rows = aligned_df.shape[0]
    # number of points where the throttle is > 95
    throttle_count = (aligned_df['Throttle'] > 95).sum()
    pct_full_throttle = int(throttle_count/rows * 100)

    brake_count = (aligned_df['Brake'] > 0.05).sum()
    pct_brake = int(brake_count/rows * 100)

    avg_throttle = aligned_df['Throttle'].mean()

    # count the number of braking zones
    braking = (aligned_df["Brake"] > 0.05)
    brake_event_count = ((~braking.shift(1, fill_value=False)) & braking).sum()
    
    return {
        "max_speed": max_speed,
        "min_speed": min_speed,
        "mean_speed": mean_speed,
        "std_speed": std_speed,
        "pct_full_throttle": pct_full_throttle,
        "pct_brake": pct_brake,
        "avg_throttle": avg_throttle,
        "brake_event_count": int(brake_event_count),
    }

def compute_pair_features(featuresA, featuresB):
    mean_speed_diff = abs(featuresA['mean_speed'] - featuresB['mean_speed'])
    top_speed_diff = abs(featuresA['max_speed'] - featuresB['max_speed'])
    min_speed_diff = abs(featuresA['min_speed'] - featuresB['min_speed'])
    std_speed_diff = abs(featuresA['std_speed'] - featuresB['std_speed'])

    full_throttle_diff = abs(featuresA['pct_full_throttle'] - featuresB['pct_full_throttle'])
    avg_throttle_diff = abs(featuresA['avg_throttle'] - featuresB['avg_throttle'])
    brake_event_diff = abs(featuresA['brake_event_count'] - featuresB['brake_event_count'])

    return {
        "mean_speed_diff": mean_speed_diff,
        "top_speed_diff": top_speed_diff,
        "min_speed_diff": min_speed_diff,
        "std_speed_diff": std_speed_diff,
        "full_throttle_diff": full_throttle_diff,
        "avg_throttle_diff": avg_throttle_diff,
        "brake_event_diff": brake_event_diff,
    }