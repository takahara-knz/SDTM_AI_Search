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

    df = load_data()

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
    search_word = st.text_input("🔍 検索ワードを入力してください（例：ヘモグロビン、QT間隔 など）")

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
            "Domain", "xxTESTCD", "xxTEST",
            "xxTEST-J", "CDISC Synonym(s)-J", "CDISC Definition-J", "NCI Preferred Term-J",
            "CDISC Synonym(s)", "CDISC Definition", "NCI Preferred Term"
        ]
        display_columns = [col for col in preferred_columns if col in results.columns]
        results = results[display_columns]
        
  # st-aggrid が streamlit Cloud でエラーになるので、代わりに st.dataframe()を使う
  #      # AgGrid 設定
  #      gb = GridOptionsBuilder.from_dataframe(results)
  #      gb.configure_default_column(resizable=True, filter=True, sortable=True)
  #      for col in ["Domain", "xxTESTCD", "xxTEST"]:
  #          if col in results.columns:
  #              gb.configure_column(col, pinned="left")
  #      grid_options = gb.build()

  #      # 表の表示（高さは固定）
  #      AgGrid(
  #          results,
  #          gridOptions=grid_options,
  #          height=400,
  #          fit_columns_on_grid_load=False,
  #          theme="streamlit"
  #      )
        # 表の表示（AgGridの代わりに）
        st.dataframe(results, use_container_width=True)
