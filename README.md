## Research Paper

📄 **Final Paper:**  
[Predicting Short-Horizon Volatility Using Bitcoin Market Microstructure](btc_microstructure_volatility.pdf)



# BTC Microstructure → Short-Horizon Volatility (Toy Study)

This project explores whether simple Bitcoin market microstructure signals (order flow imbalance, bid–ask spread, and depth imbalance) have predictive power for **very short-horizon realized volatility**. The goal is educational: build a clean end-to-end pipeline from raw exchange data → features → plots → regressions → robustness checks.

## Data
- **Venue:** Kraken (BTC)
- **Inputs:**
  - Order book snapshots (top-of-book / top levels)
  - Trade prints
- **Notes:** This is a short intraday sample and should be treated as a limited dataset (not a production-grade study).

## Features / Variables
- **Midprice:** average of best bid and best ask
- **Return:** log return of midprice
- **Realized Volatility (RV):** sum of squared returns over fixed windows (5m / 15m / 30m)
- **Bid–ask spread:** best ask − best bid
- **Order Flow Imbalance (OFI):** signed measure of changes in bid/ask queue sizes
- **Depth imbalance:** normalized difference between bid-side and ask-side depth (across top levels)

## Methodology
1. **Feature engineering** from synchronized trades + order book data
2. **Exploratory plots**:
   - OFI vs next-step returns
   - Spread vs RV
   - |Depth imbalance| vs RV
3. **Regression (OLS)**:
   - Baseline: future RV on contemporaneous microstructure variables (OFI, spread)
4. **Robustness checks**:
   - Different RV horizons (5m / 15m / 30m)
   - Lagged OFI terms
   - High-volatility vs low-volatility subsamples

## Key Results (high level)
- Relationships are **weak and noisy** in this small sample.
- OFI shows **unstable / statistically weak** links with future RV across specifications.
- Spread sometimes appears statistically significant, but effect sizes are **economically small**.
- Robustness tests suggest many patterns **do not persist** consistently across horizons and subsamples.

## Limitations
- Small sample / single-venue data
- Microstructure noise and measurement error
- Latency and execution considerations ignored (not a trading strategy)
- OLS is a simple baseline; more realistic models may be needed for forecasting

## How to run
From the project directory:

```bash
python3 day4b_collect_synced.py
python3 day5_features.py
python3 day6_returns_volatility.py
python3 day7_analysis.py
python3 day8_regression.py
python3 day9_robustness.py
