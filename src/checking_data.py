import pandas as pd

df = pd.read_csv('../outputs/tables/dataset.csv')

rows, cols = df.shape

print(rows, cols)

# column_list = df.columns.tolist()
# print(column_list)

# print(df.head()['target_delta_s'])
# print(df.dtypes)

counts = df['baseline_correct'].value_counts()
true_count = counts.get(True, 0)
false_count = counts.get(False, 0)
print(true_count)
print(false_count)

feature_cols = [
    "mean_speed_diff",
    "top_speed_diff",
    "min_speed_diff",
    "std_speed_diff",
    "full_throttle_diff",
    "avg_throttle_diff",
    "brake_event_diff",
]

target_col = "target_delta_s"

meta_cols = [
    "year",
    "event_name",
    "session_name",
    "driverA_code",
    "driverB_code",
    "driverA_name",
    "driverB_name",
    "lap_time_A_s",
    "lap_time_B_s",
    "approx_delta_s",
    "baseline_score",
    "predicted_winner",
    "actual_winner",
    "baseline_correct",
]

# not really ncecessary because their are not NaNs
model_df = df[feature_cols + [target_col]].dropna()


X = model_df[feature_cols]
y = model_df[target_col]