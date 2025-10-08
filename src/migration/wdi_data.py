import os
import requests
import zipfile
import pandas as pd

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


def extract_indicators(zip_path, indicators=INDICATORS, out="wdi_data.csv",
                       year_min=1990, year_max=2024, delete_zip=True):
    with zipfile.ZipFile(zip_path) as z:
        csvs = [f for f in z.namelist()
                if f.lower().endswith(".csv")
                and not any(x in f.lower() for x in ("series", "country", "footnote"))]
        data_file = next((f for f in csvs if "wdi" in f.lower()), csvs[0])
        print(f"📂  Found data file: {data_file}")
        with z.open(data_file) as f:
            df = pd.read_csv(f, low_memory=False)

    df = df[df["Indicator Code"].isin(indicators)]
    df = df.melt(id_vars=["Country Name", "Country Code", "Indicator Code"],
                 var_name="year", value_name="value")
    df = df[df["year"].str.isnumeric()]
    df["year"] = df["year"].astype(int)
    df = df[(df["year"] >= year_min) & (df["year"] <= year_max)]

    tidy = (df.pivot(index=["Country Name", "Country Code", "year"],
                     columns="Indicator Code", values="value")
              .reset_index()
              .rename(columns=indicators))

    out_path = os.path.join(RAW_DIR, out)
    tidy.to_csv(out_path, index=False)
    print(f"✅  Saved → {out_path} ({len(tidy)} rows)\n", tidy.head())

    if delete_zip:
        os.remove(zip_path)
        print(f"🗑️  Deleted ZIP: {zip_path}")


def main():
    zip_path = download_wdi_bulk()
    extract_indicators(zip_path)


if __name__ == "__main__":
    main()
