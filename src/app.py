import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
import streamlit as st

from search import semantic_search
from data_loader import df
from data.surah_names import SURAH_NAMES


# ============================================================
# 1. Page Configuration
# ============================================================

st.set_page_config(
    page_title="Quran Semantic Search",
    page_icon="🔎",
    layout="wide"
)


# ============================================================
# 2. Title
# ============================================================

st.title(
    "Quran Semantic Search Engine"
)

st.write(
    "Search the Quran using semantic meaning "
    "instead of exact keyword matching."
)


# ============================================================
# 3. Example Queries
# ============================================================

example_queries = [

    "من هو الله؟",

    "الصبر على المصائب والشدائد",

    "احكام الطلاق والعدة",

    "إعطاء المال للفقراء ومساعدة المحتاجين",

    "كيف يجب أن يعامل الإنسان والديه؟",

    "كيف يتوب الإنسان إلى الله بعد ارتكاب الذنب؟",

    "مغفرة الله للذنوب",

    "أهمية الصلاة والمحافظة عليها",

    "الزواج في الإسلام وحقوق الزوجين",

    "من هو النبي محمد  رسول الله  صلى الله عليه وسلم؟",
]


# ============================================================
# 4. Search Section
# ============================================================

st.subheader("Search")


query = st.text_input(
    "Enter your question:",
    placeholder=(
        "مثال: كيف يجب أن يعامل الإنسان والديه؟"
    )
)


# ============================================================
# 5. Example Query Selector
# ============================================================

selected_example = st.selectbox(
    "Or choose an example query:",
    [
        "-- Select an example --"
    ] + example_queries
)


# ============================================================
# 6. Use Selected Example
# ============================================================

if selected_example != "-- Select an example --":

    query = selected_example


# ============================================================
# 7. Sidebar
# ============================================================

st.sidebar.header(
    "Search Filters"
)


# ============================================================
# 8. Surah Metadata Filter
# ============================================================

surah_options = {
    "كل السور": None
}


for surah_number in sorted(
    df["surah"].unique()
):

    surah_number = int(
        surah_number
    )

    surah_name = SURAH_NAMES.get(
        surah_number,
        f"سورة {surah_number}"
    )

    surah_options[
        surah_name
    ] = surah_number


selected_surah_name = st.sidebar.selectbox(
    "اختر السورة:",
    list(surah_options.keys())
)


selected_surah = surah_options[
    selected_surah_name
]


# ============================================================
# 9. Number of Results
# ============================================================

top_k = st.sidebar.slider(
    "Number of results:",
    min_value=1,
    max_value=10,
    value=5
)


# ============================================================
# 10. Search Button
# ============================================================

search_button = st.button(
    "Search",
    type="primary"
)


# ============================================================
# 11. Perform Search
# ============================================================

if search_button:

    # --------------------------------------------------------
    # Validate Query
    # --------------------------------------------------------

    if not query.strip():

        st.warning(
            "Please enter a query or select "
            "an example query."
        )


    else:

        # ----------------------------------------------------
        # Semantic Search
        #
        # If selected_surah is None:
        #     Search the entire Quran.
        #
        # Otherwise:
        #     Search inside the selected Surah index.
        # ----------------------------------------------------

        with st.spinner(
            "Searching the Quran..."
        ):

            results = semantic_search(
                query=query,
                top_k=top_k,
                surah=selected_surah
            )


        # ----------------------------------------------------
        # Display Search Results
        # ----------------------------------------------------

        st.subheader(
            "Search Results"
        )


        if len(results) == 0:

            st.info(
                "No results found."
            )


        else:

            for rank, (_, row) in enumerate(
                results.iterrows(),
                start=1
            ):

                # --------------------------------------------
                # Get Surah Number
                # --------------------------------------------

                surah_number = int(
                    row["surah"]
                )


                # --------------------------------------------
                # Get Surah Name
                # --------------------------------------------

                surah_name = SURAH_NAMES.get(
                    surah_number,
                    f"سورة {surah_number}"
                )


                # --------------------------------------------
                # Display Result Header
                # --------------------------------------------

                st.markdown(
                    f"### #{rank} — "
                    f"{surah_name} | "
                    f"آية {row['ayah']}"
                )


                # --------------------------------------------
                # Display Similarity Score
                # --------------------------------------------

                st.write(
                    f"**Similarity Score:** "
                    f"{row['score']:.4f}"
                )


                # --------------------------------------------
                # Display Ayah
                # --------------------------------------------

                st.write(
                    row["text"]
                )


                st.divider()