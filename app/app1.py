import streamlit as st
import pandas as pd
# from st_aggrid import AgGrid, GridOptionsBuilder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ アプリ本体
def run():
    # タイトル
    st.title("CDISC Terminology 検索ツール（xxTEST 系）")

    # データ読み込み（キャッシュ付き）
    @st.cache_data
    def load_data():
        return pd.read_excel("data/00.TerminologyMerge.xlsx")
        st.write("📋 読み込んだ列名一覧:", df.columns.tolist())
