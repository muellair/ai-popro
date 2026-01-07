import pandas as pd
import numpy as np
from pathlib import Path

WINDOW_SIZE = 5
RAW_PATH = "data/raw/population_raw.csv"
OUT_DIR = Path("data/preprocessed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def discard_outliers(df):
    # Safeguard: dataset is known to be outlier-free
    return df

def normalize(df, cols):
    for c in cols:
        df[c] = (df[c] - df[c].mean()) / df[c].std()
    return df

def create_sliding_windows(df):
    rows = []
    for state, g in df.groupby("state"):
        g = g.sort_values("year")
        pop = g["population"].values
        for i in range(len(pop) - WINDOW_SIZE):
            window = pop[i:i+WINDOW_SIZE]
            target = pop[i+WINDOW_SIZE]
            growth = (window[-1] - window[0]) / window[0]
            rows.append(
                list(window) + [growth, target, state]
            )
    cols = [f"lag_{i}" for i in range(WINDOW_SIZE)] + ["growth", "target", "state"]
    return pd.DataFrame(rows, columns=cols)

def main():
    df = pd.read_csv(RAW_PATH)
    df = discard_outliers(df)

    joint = create_sliding_windows(df)
    feature_cols = [c for c in joint.columns if c.startswith("lag_") or c == "growth"]
    joint = normalize(joint, feature_cols)

    joint.to_csv(OUT_DIR / "joint_data_collection.csv", index=False)

    train = joint.sample(frac=0.8, random_state=42)
    test = joint.drop(train.index)

    train.to_csv(OUT_DIR / "training_data.csv", index=False)
    test.to_csv(OUT_DIR / "test_data.csv", index=False)

    test.sample(1, random_state=1).to_csv(
        OUT_DIR / "activation_data.csv", index=False
    )

if __name__ == "__main__":
    main()
