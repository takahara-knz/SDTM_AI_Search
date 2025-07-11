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

    # 🔹 データ読み込み
    try:
        df = pd.read_excel("data/00.TerminologyMerge.xlsx")
        df.columns = df.columns.str.strip()
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {e}")
        return

    # 🔍 検索語入力
    search_word = st.text_input("🔍 検索ワードを入力してください（例：ヘモグロビン、QT間隔、ALT など）")

    if search_word:
        # 🔍 部分一致検索
        mask = df.apply(lambda row: row.astype(str).str.contains(search_word, case=False, na=False).any(), axis=1)
        results = df[mask].reset_index(drop=True)
        st.write(f"🔎 検索結果：{len(results)} 件ヒットしました")

        # ✅ ソートボタン＋説明文を横並び表示
        col1, col2 = st.columns([1, 5])
        with col1:
            sort_trigger = st.button("🔘 類似度の高い順にソート")
        with col2:
            if sort_trigger:
                st.markdown("✅ 類似度順で表示しています")
            elif search_word:
                st.markdown("📝 現在はABC順です。このボタンを押すと類似度順に並べ替えできます")

        # ✅ 類似度ソート実行
        if sort_trigger:
            results = filter_by_similarity(results, search_word)

        # 🔹 表示列の順番調整
        preferred_columns = [
            "Domain", "Code", "xxTESTCD", "xxTEST",
            "xxTEST-J", "CDISC Synonym(s)-J", "CDISC Definition-J", "NCI Preferred Term-J",
            "CDISC Synonym(s)", "CDISC Definition", "NCI Preferred Term"
        ]
        display_columns = [col for col in preferred_columns if col in results.columns]
        st.dataframe(results[display_columns], use_container_width=True)

    else:
        st.info("🔍 上のテキストボックスに検索語を入力してください。例：ヘモグロビン、QT間隔、ALT など")

# ✅ アプリ実行
if __name__ == "__main__":
    run()
