import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
# ============================================================
# File paths
# ============================================================
ORIGINAL_FILE = DATA_DIR / "quran.txt"
SEARCH_FILE = DATA_DIR / "quran_no_tashkeel.txt"


# ============================================================
# Load Quran file
# ============================================================

def load_quran(file_path, text_column):

    records = []

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:

            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue

            parts = line.split("|", 2)

            # Skip malformed lines
            if len(parts) != 3:
                continue

            surah, ayah, text = parts

            records.append({
                "surah": int(surah),
                "ayah": int(ayah),
                text_column: text
            })

    return pd.DataFrame(records)


# ============================================================
# Load both versions
# ============================================================

original_df = load_quran(
    ORIGINAL_FILE,
    "text"
)

search_df = load_quran(
    SEARCH_FILE,
    "search_text"
)


# ============================================================
# Combine them
# ============================================================

df = original_df.copy()

df["search_text"] = search_df["search_text"].values


# ============================================================
# Inspect
# ============================================================

print("Number of verses:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())