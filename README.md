# Quran Semantic Search Engine

A semantic search engine for the Quran that retrieves relevant verses based on meaning rather than exact keyword matching.

The project uses sentence embeddings and FAISS vector search, with a Streamlit interface for interactive searching and Surah metadata filtering.

---

## Features

- Semantic search over the Quran
- Sentence-transformer embeddings
- FAISS vector similarity search
- Top-K relevant verse retrieval
- Streamlit web interface
- Example search queries
- Surah metadata filtering
- Surah-specific FAISS indexes
- Similarity scores for retrieved verses

---

## Project Structure

```text
quran-semantic-search/
│
├── data/
│   ├── quran.txt
│   ├── quran_embeddings.npy
│   ├── quran.index
│   ├── surah_indexes/
│   └── surah_names.py
│
├── src/
│   ├── app.py
│   ├── data_loader.py
│   ├── embedding.py
│   ├── search.py
│   └── build_index.py
│
├── requirements.txt
├── README.md
└── .gitignore
How It Works

The system follows a semantic retrieval pipeline:

Quran Corpus
     ↓
Data Preprocessing
     ↓
Sentence Embeddings
     ↓
FAISS Vector Index
     ↓
User Query
     ↓
Query Embedding
     ↓
Metadata Filtering
     ↓
Similarity Search
     ↓
Top-K Quran Verses
Embedding Model

The project uses:

silma-ai/silma-embedding-sts-v0.1

The model was selected because it provides semantic embeddings suitable for Arabic text similarity.

The same embedding model is used during both:

Quran embedding generation
User query embedding

Using the same model is important because Quran vectors and query vectors must exist in the same embedding space for similarity search to be meaningful.

Chunking Strategy

Unlike long documents, the Quran already has a natural semantic unit: the Ayah.

Therefore, each Ayah is treated as one searchable chunk:

1 row = 1 Ayah = 1 searchable chunk

This preserves the original Quran structure and allows every search result to retain its Surah and Ayah metadata.

No arbitrary fixed-size text chunking was applied.

Vector Search

FAISS is used to efficiently search the generated embeddings.

The embeddings are normalized and searched using inner-product similarity, which corresponds to cosine similarity for normalized vectors.

Two types of indexes are created:

One index containing the complete Quran
One index for each Surah

This allows metadata filtering to happen before retrieval.

For example:

User Query
    ↓
Select Surah: Al-Baqarah
    ↓
Search only Al-Baqarah FAISS index
    ↓
Return Top-K verses
Metadata Filtering

Users can optionally filter their search by Surah.

When "All Surahs" is selected, the system searches the complete Quran index.

When a specific Surah is selected, the system searches only the FAISS index associated with that Surah.

This means the metadata filter is applied before semantic retrieval rather than filtering the results after the search.

User Interface

The Streamlit application provides:

Free-text query input
Example queries
Number of results selection
Surah filtering
Similarity scores
Retrieved Quran verses
Surah names and Ayah numbers
Example Queries

Examples included in the application:

من هم الذين يؤمنون بالغيب ويقيمون الصلاة؟
الصبر على المصائب والشدائد
احكام النساء وحقوق وواجبات المرأة في الإسلام
إعطاء المال للفقراء ومساعدة المحتاجين
كيف يجب أن يعامل الإنسان والديه؟
كيف يتوب الإنسان إلى الله بعد ارتكاب الذنب؟
مغفرة الله للذنوب
أهمية الصلاة والمحافظة عليها
الصدق وعدم الكذب
العدل وعدم ظلم الآخرين
Technologies
Python
NumPy
Pandas
Sentence Transformers
FAISS
Scikit-learn
Streamlit
Installation

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd quran-semantic-search

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt
Running the Project
1. Generate Quran Embeddings

If the embeddings file does not already exist:

python src/embedding.py

This generates:

data/quran_embeddings.npy
2. Build the FAISS Indexes

Run:

python src/build_index.py

This creates:

data/quran.index

and the Surah-specific indexes:

data/surah_indexes/
3. Run the Streamlit Application

Run:

python -m streamlit run src/app.py

The application will open in the browser.

Search Example

A user can enter a semantic query such as:

كيف يجب أن يعامل الإنسان والديه؟

The system converts the query into an embedding and searches for Quran verses with similar semantic meaning.

The result includes:

Surah name
Ayah number
Quran verse
Similarity score
Project Goal

This project demonstrates the core concepts behind semantic search and vector retrieval:

Text embeddings
Semantic similarity
Vector indexing
FAISS search
Top-K retrieval
Metadata filtering
Interactive search applications
Future Improvements

Possible future improvements include:

Multilingual search
English-to-Arabic semantic retrieval
Improved ranking models
Reranking retrieved verses
Additional Quran metadata filters
Search result highlighting
Deployment as a public web application
Author

Built as part of an AI Engineer learning roadmap and Mini Project 5: Semantic Search Engine.


**ده هو الملف كاملًا**. انسخيه كما هو في `README.md`.

بس قبل الـ GitHub push، **ماتغيريش**:

```text
<YOUR_GITHUB_REPOSITORY_URL>