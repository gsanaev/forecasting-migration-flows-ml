"""
Merge World Bank (WDI) data, UNDP HDR data, and WDI metadata.
Output: data/processed/wdi_hdr.csv
"""

import os
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")


def _ensure_directories():
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def merge_datasets(
    wdi_file="wdi_data.csv",
    undp_file="hdr-data.xlsx",
    meta_file="wdi_metadata.csv",
    output_file="wdi_hdr.csv",
    replace=True,
) -> str:
    """
    Merge World Bank (WDI), UNDP (HDR), and WDI metadata into one tidy dataset.
    Merge keys:
      • WDI ↔ HDR  : on Country Code and year
      • WDI ↔ META : on Country Code
    """

    _ensure_directories()

    wdi_path = os.path.join(RAW_DIR, wdi_file)
    undp_path = os.path.join(RAW_DIR, undp_file)
    meta_path = os.path.join(RAW_DIR, meta_file)
    output_path = os.path.join(PROCESSED_DIR, output_file)

    if os.path.exists(output_path) and not replace:
        print(f"✅ File already exists, skipping merge: {output_path}")
        return output_path

    # --- Load datasets ---
    wdi = pd.read_csv(wdi_path)
    undp = pd.read_excel(undp_path)
    meta = pd.read_csv(meta_path)

    print(f"WDI: {wdi.shape}, HDR: {undp.shape}, META: {meta.shape}")

    # --- Clean column names ---
    for df in [wdi, undp, meta]:
        df.columns = df.columns.str.strip()

    # --- Prepare UNDP (HDI only) ---
    undp_hdi = undp[undp["indicatorCode"] == "hdi"].copy()
    undp_hdi = (
        undp_hdi[["countryIsoCode", "year", "value"]]
        .rename(columns={"value": "hdi"})
        .dropna(subset=["countryIsoCode"])
    )

    # --- Merge WDI + HDR ---
    merged = pd.merge(
        wdi,
        undp_hdi,
        how="left",
        left_on=["Country Code", "year"],
        right_on=["countryIsoCode", "year"],
    ).drop(columns=["countryIsoCode"], errors="ignore")

    # --- Merge metadata (Region, IncomeGroup) ---
    meta_cols = [c for c in ["Country Code", "Region", "IncomeGroup"] if c in meta.columns]
    meta = meta[meta_cols].drop_duplicates(subset="Country Code")

    merged = pd.merge(
        merged,
        meta,
        on="Country Code",
        how="left",
    )

    # --- Save final merged dataset ---
    merged.to_csv(output_path, index=False)
    print(f"✅ Merged dataset saved → {output_path}")
    print(f"Final shape: {merged.shape}")
    print(merged.head())

    return output_path


if __name__ == "__main__":
    merge_datasets()
