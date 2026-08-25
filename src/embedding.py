import numpy as np
from sentence_transformers import SentenceTransformer

from data_loader import df


# ============================================================
# 1. Load embedding model
# ============================================================

MODEL_NAME = "silma-ai/silma-embedding-sts-v0.1"

model = SentenceTransformer(MODEL_NAME)


# ============================================================
# 2. Get Quran search texts
# ============================================================

texts = df["search_text"].tolist()

print("Number of verses:", len(texts))


# ============================================================
# 3. Generate embeddings
# ============================================================

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True
)


# ============================================================
# 4. Inspect embeddings
# ============================================================

print("\nEmbeddings type:", type(embeddings))
print("Embeddings shape:", embeddings.shape)


# ============================================================
# 5. Save embeddings
# ============================================================

np.save(
    "../data/quran_embeddings.npy",
    embeddings
)

print("\nEmbeddings saved successfully!")