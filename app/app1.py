import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ アプリ本体
def run():
    # タイトル
    st.title("CDISC Terminology 検索ツール（xxTEST 系）")

    # データ読み込み（キャッシュなしでエラー表示あり）
    try:
        df = pd.read_excel("data/00.TerminologyMerge.xlsx")
        df.columns = df.columns.str.strip()  # 列名の前後の空白を除去
        st.success("✅ データ読み込み成功")
        st.write("📋 読み込んだ列名一覧:", df.columns.tolist())
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {e}")
        return

    # 類似度スコアで並べ替える関数
    def filter_by_similarity(df, keyword, top_n=None):
        texts = (
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

    # 検索語の入力
    search_word = st.text_input("🔍 検索ワードを入力してください（例：ヘモグロビン、QT間隔、ALT など）")

    if search_word:
        # 部分一致検索（全列対象）
        mask = df.apply(lambda row: row.astype(str).str.contains(search_word, case=False, na=False).any(), axis=1)
        results = df[mask].reset_index(drop=True)
        st.write(f"🔎 検索結果：{len(results)} 件ヒットしました")

        # 類似度ソートボタン
        if st.button("🔘 類似度の高い順にソート"):
            results = filter_by_similarity(results, search_word)
            st.write("🎯 類似度の高い順に並べ替えました")

        # 表示する列の順番を指定
        preferred_columns = [
            "Domain", "Code", "xxTESTCD", "xxTEST",
            "xxTEST-J", "CDISC Synonym(s)-J", "CDISC Definition-J", "NCI Preferred Term-J",
            "CDISC Synonym(s)", "CDISC Definition", "NCI Preferred Term"
        ]
        display_columns = [col for col in preferred_columns if col in results.columns]
        results = results[display_columns]

        # 表の表示
        st.dataframe(results, use_container_width=True)

    else:
        st.info("🔍 上のテキストボックスに検索語を入力してください。例：ALT、QT間隔、ヘモグロビン など")
