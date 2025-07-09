def run():
    try:
        st.title("CDISC Terminology 検索ツール（xxTEST 系）")
        st.write("✅ タイトル表示完了")


        @st.cache_data
        def load_data():
            st.write("📥 データ読み込み開始")
#            return pd.read_excel("data/00.TerminologyMerge.xlsx")
            df = pd.read_excel("data/00.TerminologyMerge.xlsx")
            st.success("✅ データ読み込み成功")
        except Exception as e:
            st.error(f"❌ データ読み込みエラー: {e}")
            return

        df = load_data()
        st.write("✅ データ読み込み完了")

        search_word = st.text_input("🔍 検索ワードを入力してください（例：ヘモグロビン、QT間隔 など）")
        st.write(f"🔎 入力された検索語: {search_word}")

        if search_word:
            st.write("🔍 検索処理開始")
            mask = df.apply(lambda row: row.astype(str).str.contains(search_word, case=False, na=False).any(), axis=1)
            results = df[mask].reset_index(drop=True)
            st.write(f"🔎 検索結果：{len(results)} 件ヒットしました")

            if st.button("🔘 類似度の高い順にソート"):
                results = filter_by_similarity(results, search_word)
                st.write("🎯 類似度の高い順に並べ替えました")

            preferred_columns = [
                "Domain", "xxTESTCD", "xxTEST",
                "xxTEST-J", "CDISC Synonym(s)-J", "CDISC Definition-J", "NCI Preferred Term-J",
                "CDISC Synonym(s)", "CDISC Definition", "NCI Preferred Term"
            ]
            display_columns = [col for col in preferred_columns if col in results.columns]
            results = results[display_columns]

            st.dataframe(results, use_container_width=True)

        else:
            st.info("🔍 左上のテキストボックスに検索語を入力してください。")

    except Exception as e:
        st.error(f"⚠️ エラーが発生しました: {e}")
