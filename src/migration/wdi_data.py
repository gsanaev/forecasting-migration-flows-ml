"""
Download and prepare World Bank WDI data + metadata (Region, IncomeGroup).
"""

import os
import zipfile
import requests
import pandas as pd

# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------
RAW_DIR = os.path.join("data", "raw")
URL = "http://databank.worldbank.org/data/download/WDI_CSV.zip"

INDICATORS = {
    "SP.POP.TOTL": "population",
    "EN.POP.DNST": "pop_density",
    "SP.DYN.TFRT.IN": "fertility_rate",
    "SP.ADO.TFRT": "adol_fertility",
    "SP.DYN.LE00.IN": "life_expectancy",
    "SH.DYN.MORT": "under5_mortality",
    "SP.POP.GROW": "pop_growth",
    "SP.URB.GROW": "urban_pop_growth",
    "SM.POP.NETM": "net_migration",
    "IT.CEL.SETS.P2": "mobile_subs",
    "NY.GDP.PCAP.KD": "gdp_per_capita",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "NE.EXP.GNFS.ZS": "exports_gdp",
    "NE.IMP.GNFS.ZS": "imports_gdp",
    "SL.UEM.TOTL.ZS": "unemployment",
}

# ---------------------------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------------------------
def download_wdi_bulk(url=URL, filename="WDI_CSV.zip"):
    os.makedirs(RAW_DIR, exist_ok=True)
    path = os.path.join(RAW_DIR, filename)

    if os.path.exists(path):
        print(f"File already exists → {path}")
        return path

    print("⬇️  Downloading WDI bulk dataset (this may take a few minutes)...")
    with requests.get(url, stream=True, timeout=120) as r, open(path, "wb") as f:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        for chunk in r.iter_content(1024 * 1024):
            f.write(chunk)
            if total:
                print(f"\r   Progress: {f.tell() / total * 100:5.1f}%", end="")
    print(f"\n✅  Saved ZIP → {path}")
    return path


# ---------------------------------------------------------------------
# EXTRACT DATA + METADATA
# ---------------------------------------------------------------------
def extract_wdi(zip_path, indicators=INDICATORS,
                year_min=1990, year_max=2024, delete_zip=True):

    with zipfile.ZipFile(zip_path) as z:
        csvs = [f for f in z.namelist() if f.lower().endswith(".csv")]

        # Detect main data file robustly
        preferred = [f for f in csvs if "data" in f.lower() or "wdi" in f.lower()]
        data_file = preferred[0] if preferred else csvs[0] if csvs else None
        if data_file is None:
            raise FileNotFoundError("❌ No CSV file found in the WDI ZIP archive.")
        print(f"📂 Found data file: {data_file}")

        with z.open(data_file) as f:
            df = pd.read_csv(f, low_memory=False)

        # --- Metadata extraction: prefer WDICountry.csv exactly ---
        files_lower = {f: f.lower() for f in csvs}
        country_exact = [f for f in csvs if files_lower[f].endswith("/wdicountry.csv") or files_lower[f] == "wdicountry.csv"]
        if not country_exact:
            # try any file whose basename is WDICountry.csv
            country_exact = [f for f in csvs if files_lower[f].split("/")[-1] == "wdicountry.csv"]

        metadata_df = None
        if country_exact:
            metadata_file = country_exact[0]
            with z.open(metadata_file) as f:
                meta_raw = pd.read_csv(f, low_memory=False)

            # Normalize headers
            raw_cols = {c.strip().lower(): c for c in meta_raw.columns}

            # Pick best candidates
            code_col = raw_cols.get("country code") or raw_cols.get("countrycode") or raw_cols.get("code")
            # Prefer TableName, else Short Name, else Long Name
            name_col = raw_cols.get("table name") or raw_cols.get("tablename") or raw_cols.get("short name") or raw_cols.get("shortname") or raw_cols.get("long name") or raw_cols.get("longname")
            region_col = raw_cols.get("region")
            income_col = raw_cols.get("income group") or raw_cols.get("incomegroup") or raw_cols.get("income level") or raw_cols.get("incomelevel")

            if not code_col or not name_col:
                print("⚠️ WDICountry.csv found but missing required columns; will try API fallback.")
                metadata_df = None
            else:
                out = pd.DataFrame({
                    "Country Code": meta_raw[code_col].astype(str),
                    "Country Name": meta_raw[name_col].astype(str),
                })
                if region_col:     out["Region"] = meta_raw[region_col]
                if income_col:     out["IncomeGroup"] = meta_raw[income_col]
                metadata_df = out.drop_duplicates("Country Code")

        # Fallback: World Bank API for country list (only if needed)
        if metadata_df is None:
            try:
                import requests
                url = "https://api.worldbank.org/v2/country?format=json&per_page=400"
                r = requests.get(url, timeout=60)
                r.raise_for_status()
                payload = r.json()
                rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
                meta_rows = []
                for x in rows:
                    meta_rows.append({
                        "Country Code": x.get("id"),
                        "Country Name": x.get("name"),
                        "Region": (x.get("region") or {}).get("value"),
                        "IncomeGroup": (x.get("incomeLevel") or {}).get("value"),
                    })
                metadata_df = pd.DataFrame(meta_rows).dropna(subset=["Country Code"])
                print("✅ Fallback metadata fetched from World Bank API.")
            except Exception as e:
                print(f"⚠️ Could not fetch metadata via API: {e}")
                metadata_df = None

        if metadata_df is not None and len(metadata_df):
            meta_out = os.path.join(RAW_DIR, "wdi_metadata.csv")
            metadata_df.to_csv(meta_out, index=False)
            print(f"✅ Saved metadata → {meta_out} ({len(metadata_df)} rows)")
        else:
            print("⚠️ No usable country metadata available (WDICountry/API).")

    # -----------------------------------------------------------------
    # Reshape indicator data
    # -----------------------------------------------------------------
    df = df[df["Indicator Code"].isin(indicators)]
    df = df.melt(id_vars=["Country Name", "Country Code", "Indicator Code"],
                 var_name="year", value_name="value")
    df = df[df["year"].str.isnumeric()]
    df["year"] = df["year"].astype(int)
    df = df[(df["year"] >= year_min) & (df["year"] <= year_max)]

    tidy = (
        df.pivot(index=["Country Name", "Country Code", "year"],
                 columns="Indicator Code", values="value")
        .reset_index()
        .rename(columns=indicators)
    )

    out_path = os.path.join(RAW_DIR, "wdi_data.csv")
    tidy.to_csv(out_path, index=False)
    print(f"✅ Saved main WDI data → {out_path} ({len(tidy)} rows)")

    # -----------------------------------------------------------------
    # Optional cleanup
    # -----------------------------------------------------------------
    if delete_zip and os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"🗑️  Deleted ZIP: {zip_path}")

    print("\nPreview:")
    print(tidy.head())


# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main():
    zip_path = download_wdi_bulk()
    extract_wdi(zip_path, delete_zip=True)


if __name__ == "__main__":
    main()
