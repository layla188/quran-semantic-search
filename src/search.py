import faiss

from pathlib import Path

from sentence_transformers import SentenceTransformer

from data_loader import df


# ============================================================
# 1. Configuration
# ============================================================

MODEL_NAME = "silma-ai/silma-embedding-sts-v0.1"


# ============================================================
# 2. Project paths
# ============================================================

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
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
# 3. Load embedding model
# ============================================================

print(
    "Loading embedding model..."
)

model = SentenceTransformer(
    MODEL_NAME
)

print(
    "Model loaded successfully!"
)


# ============================================================
# 4. Load main Quran FAISS index
# ============================================================

print(
    "Loading Quran FAISS index..."
)

quran_index = faiss.read_index(
    str(INDEX_PATH)
)

print(
    "Quran index loaded!"
)

print(
    "Number of indexed verses:",
    quran_index.ntotal
)


# ============================================================
# 5. Check embedding dimension
# ============================================================

test_embedding = model.encode(
    "اختبار"
)


print(
    "Query embedding shape:",
    test_embedding.shape
)


if (
    quran_index.d
    != test_embedding.shape[0]
):

    raise ValueError(
        f"Dimension mismatch!\n"
        f"FAISS index dimension: "
        f"{quran_index.d}\n"
        f"Query embedding dimension: "
        f"{test_embedding.shape[0]}"
    )


print(
    "Dimensions match!"
)


# ============================================================
# 6. Semantic Search
# ============================================================

def semantic_search(
    query,
    top_k=5,
    surah=None
):

    # --------------------------------------------------------
    # 1. Convert query to embedding
    # --------------------------------------------------------

    query_embedding = model.encode(
        query
    )


    # --------------------------------------------------------
    # 2. Reshape
    # --------------------------------------------------------

    query_embedding = (
        query_embedding
        .reshape(1, -1)
    )


    # --------------------------------------------------------
    # 3. Convert to float32
    # --------------------------------------------------------

    query_embedding = (
        query_embedding
        .astype("float32")
    )


    # --------------------------------------------------------
    # 4. Normalize query
    # --------------------------------------------------------

    faiss.normalize_L2(
        query_embedding
    )


    # ========================================================
    # 5. Choose FAISS index
    # ========================================================

    if surah is None:

        # ----------------------------------------------------
        # Search entire Quran
        # ----------------------------------------------------

        search_index = quran_index

        search_df = df

    else:

        # ----------------------------------------------------
        # Load Surah-specific index
        # ----------------------------------------------------

        surah_index_path = (
            SURAH_INDEX_DIR
            / f"{surah}.index"
        )


        if not surah_index_path.exists():

            raise ValueError(
                f"No FAISS index found "
                f"for Surah {surah}"
            )


        search_index = faiss.read_index(
            str(surah_index_path)
        )


        # ----------------------------------------------------
        # Keep dataframe aligned with index
        # ----------------------------------------------------

        search_df = df[
            df["surah"] == surah
        ].reset_index(
            drop=True
        )


    # ========================================================
    # 6. Search
    # ========================================================

    scores, indices = (
        search_index.search(
            query_embedding,
            min(
                top_k,
                search_index.ntotal
            )
        )
    )


    # ========================================================
    # 7. Get results
    # ========================================================

    top_indices = indices[0]

    top_scores = scores[0]


    # --------------------------------------------------------
    # Remove invalid indices if any
    # --------------------------------------------------------

    valid = (
        top_indices >= 0
    )


    top_indices = (
        top_indices[valid]
    )

    top_scores = (
        top_scores[valid]
    )


    # --------------------------------------------------------
    # Get corresponding Quran verses
    # --------------------------------------------------------

    results = search_df.iloc[
        top_indices
    ].copy()


    # --------------------------------------------------------
    # Add similarity score
    # --------------------------------------------------------

    results["score"] = (
        top_scores
    )


    return results