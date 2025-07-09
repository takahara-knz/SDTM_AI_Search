import streamlit as st
import pandas as pd
# from st_aggrid import AgGrid, GridOptionsBuilder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ アプリ本体
def run():
    # タイトル
    st.title("CDISC Terminology 検索ツール（xxTEST 系）")

    try:
        df = pd.read_excel("data/00.TerminologyMerge.xlsx")
        st.success("✅ データ読み込み成功")
        st.write("📋 読み込んだ列名一覧:", df.columns.tolist())
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {e}")
        return
