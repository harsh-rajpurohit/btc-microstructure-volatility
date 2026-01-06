import pandas as pd
import numpy as np

# Load microstructure features
df = pd.read_csv("microstructure_features.csv")

# Sort by time (always do this)
df = df.sort_values("timestamp_ms").reset_index(drop=True)

print(df.head())



# Log returns from midprice
df["log_midprice"] = np.log(df["midprice"])
df["return"] = df["log_midprice"].diff()

print(df[["midprice", "return"]].head())



#What this does: takes rolling chunks of returns, squares them, sums them, assigns RV to the end of each window
WINDOW = 150  # 5 minutes at 2-second frequency

df["rv_5min"] = (
    df["return"]
    .rolling(WINDOW)
    .apply(lambda x: np.sum(x**2), raw=True)
)

print(df[["return", "rv_5min"]].tail())



final_df = df[[
    "timestamp_ms",
    "midprice",
    "return",
    "rv_5min",
    "spread",
    "depth_imbalance",
    "OFI"
]]

final_df.to_csv("microstructure_with_rv.csv", index=False)

print("Day 6 DONE.")
print(final_df.tail())