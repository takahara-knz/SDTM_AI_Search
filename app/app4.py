import streamlit as st
import pandas as pd
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from janome.tokenizer import Tokenizer

def run_app():

    # ページ設定
    st.set_page_config(page_title="おしえてねこちゃん", layout="wide")

    tokenizer = Tokenizer()

    def tokenize(text):
        return " ".join(tokenizer.tokenize(str(text), wakati=True))

    def get_combined_texts(df):
        return (
            df["CDISC Submission Value-J"].fillna("") + " " +
            df["NCI Preferred Term-J"].fillna("") + " " +
            df["CDISC Synonym(s)-J"].fillna("") + " " +
            df["CDISC Submission Value"].fillna("")
        )

    @st.cache_data
    def load_excel_data():
        # dataのパスを取得
        current_dir = os.path.dirname(__file__)
        excel_path = os.path.join(current_dir, "..", "data", "02.Terminology_V3.3_和訳付き.xlsx")

        # Excelファイルからシートごとに読み込む
        index = pd.read_excel(excel_path, sheet_name="ペア以外")
        data = pd.read_excel(excel_path, sheet_name="ペアのないTerminology和訳付き")
        return index, data

    def clear_search():
        st.session_state.search_word = ""
        st.session_state.search_mode = None

    def run_terminology_app():
        st.title("🐱さがしてねこちゃん SDTMIG V3.3 Terminology検索")

        try:
            sheet_index, sheet_data = load_excel_data()
        except Exception as e:
            st.error(f"❌ データ読み込みエラー: {e}")
            return

        # 状態初期化
        if "search_mode" not in st.session_state:
            st.session_state.search_mode = None

        if "search_word" not in st.session_state:
            st.session_state.search_word = ""

        # Terminology選択
        term_list = sheet_index["Term"].dropna().unique().tolist()

        selected_term = st.selectbox(
            "📂 Terminologyを選んでください",
            term_list,
            key="term_selector",
            on_change=clear_search
        )

        # 検索語とボタン
        st.session_state.search_word = st.text_input("🔍 検索語を入力してください", value=st.session_state.search_word)

        col1, col2, col3 = st.columns(3)
        if col1.button("🧠 おすすめ検索（AIソート）"):
            st.session_state.search_mode = "ai"
        if col2.button("🎯 ピンポイント検索（完全一致）"):
            st.session_state.search_mode = "exact"
        if col3.button("🔍 ゆるっと検索（部分一致）"):
            st.session_state.search_mode = "partial"

        # データ抽出
        df_filtered = sheet_data[sheet_data["Term"] == selected_term].copy()

        # 検索モード別処理
        keyword = st.session_state.search_word.strip()

        if keyword and st.session_state.search_mode == "ai":
            texts = get_combined_texts(df_filtered).tolist()
            tokenized_texts = [tokenize(t) for t in texts]
            tokenized_keyword = tokenize(keyword)

            vectorizer = TfidfVectorizer(max_features=1000)
            tfidf_matrix = vectorizer.fit_transform(tokenized_texts + [tokenized_keyword])
            similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()

            df_filtered["類似度スコア"] = similarity
            df_filtered = df_filtered.sort_values("類似度スコア", ascending=False)

            st.write(f"🔍 類似度順に {len(df_filtered)} 件の結果")

        elif keyword and st.session_state.search_mode == "exact":
            mask = df_filtered.apply(lambda row: any(str(keyword).lower() == str(v).lower() for v in row.values), axis=1)
            df_filtered = df_filtered[mask]
            st.write(f"🎯 完全一致で {len(df_filtered)} 件ヒット")

        elif keyword and st.session_state.search_mode == "partial":
            mask = df_filtered.apply(lambda row: any(keyword.lower() in str(v).lower() for v in row.values), axis=1)
            df_filtered = df_filtered[mask]
            st.write(f"🧩 部分一致で {len(df_filtered)} 件ヒット")

        elif not keyword:
            st.info("🔎 検索語が未入力なので、選択したTerminologyの候補一覧を表示します")

        # 表示列
        display_columns = [
            "Code", "CDISC Submission Value", "CDISC Submission Value-J",
            "CDISC Synonym(s)-J", "CDISC Definition-J", "NCI Preferred Term-J",
            "CDISC Synonym(s)", "CDISC Definition", "NCI Preferred Term", "類似度スコア"
        ]
        display_cols = [c for c in display_columns if c in df_filtered.columns]

        st.dataframe(df_filtered[display_cols], use_container_width=True)

        if st.button("← メニューに戻る"):
            st.session_state["selected_app"] = "menu"
    run_terminology_app()

if __name__ == "__main__":
    run_app()