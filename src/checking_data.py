import pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import math

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
# print(true_count)
# print(false_count)

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


model_df = df[feature_cols + [target_col, "year", "event_name", "session_name", "baseline_correct"]].dropna().copy()

model_df["session_id"] = (
    model_df["year"].astype(str)
    + "_"
    + model_df["event_name"].astype(str)
    + "_"
    + model_df["session_name"].astype(str)
)

X = model_df[feature_cols]
y = model_df[target_col]
groups = model_df["session_id"]

#splitting the data
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

train_idx, test_idx = next(gss.split(X, y, groups=groups))
test_rows = model_df.iloc[test_idx].copy()
baseline_acc = (test_rows["baseline_correct"] == True).mean()

X_train = X.iloc[train_idx]
X_test = X.iloc[test_idx]
y_train = y.iloc[train_idx]
y_test = y.iloc[test_idx]

train_sessions = set(groups.iloc[train_idx])
test_sessions = set(groups.iloc[test_idx])

print("Train sessions:", train_sessions)
print("Test sessions:", test_sessions)
print("Overlap:", train_sessions & test_sessions)

# create the model

# create model
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# make predictions
y_pred = model.predict(X_test)

# evaluate
mae = mean_absolute_error(y_test, y_pred)
rmse = math.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R^2:", r2)

results_df = pd.DataFrame({
    "actual_delta": y_test.values,
    "predicted_delta": y_pred
})

print(results_df.head(10))

ml_pred_winner = pd.Series(["A" if p < 0 else "B" for p in y_pred], index=test_rows.index)
ml_true_winner = pd.Series(["A" if t < 0 else "B" for t in y_test], index=test_rows.index)
ml_acc = (ml_pred_winner == ml_true_winner).mean()


print("Baseline accuracy (test):", baseline_acc)
print("ML accuracy (test):", ml_acc)
print("Improvement:", ml_acc - baseline_acc)