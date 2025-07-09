import streamlit as st
st.set_page_config(layout="wide") # ページ設定（ワイド表示）

from app import app1  # 今は app1 のみ

st.sidebar.title("📚 おしえてねこちゃんメニュー")
#app_choice = st.sidebar.radio("機能を選択してください", [
#    "xxTESTCD/xxTEST検索（Findings系ドメイン検索）",
#    "機能2（準備中）",
#    "機能3（準備中）"
#])

#if app_choice == "xxTESTCD/xxTEST検索（Findings系ドメイン検索）":
    app2.run()
#elif app_choice == "機能2（準備中）":
#    app2.run()
#elif app_choice == "機能3（準備中）":
#    app3.run()
