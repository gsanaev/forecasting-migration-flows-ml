import os
import pandas as pd

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")


def _ensure_directories():
    os.makedirs(PROCESSED_DIR, exist_ok=True)


def merge_datasets(
    wdi_file="wdi_data.csv",
    undp_file="hdr-data.xlsx",
    output_file="wdi_hdr.csv",
    replace=True
) -> str:
    """
    Merge World Bank (WDI) and UNDP (HDR) datasets into a single tidy CSV.
    Keeps all WDI columns and adds only the HDI column from UNDP.
    """
    _ensure_directories()

    wdi_path = os.path.join(RAW_DIR, wdi_file)
    undp_path = os.path.join(RAW_DIR, undp_file)
    output_path = os.path.join(PROCESSED_DIR, output_file)

    if os.path.exists(output_path) and not replace:
        print(f"File already exists, skipping merge: {output_path}")
        return output_path

    # Load datasets
    wdi = pd.read_csv(wdi_path)
    undp = pd.read_excel(undp_path)

    # Clean column names
    wdi.columns = wdi.columns.str.strip()
    undp.columns = undp.columns.str.strip()

    # Keep only HDI indicator
    undp_hdi = undp[undp["indicatorCode"] == "hdi"].copy()
    undp_hdi = undp_hdi[["countryIsoCode", "year", "value"]].rename(columns={"value": "hdi"})

    # Merge on ISO code and year
    merged = pd.merge(
        wdi,
        undp_hdi,
        how="left",
        left_on=["Country Code", "year"],
        right_on=["countryIsoCode", "year"]
    )

    # Drop duplicate ISO column
    merged = merged.drop(columns=["countryIsoCode"])

    # Save merged dataset
    merged.to_csv(output_path, index=False)
    print(f"Merged dataset saved to {output_path} ({len(merged)} rows)")
    print(merged.head())

    return output_path


if __name__ == "__main__":
    merge_datasets()
