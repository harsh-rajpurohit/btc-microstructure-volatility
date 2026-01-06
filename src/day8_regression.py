#load data
import pandas as pd
import statsmodels.api as sm

# Load dataset
df = pd.read_csv("microstructure_with_rv.csv")

# Sort by time (important)
df = df.sort_values("timestamp_ms").reset_index(drop=True)

# Drop missing values
df = df.dropna().reset_index(drop=True)



#create RV(t+1) (future volatility)
df["rv_future"] = df["rv_5min"].shift(-1)

# Drop last row (no future RV)
df = df.dropna().reset_index(drop=True)



#Define regression variables
Y = df["rv_future"]

X = df[["OFI", "spread"]]
X = sm.add_constant(X)  # adds alpha




#run regression
model = sm.OLS(Y, X).fit()

print(model.summary())




#to run the code - 
#cd ~/Desktop/btc_microstructure
#python3 day8_regression.py
