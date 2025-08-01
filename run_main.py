import streamlit.web.cli as stcli
import sys
import os

def streamlit_run():
    # Web版のstreamlit_app.py（1階層上のSDTM_AI_Search内）を指定
    script_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "SDTM_AI_Search", "streamlit_app.py")
    )
    sys.argv = ["streamlit", "run", script_path, "--global.developmentMode=false"]
    sys.exit(stcli.main())

if __name__ == "__main__":
    streamlit_run()