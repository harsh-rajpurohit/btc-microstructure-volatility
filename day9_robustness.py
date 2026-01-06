#In our Day 6 file, we computed: rv_5min
#Now create rv_15min and rv_30min.


#Test 1: Different time windows
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("microstructure_with_rv.csv")
df = df.dropna().reset_index(drop=True)

# log returns already exist
df["rv_15min"] = df["return"].rolling(15).apply(lambda x: (x**2).sum())
df["rv_30min"] = df["return"].rolling(30).apply(lambda x: (x**2).sum())

df = df.dropna().reset_index(drop=True)



#Run regressions for each window
def run_reg(y, df):
    X = df[["OFI", "spread"]]
    X = sm.add_constant(X)
    model = sm.OLS(df[y], X).fit()
    print(f"\nRegression for {y}")
    print(model.summary())

run_reg("rv_5min", df)
run_reg("rv_15min", df)
run_reg("rv_30min", df)


#Test 2: Lagged OFI
df["OFI_lag1"] = df["OFI"].shift(1)
df["OFI_lag5"] = df["OFI"].shift(5)

df = df.dropna().reset_index(drop=True)

X = df[["OFI", "OFI_lag1", "OFI_lag5", "spread"]]
X = sm.add_constant(X)

model = sm.OLS(df["rv_5min"], X).fit()
print(model.summary())




#Test 3: Subsample — high vs low volatility regimes
median_rv = df["rv_5min"].median()

high_vol = df[df["rv_5min"] > median_rv]
low_vol  = df[df["rv_5min"] <= median_rv]


#Run same regression on both
def run_subsample(name, subdf):
    X = subdf[["OFI", "spread"]]
    X = sm.add_constant(X)
    model = sm.OLS(subdf["rv_5min"], X).fit()
    print(f"\n{name} sample")
    print(model.summary())

run_subsample("HIGH volatility", high_vol)
run_subsample("LOW volatility", low_vol)




