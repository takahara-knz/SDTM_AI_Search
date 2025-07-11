import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ 類似度スコアで並べ替える関数
def filter_by_similarity(df, keyword, top_n=None):
    texts = (
        df["xxTESTCD"].fillna("") + " " +
        df["xxTEST"].fillna("") + " " +
        df["xxTEST-J"].fillna("")
    )
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts.tolist() + [keyword])
    similarity = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1]).flatten()
    df = df.copy()
    df["類似度スコア"] = similarity
    if top_n:
        return df.sort_values("類似度スコア", ascending=False).head(top_n)
    else:
        return df.sort_values("類似度スコア", ascending=False)

# ✅ アプリ本体
def run():
    st.title("おしえてねこちゃん：CDISC Terminology 検索ツール（xxTEST系）")

    # 🔹 データ読み込み（エラー表示付き）
    try:
        df = pd.read_excel("data/00.TerminologyMerge.xlsx")
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {e}")
        return

    # ✅ セッションステートでソート状態を記憶
    if "sort_by_similarity" not in st.session_state:
        st.session_state.sort_by_similarity = False

    # 🔎 検索語の入力
    search_word = st.text_input("🔍 検索ワードを入力してください（例：ヘモグロビン、QT間隔、ALT など）")

    if search_word:
        # 🔍 部分一致検索
        mask = df.apply(lambda row: row.astype(str).str.contains(search_word, case=False, na=False).any(), axis=1)
        results = df[mask].reset_index(drop=True)
        st.write(f"🔎 検索結果：{len(results)} 件ヒットしました")

        # ✅ 横並びでボタン＋状態表示
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("🔘 類似度の高い順にソート"):
                st.session_state.sort_by_similarity = True

        with col2:
            if st.session_state.sort_by_similarity:
                st.markdown("✅ 現在は類似度の高い順で並べています")
            else:
                st.markdown("📝 現在はABC順です。このボタンを押すと類似度順に並び替えできます")

        # ✅ ソートの実行
        if st.session_state.sort_by_similarity:
            results = filter_by_similarity(results, search_word)

        # 🔹 表示列の指定（存在する列のみ表示）
        preferred_columns = [
            "Domain", "Code", "xxTESTCD", "xxTEST",
            "xxTEST-J", "CDISC Synonym(s)-J", "CDISC Definition-J", "NCI Preferred Term-J",
            "CDISC Synonym(s)", "CDISC Definition", "NCI Preferred Term"
        ]
        display_columns = [col for col in preferred_columns if col in results.columns]
        st.dataframe(results[display_columns], use_container_width=True)

    else:
        st.info("🔍 上のテキストボックスに検索語を入力してください。例：ヘモグロビン、QT間隔、ALT など")

# ✅ 実行
if __name__ == "__main__":
    run()
