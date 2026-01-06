#Load data + basic setup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("microstructure_with_rv.csv")

# Sort by time
df = df.sort_values("timestamp_ms").reset_index(drop=True)

# Drop rows with missing values (important for plots)
df = df.dropna().reset_index(drop=True)

print(df.head())



# 1-step ahead return (2 seconds into the future)
df["future_return"] = df["return"].shift(-1)

# Drop last row (no future return)
df = df.dropna().reset_index(drop=True)


#Plot OFI vs future returns
plt.figure()
plt.scatter(df["OFI"], df["future_return"], alpha=0.3)
plt.xlabel("Order Flow Imbalance (OFI)")
plt.ylabel("Future Return")
plt.title("OFI vs Future Returns")
plt.tight_layout()
plt.savefig("ofi_vs_future_returns.png", dpi=150)
plt.close()



#Plot spread vs RV
plt.figure()
plt.scatter(df["spread"], df["rv_5min"], alpha=0.3)
plt.xlabel("Bid–Ask Spread")
plt.ylabel("5-min Realized Volatility")
plt.title("Spread vs Realized Volatility")
plt.tight_layout()
plt.savefig("spread_vs_rv.png", dpi=150)
plt.close()


#Plot |depth imbalance| vs RV
plt.figure()
plt.scatter(np.abs(df["depth_imbalance"]), df["rv_5min"], alpha=0.3)
plt.xlabel("|Depth Imbalance|")
plt.ylabel("5-min Realized Volatility")
plt.title("Depth Imbalance vs Realized Volatility")
plt.tight_layout()
plt.savefig("depth_imbalance_vs_rv.png", dpi=150)
plt.close()
