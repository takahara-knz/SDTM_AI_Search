import streamlit as st
from app import app1, app2, app3  # 各アプリをモジュールとして読み込む

st.sidebar.title("📚 おしえてねこちゃんメニュー")
app_choice = st.sidebar.radio("機能を選択してください", ["xxTEST検索", "機能2", "機能3"])

if app_choice == "xxTESTCD/xxTEST検索（Findings系ドメイン検索）":
    app1.run()
#elif app_choice == "機能2":
#    app2.run()
#elif app_choice == "機能3":
#    app3.run()