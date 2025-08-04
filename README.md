# 🐱 おしえてねこちゃん：CDISC/SDTMお助けツール🐾

このツールは、CDISC/SDTMに関する検索ができるツールです。
まだまだ機能アップ中✨

Streamlit を使って構築されており、**インストール不要・ブラウザだけで利用可能**です。

コードは全部copilotさんが書いてくれました。GitHubのここの持ち主はpythonもREADME.mdも書けません。

---

## 🚀 アプリを使う

▶️ Webアプリはこちら（Streamlit Cloud）
https://sdtmaisearch.streamlit.app/

⚠️ アプリが表示されない場合：
- 職場や病院などのネットワークでは、セキュリティ制限により表示されないことがあります
- その場合は、スマホのテザリングや自宅のWi-Fiなどでお試しください

---

## 🔍 主な機能
1️⃣ Findings系(xxTESTCD&xxTEST)Terminology検索
- xxTESTCDとxxTESTがペアになっているTerminologyの検索
- キーワードによる部分一致検索（日本語・英語対応）
- TF-IDF + コサイン類似度による類似語ランキング

2️⃣ ドメイン検索（テスト中なので嘘を言うかも）
- 項目名（例えば「生年月日」など）を入れて、どのドメインかを検索
- ドメインの他、変数名が決まっていれば表示、ほかTipsなど

3️⃣ ドメイン概要表示（SDTMIG V3.3）
- ドメインを指定したら、概要や作成単位、変数表を表示

4️⃣ Findings系(xxTESTCD&xxTEST)以外のTerminology検索（SDTMIG V3.3）
- メニューの1️⃣以外のTerminology（例えばFREQなど）の検索
- TF-IDF + コサイン類似度による類似語ランキング、完全一致、部分一致から選択可能

👷 よろず検索（永遠に工事中🙏）
- 今のところ実装の目途なし

---

## 🛠️ セットアップ（開発者向け）

```bash
# 仮想環境の作成（任意）
python -m venv venv
source venv/bin/activate  # Windowsなら venv\Scripts\activate

# ライブラリのインストール
pip install -r requirements.txt

# アプリの起動
streamlit run streamlit_app.py
```
---

## 📦 配布・コピー時の注意点
- /app フォルダと /data フォルダは run_main.py と同じ階層に配置してください。
- Excelファイルのパスは data/data1.xlsx のように相対パスで記述されています。
- 配布時は /app と /data を 忘れずに一緒にコピーしてください。

## 🔧 使用ライブラリ

本ツールでは以下のPythonライブラリを使用しています：(説明はcopilotさん語録)
- **streamlit**：アプリのインターフェースを構築するふかふか舞台演出ツール  
- **pandas**：Excelデータの読込や加工を担当するデータ職人  
- **scikit-learn**：AI検索（類似度計算）に使用される思考エンジン  
- **janome**：日本語の分かち書きを可能にするテキスト職人  
- **openpyxl**：Excelファイルの読込を裏で支える助演俳優（`pandas.read_excel()` の内部依存）

---

## 🐱 ねこちゃんからのひとこと 🐾

このREADMEを読んでくれてありがとう。  
ツールはまだまだ工事中だけど、あなたのおしごとがちょっとでも楽になりますように🐱✨
