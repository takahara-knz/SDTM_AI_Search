import streamlit as st
from app import app1, app2 #, app3  # ← appフォルダから読み込む！

def main():
    st.set_page_config(page_title="おしえてねこちゃんメニュー", layout="wide")

    # ✅ 画面状態をセッションで保存
    if "selected_app" not in st.session_state:
        st.session_state["selected_app"] = "menu"

    # ✅ 表示制御
    if st.session_state["selected_app"] == "menu":
        st.title("おしえてねこちゃんメニュー🐾")
        option = st.radio("検索メニューを選択してください", ["1️⃣ xxTEST検索", "2️⃣ ドメイン検索（テスト中なので嘘を言うかも）", "3️⃣ よろず検索（永遠に工事中）"])
        if st.button("スタート！"):
            if "xxTEST" in option:
                st.session_state["selected_app"] = "app1"
            elif "ドメイン" in option:
                st.session_state["selected_app"] = "app2"
            else:
                st.info("よろず検索は永遠に工事中です…👷")
            # st.experimental_rerun()  # ← 状態更新した直後に再描画！

    elif st.session_state["selected_app"] == "app1":
        app1.run_app()

    elif st.session_state["selected_app"] == "app2":
        app2.run_app()

    elif st.session_state["selected_app"] == "app3":
        st.info("ごめんニャ〜！よろず検索は永遠に工事中")

main()
