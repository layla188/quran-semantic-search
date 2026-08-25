import numpy as np
import faiss

from pathlib import Path

from data_loader import df


# ============================================================
# 1. Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDINGS_PATH = (
    BASE_DIR
    / "data"
    / "quran_embeddings.npy"
)

INDEX_PATH = (
    BASE_DIR
    / "data"
    / "quran.index"
)

SURAH_INDEX_DIR = (
    BASE_DIR
    / "data"
    / "surah_indexes"
)


# ============================================================
# 2. Load embeddings
# ============================================================

print("Loading Quran embeddings...")

embeddings = np.load(
    EMBEDDINGS_PATH
)

print(
    "Embeddings shape:",
    embeddings.shape
)


# ============================================================
# 3. Check alignment
# ============================================================

if len(df) != len(embeddings):

    raise ValueError(
        "Mismatch between dataframe rows "
        "and embeddings!"
    )


print(
    "Dataframe and embeddings are aligned."
)


# ============================================================
# 4. Convert to float32
# ============================================================

embeddings = embeddings.astype(
    "float32"
)


# ============================================================
# 5. Normalize embeddings
# ============================================================

faiss.normalize_L2(
    embeddings
)


# ============================================================
# 6. Create main Quran index
# ============================================================

dimension = embeddings.shape[1]

quran_index = faiss.IndexFlatIP(
    dimension
)


# ============================================================
# 7. Add all Quran embeddings
# ============================================================

quran_index.add(
    embeddings
)

print(
    "Total Quran vectors:",
    quran_index.ntotal
)


# ============================================================
# 8. Save main index
# ============================================================

faiss.write_index(
    quran_index,
    str(INDEX_PATH)
)

print(
    "Main Quran index saved!"
)


# ============================================================
# 9. Create Surah indexes directory
# ============================================================

SURAH_INDEX_DIR.mkdir(
    exist_ok=True
)


# ============================================================
# 10. Build one index per Surah
# ============================================================

print(
    "\nBuilding Surah-specific indexes..."
)


surahs = sorted(
    df["surah"].unique()
)


for surah in surahs:

    # --------------------------------------------------------
    # Get dataframe rows belonging to this Surah
    # --------------------------------------------------------

    mask = (
        df["surah"] == surah
    )


    # --------------------------------------------------------
    # Get corresponding embedding positions
    # --------------------------------------------------------

    surah_embeddings = embeddings[mask.values]


    # --------------------------------------------------------
    # Create FAISS index
    # --------------------------------------------------------

    surah_index = faiss.IndexFlatIP(
        dimension
    )


    # --------------------------------------------------------
    # Add Surah embeddings
    # --------------------------------------------------------

    surah_index.add(
        surah_embeddings
    )


    # --------------------------------------------------------
    # Save index
    # --------------------------------------------------------

    index_path = (
        SURAH_INDEX_DIR
        / f"{surah}.index"
    )


    faiss.write_index(
        surah_index,
        str(index_path)
    )


    print(
        f"Surah {surah}: "
        f"{surah_index.ntotal} verses"
    )


print(
    "\nAll Surah indexes built successfully!"
)