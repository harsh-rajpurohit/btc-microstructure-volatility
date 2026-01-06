
#PART A — Order Book Features (Liquidity Side)

import pandas as pd

# Load order book snapshots
ob = pd.read_csv("orderbook_top5_synced.csv")

# Sort by time (important)
ob = ob.sort_values("timestamp_ms").reset_index(drop=True)

print(ob.head())

# Midprice
ob["midprice"] = (ob["best_bid_price"] + ob["best_ask_price"]) / 2

# Bid–ask spread
ob["spread"] = ob["best_ask_price"] - ob["best_bid_price"]



#Depth & Depth Imbalance
bid_depth_cols = [f"bid{i}_size" for i in range(1, 6)]
ask_depth_cols = [f"ask{i}_size" for i in range(1, 6)]

ob["bid_depth"] = ob[bid_depth_cols].sum(axis=1)
ob["ask_depth"] = ob[ask_depth_cols].sum(axis=1)


ob["depth_imbalance"] = (
    ob["bid_depth"] - ob["ask_depth"]
) / (ob["bid_depth"] + ob["ask_depth"])




#PART B — Order Flow Imbalance (Pressure Side)

# Load trades
trades = pd.read_csv("trades_synced.csv")

trades = trades.sort_values("timestamp_ms").reset_index(drop=True)
print(trades.head())


# Use 2-second bins (2000 ms)
BIN_MS = 2000
trades["time_bin"] = (trades["timestamp_ms"] // BIN_MS) * BIN_MS



trades["signed_volume"] = trades.apply(
    lambda x: x["amount"] if x["side"] == "buy" else -x["amount"],
    axis=1
)


#Aggregate → OFI
ofi = (
    trades
    .groupby("time_bin")["signed_volume"]
    .sum()
    .reset_index()
    .rename(columns={"signed_volume": "OFI"})
)


#PART C — Merge Everything

# Create matching bins for order book
ob["time_bin"] = (ob["timestamp_ms"] // BIN_MS) * BIN_MS

# Merge
df = pd.merge(
    ob,
    ofi,
    on="time_bin",
    how="left"
)

df["OFI"] = df["OFI"].fillna(0)


#Final Dataset
final_df = df[[
    "timestamp_ms",
    "midprice",
    "spread",
    "depth_imbalance",
    "OFI"
]]

final_df.to_csv("microstructure_features.csv", index=False)

print("Day 5 DONE.")
print(final_df.head())