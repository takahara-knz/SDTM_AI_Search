import pandas as pd
import streamlit as st
import os

def run_app():

    st.set_page_config(page_title="おしえてねこちゃん", layout="wide")  # ←横幅MAX✨

    # dataのパスを取得
    current_dir = os.path.dirname(__file__)
    # excel_path = os.path.join(current_dir, "..", "data", "stdmig_v3.3_tables_和訳付き.xlsx")
    excel_path = "/mount/src/sdtm_ai_search/data/sdtmig_v3.3_tables_和訳付き.xlsx"
    st.write("Excelファイルのパス:", excel_path)
    st.write("このファイル存在する？", os.path.exists(excel_path))
    # Excelファイルからシートごとに読み込む
    table0_df = pd.read_excel(excel_path, sheet_name="Table0")
    table1_df = pd.read_excel(excel_path, sheet_name="Table1")
    table2_df = pd.read_excel(excel_path, sheet_name="Table2")

    # ドメイン選択
    domain_list = sorted(table1_df["Domain"].unique())
    selected_domain = st.selectbox("検索するドメインを選んでねこ:", domain_list)

    # Table0から概要を抽出
    domain_overview = table0_df[table0_df["Domain"] == selected_domain]

    # Table1から作成単位を抽出
    domain_info = table1_df[table1_df["Domain"] == selected_domain]

    # Table2から項目表を抽出
    domain_items = table2_df[table2_df["Domain"] == selected_domain]

    # 結果表示
    st.subheader(f"🐾 {selected_domain} ドメインの概要")
    st.dataframe(domain_overview)

    st.subheader(f"🍡 {selected_domain} ドメインの作成単位")
    st.dataframe(domain_info)

    st.subheader(f"📋 {selected_domain} ドメインの項目一覧")
    st.dataframe(domain_items)

    # ✅ 戻るボタン（メニュー画面へ）
    if st.button("← メニューに戻る"):
        st.session_state["selected_app"] = "menu"
        # st.experimental_rerun() ← 必要なら追加。今は安定動作を優先でOK！
