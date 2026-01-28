#!/usr/bin/env python3
"""
Preprocessing pipeline for Destatis population data (12411-0010)

- Parses raw Destatis CSV export
- Cleans metadata and quality flags
- Creates sliding-window regression dataset
- Performs (dummy) outlier detection
- Normalizes features
- Writes required output CSV files
"""

import csv
import pathlib
import random
from typing import List, Tuple

import numpy as np
import pandas as pd
from scipy.stats import zscore


# =========================
# Configuration
# =========================

RAW_DATA_PATH = pathlib.Path("data/raw/population_raw.csv")
OUTPUT_DIR = pathlib.Path("data/preprocessed")

WINDOW_SIZE = 3        # sliding window length
TRAIN_SPLIT = 0.8
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# =========================
# Utility functions
# =========================

def discard_outliers(
    df: pd.DataFrame,
    value_column: str = "target",
    z_threshold: float = 3.0
) -> pd.DataFrame:
    """
    Removes rows with extreme z-scores per Bundesland.

    For each Bundesland, compute the z-score of the target variable.
    Rows with |z| > z_threshold are discarded.

    NOTE:
    - Dataset is expected to be outlier-free
    - Function acts as a safeguard
    """

    def _filter_group(group: pd.DataFrame) -> pd.DataFrame:
        if len(group) < 3:
            return group

        z = zscore(group[value_column], nan_policy="omit")

        # zscore returns ndarray; align with index
        mask = (abs(z) <= z_threshold) | np.isnan(z)
        return group.loc[mask]

    filtered = (
        df
        .groupby("bundesland", group_keys=False)
        .apply(_filter_group)
        .reset_index(drop=True)
    )

    return filtered



def normalize_features(
    df: pd.DataFrame,
    feature_cols: List[str]
) -> Tuple[pd.DataFrame, dict]:
    """
    Z-score normalization.
    Returns normalized dataframe and normalization parameters.
    """
    stats = {}
    df_norm = df.copy()

    for col in feature_cols:
        mean = df[col].mean()
        std = df[col].std()

        if std == 0:
            std = 1.0

        df_norm[col] = (df[col] - mean) / std
        stats[col] = {"mean": mean, "std": std}

    return df_norm, stats


# =========================
# Parsing Destatis CSV
# =========================

def load_destatis_csv(path: pathlib.Path) -> pd.DataFrame:
    """
    Parses the Destatis semicolon CSV with interleaved quality flags.
    Returns a wide dataframe: bundesland × year columns.
    """
    rows = []

    with path.open(encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for row in reader:
            rows.append(row)

    # Find header row with years
    header_idx = next(
        i for i, r in enumerate(rows)
        if r and r[0] == "" and "31.12." in r[1]
    )

    year_row = rows[header_idx]
    years = []
    for cell in year_row:
        if cell.startswith("31.12."):
            years.append(int(cell[-4:]))

    data_rows = []
    for r in rows[header_idx + 1:]:
        if not r or r[0].startswith("_"):
            break
        if r[0].strip() == "":
            continue

        bundesland = r[0].strip()
        values = []

        # values are at positions 1,3,5,... (numbers), with "e" in between
        for i in range(1, len(r), 2):
            try:
                values.append(int(r[i]))
            except (ValueError, IndexError):
                break

        if len(values) == len(years):
            data_rows.append([bundesland] + values)

    columns = ["bundesland"] + years
    return pd.DataFrame(data_rows, columns=columns)


# =========================
# Feature engineering
# =========================

def build_sliding_window_dataset(
    df_wide: pd.DataFrame,
    window_size: int
) -> pd.DataFrame:
    """
    Converts wide bundesland×year data into supervised learning dataset.
    """
    records = []

    years = df_wide.columns[1:]

    for _, row in df_wide.iterrows():
        bundesland = row["bundesland"]
        series = row[1:].values.astype(float)

        for t in range(window_size, len(series)):
            features = series[t - window_size:t]
            target = series[t]
            year = years[t]

            record = {
                "bundesland": bundesland,
                "year": year,
                "target": target,
            }

            for i in range(window_size):
                record[f"x_t-{window_size-i}"] = features[i]

            records.append(record)

    return pd.DataFrame(records)


# =========================
# Main pipeline
# =========================

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Load raw data
    df_wide = load_destatis_csv(RAW_DATA_PATH)

    # 2) Build supervised dataset
    df = build_sliding_window_dataset(df_wide, WINDOW_SIZE)

    # 3) Outlier handling (dummy)
    df = discard_outliers(df)

    # 4) Normalization
    feature_cols = [c for c in df.columns if c.startswith("x_t-")] + ["year"]
    df["year-unnormalized"] = df["year"]
    df_norm, _ = normalize_features(df, feature_cols)
    # df = df.rename({"year": "year-normalized", "year-unnormalized": "year"})

    # 5) Stratify and split
    train_list = []
    test_list = []
    for _, group in df_norm.groupby("bundesland"):
        group_shuffled = group.sample(frac=1.0, random_state=RANDOM_SEED).reset_index(drop=True)
        split_idx = int(len(group_shuffled) * TRAIN_SPLIT)
        train_list.append(group_shuffled.iloc[:split_idx])
        test_list.append(group_shuffled.iloc[split_idx:])
    train_df = pd.concat(train_list, axis=0).reset_index(drop=True)
    test_df = pd.concat(test_list, axis=0).reset_index(drop=True)
    y_train_mean, y_train_std = train_df.target.mean(), train_df.target.std()
    train_df["target"] = (train_df["target"] - y_train_mean) / y_train_std
    test_df["target"] = (test_df["target"] - y_train_mean) / y_train_std

    # 6) Activation data (single test row)
    activation_df = test_df.sample(n=1, random_state=RANDOM_SEED)

    # 7) Save files
    df_norm.to_csv(OUTPUT_DIR / "joint_data_collection.csv", index=False)
    train_df.to_csv(OUTPUT_DIR / "training_data.csv", index=False)
    test_df.to_csv(OUTPUT_DIR / "test_data.csv", index=False)
    activation_df.to_csv(OUTPUT_DIR / "activation_data.csv", index=False)

    print("Preprocessing completed successfully.")
    print(f"Rows total: {len(df_norm)}")
    print(f"Training rows: {len(train_df)}")
    print(f"Test rows: {len(test_df)}")


if __name__ == "__main__":
    main()
