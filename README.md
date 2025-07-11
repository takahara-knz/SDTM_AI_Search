# 🐾 おしえてねこちゃん：CDISC Terminology 検索ツール

このツールは、CDISC/SDTMに関する検索ができるツールです。

現在は、SDTM Terminologyの、Findings ドメインの `xxTESTCD` / `xxTEST` を対象に、  
**日本語・英語のキーワードで検索・類似語探索ができるWebアプリ**だけです。  
Streamlit を使って構築されており、**インストール不要・ブラウザだけで利用可能**です。

コードは全部copilotさんが書いてくれました。私はpython書けません。

---

## 🚀 アプリを使う

▶️ Webアプリはこちら（Streamlit Cloud）  
https://sdtmaisearch.streamlit.app/

⚠️ アプリが表示されない場合：
- 職場や病院などのネットワークでは、セキュリティ制限により表示されないことがあります
- その場合は、スマホのテザリングや自宅のWi-Fiでお試しください


---

## 🔍 主な機能

- キーワードによる部分一致検索（日本語・英語対応）
- TF-IDF + コサイン類似度による類似語ランキング
- CDISC用語の日本語訳・定義・シノニム表示
- インタラクティブな表（フィルタ・ソート・固定列）

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
