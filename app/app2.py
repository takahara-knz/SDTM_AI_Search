import streamlit as st
import pandas as pd

def run_app():
    st.title("さがしてねこちゃん: ドメイン検索")

    # ✅ 辞書読み込み（dataフォルダから）
    @st.cache_data
    def load_dictionary():
        return pd.read_excel("data/NekoDic.xlsx")

    dic = load_dictionary()

    # ✅ 検索入力
    user_input = st.text_input("検索語を入力してください（例：性別、生年月日）")

    if user_input:
        # 検索処理（部分一致、大小文字区別なし）
        results = dic[dic["Term"].str.contains(user_input, case=False, na=False)]

        if not results.empty:
            st.success("候補が見つかったよ！")
            st.dataframe(
                results[["Term", "Domain", "Variable", "Putpose", "Hint"]].reset_index(drop=True),
                use_container_width=True
            )
        else:
            st.warning("候補が見つからなかったよ…")
            st.info("xxTESTの検索で探してみてね！（VSやLBのTEST項目など）")

    # ✅ 戻るボタン（メニュー画面へ）
    if st.button("← メニューに戻る"):
        st.session_state["selected_app"] = "menu"
        # st.experimental_rerun() ← 必要なら追加。今は安定動作を優先でOK！
