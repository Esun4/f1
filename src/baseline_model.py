def compute_score(features):
    total = 0
    
    weights = {
        "mean_speed_diff": 1.0,
        "top_speed_diff": 0.35,
        "min_speed_diff": 0.8,
        "std_speed_diff": -0.2,
        "full_throttle_diff": 0.45,
        "avg_throttle_diff": 0.25,
        "brake_event_diff": -0.5,
    }
    
    for i in weights:
        total += features[i] * weights[i]

    return total

def predict_winner(predicted):
    if predicted > 0:
        return "B"
    elif predicted == 0:
        return "Same"
    else:
        return "A"
    
def actual_winner(delta):
    if delta < 0:
        return "A"
    elif delta == 0:
        return "Same"
    else:
        return "B"