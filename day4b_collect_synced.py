import time
from datetime import datetime, timezone
import ccxt
import pandas as pd

SYMBOL = "BTC/USDT"
EXCHANGE_ID = "kraken"

SNAPSHOTS = 300          # 300 snapshots
SLEEP_SEC = 2            # every 2 seconds (~10 minutes)
ORDERBOOK_LEVELS = 5

def utc_ms_to_iso(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()

def main():
    ex = getattr(ccxt, EXCHANGE_ID)({
        "enableRateLimit": True,
        "options": {"defaultType": "spot"},
    })

    print("Using exchange:", EXCHANGE_ID)
    print("Collecting synced trades + order book...")

    all_trades_rows = []
    ob_rows = []

    # Track last trade timestamp so we only collect new trades each loop
    last_trade_ts = None

    for i in range(SNAPSHOTS):
        # 1) Order book snapshot (top 5)
        ob = ex.fetch_order_book(SYMBOL, limit=ORDERBOOK_LEVELS)
        ts_ms = ex.milliseconds()

        bids = ob.get("bids", [])[:ORDERBOOK_LEVELS]
        asks = ob.get("asks", [])[:ORDERBOOK_LEVELS]

        row = {
            "timestamp_ms": ts_ms,
            "timestamp_utc": utc_ms_to_iso(ts_ms),
        }

        if bids:
            row["best_bid_price"] = bids[0][0]
            row["best_bid_size"] = bids[0][1]
        else:
            row["best_bid_price"] = None
            row["best_bid_size"] = None

        if asks:
            row["best_ask_price"] = asks[0][0]
            row["best_ask_size"] = asks[0][1]
        else:
            row["best_ask_price"] = None
            row["best_ask_size"] = None

        for lvl in range(ORDERBOOK_LEVELS):
            if lvl < len(bids):
                row[f"bid{lvl+1}_price"] = bids[lvl][0]
                row[f"bid{lvl+1}_size"] = bids[lvl][1]
            else:
                row[f"bid{lvl+1}_price"] = None
                row[f"bid{lvl+1}_size"] = None

            if lvl < len(asks):
                row[f"ask{lvl+1}_price"] = asks[lvl][0]
                row[f"ask{lvl+1}_size"] = asks[lvl][1]
            else:
                row[f"ask{lvl+1}_price"] = None
                row[f"ask{lvl+1}_size"] = None

        ob_rows.append(row)

        # 2) Trades since last timestamp (synced)
        # Kraken supports 'since' reasonably; if it returns duplicates, we'll dedupe later.
        try:
            trades = ex.fetch_trades(SYMBOL, since=last_trade_ts, limit=200)
        except Exception:
            trades = ex.fetch_trades(SYMBOL, limit=200)

        # Update last_trade_ts to newest seen trade timestamp + 1ms
        if trades:
            max_ts = max(t["timestamp"] for t in trades if t.get("timestamp") is not None)
            last_trade_ts = (max_ts + 1) if max_ts is not None else last_trade_ts

        for t in trades:
            if t.get("timestamp") is None:
                continue
            all_trades_rows.append({
                "timestamp_ms": t["timestamp"],
                "timestamp_utc": utc_ms_to_iso(t["timestamp"]),
                "price": t["price"],
                "amount": t["amount"],
                "side": t.get("side"),
            })

        if (i + 1) % 25 == 0:
            print(f"{i+1}/{SNAPSHOTS} snapshots collected")

        time.sleep(SLEEP_SEC)

    # Save order book
    ob_df = pd.DataFrame(ob_rows).sort_values("timestamp_ms")
    ob_df.to_csv("orderbook_top5_synced.csv", index=False)

    # Save trades (dedupe by timestamp+price+amount+side)
    trades_df = pd.DataFrame(all_trades_rows)
    if len(trades_df) > 0:
        trades_df = trades_df.drop_duplicates(subset=["timestamp_ms", "price", "amount", "side"])
        trades_df = trades_df.sort_values("timestamp_ms")

    trades_df.to_csv("trades_synced.csv", index=False)

    print("Done.")
    print("Saved: orderbook_top5_synced.csv")
    print("Saved: trades_synced.csv")
    print(f"Trades rows: {len(trades_df)} | Orderbook rows: {len(ob_df)}")

if __name__ == "__main__":
    main()
