import wbgapi as wb
import os

# ------------------------------
# Parameters
# ------------------------------
# Thematic / logical order
indicators = [
    # Demographics / Population
    "SP.POP.TOTL",       # Population
    "EN.POP.DNST",       # Population density
    "SP.DYN.TFRT.IN",    # Fertility rate
    "SP.ADO.TFRT",       # Adolescent fertility
    "SP.DYN.LE00.IN",    # Life expectancy
    "SH.DYN.MORT",       # Under-5 mortality
    "SP.URB.GROW",       # Urban population growth
    "SM.POP.NETM",       # Net migration

    # Technology
    "IT.CEL.SETS.P2",    # Mobile subscriptions

    # Economics / GDP
    "NY.GDP.PCAP.KD",    # GDP per capita
    "NY.GDP.MKTP.KD.ZG", # GDP growth
    "NE.EXP.GNFS.ZS",    # Exports % GDP
    "NE.IMP.GNFS.ZS",    # Imports % GDP
        
    # Other / Government 
    "SL.UEM.TOTL.ZS"     # Unemployment % of labor force
]

# Corresponding column names
col_names = {
    "SP.POP.TOTL": "population",
    "EN.POP.DNST": "pop_density",
    "SP.DYN.TFRT.IN": "fertility_rate",
    "SP.ADO.TFRT": "adol_fertility",
    "SP.DYN.LE00.IN": "life_expectancy",
    "SH.DYN.MORT": "under5_mortality",
    "SP.URB.GROW": "urban_pop_growth",
    "SM.POP.NETM": "net_migration",
    "IT.CEL.SETS.P2": "mobile_subs",
    "NY.GDP.PCAP.KD": "gdp_per_capita",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "NE.EXP.GNFS.ZS": "exports_gdp",
    "NE.IMP.GNFS.ZS": "imports_gdp",
    "SL.UEM.TOTL.ZS": "unemployment"
}

# ------------------------------
# File paths
# ------------------------------
data_dir = os.path.join(os.getcwd(), "data", "raw")
os.makedirs(data_dir, exist_ok=True)
output_file = os.path.join(data_dir, "wdi_data.csv")

# ------------------------------
# Download all indicators at once
# ------------------------------
print("Downloading WDI data...")
df = wb.data.DataFrame(
    series=indicators,
    economy="all",
    time=range(1990, 2025),
    labels=True,
    skipBlanks=True
)

# ------------------------------
# Prepare dataframe
# ------------------------------
df.reset_index(inplace=True)
df.rename(columns={'economy':'Country','time':'Year'}, inplace=True)
df.rename(columns=col_names, inplace=True)

# ------------------------------
# Save CSV
# ------------------------------
df.to_csv(output_file, index=False)
print(f"Data successfully saved to {output_file}")
