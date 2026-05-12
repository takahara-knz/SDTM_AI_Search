import streamlit as st
from app import app1, app2, app3, app4  # ← appフォルダから読み込む！

st.cache_data.clear()

def main():
    st.set_page_config(page_title="おしえてねこちゃんメニュー", layout="wide")

    # ✅ 画面状態をセッションで保存
    if "selected_app" not in st.session_state:
        st.session_state["selected_app"] = "menu"

    # ✅ ライセンス表示テキスト
    lictxt  =   ("※Terminologyのデータは、米国国立がん研究所（NCI）が以下のページで公開しているCDISC Terminology（SDTM）を加工し、Google翻訳結果を付加したものです。"
                 "<br>"
                 "　出典：https://www.cancer.gov/about-nci/organization/cbiit/vocabulary/cdisc"
                 "<br>"
                 "　The National Cancer Institute (NCI) does not endorse this translation and no endorsement by NCI should be inferred."
                )

    # ✅ 表示制御
    if st.session_state["selected_app"] == "menu":
        st.title("🐱おしえてねこちゃんメニュー🐾")
        st.write("※ボタンを押しても動かない場合は、もう１回押してください")
        option = st.radio("検索メニューを選択してください", 
                          ["1️⃣ Findings系(xxTESTCD&xxTEST)Terminology検索", 
                           "2️⃣ ドメイン検索（テスト中なので嘘を言うかも）", 
                           "3️⃣ ドメイン概要表示（SDTMIG V3.3）→非公開", 
                           "4️⃣ Findings系(xxTESTCD&xxTEST)以外のTerminology検索（SDTMIG V3.3）" ,
                           "👷 よろず検索 → NotebookLMで環境構築をお勧め"])
        st.markdown(lictxt, unsafe_allow_html=True)
        if st.button("スタート！"):
            if "Findings系(xxTESTCD&xxTEST)Terminology" in option:
                st.session_state["selected_app"] = "app1"
            elif "ドメイン検索" in option:
                st.session_state["selected_app"] = "app2"
            elif "ドメイン概要" in option:
                st.info("このメニューは非公開です🙇‍♀️")
            elif "Findings系(xxTESTCD&xxTEST)以外のTerminology" in option:
                st.session_state["selected_app"] = "app4"
            else:
                st.info("NotebookLM の環境構築はこちら → https://github.com/takahara-knz/SDTM_NotebookLM")
            # st.experimental_rerun()  # ← 状態更新した直後に再描画！

    elif st.session_state["selected_app"] == "app1":
        app1.run_app()

    elif st.session_state["selected_app"] == "app2":
        app2.run_app()

#    elif st.session_state["selected_app"] == "app3":
#        app3.run_app()

    elif st.session_state["selected_app"] == "app4":
        app4.run_app()

    elif st.session_state["selected_app"] == "app5":
        st.info("ごめんニャ〜！よろず検索は永遠に工事中")

main()




