
import dtale
import pandas as pd
from dtale.views import startup
from dtale.app import get_instance
import streamlit as st
import requests

CSS = """
<style>
    div.sidebar-content {
      padding: 1rem !important;
    }
    section.main div.block-container {
      padding: 3rem 1rem 1rem !important;
    }
    div.block-container > div:first-child {
      height: 100%;
    }
    div.block-container > div > div.element-container:first-child,
    div.block-container > div > div.element-container:last-child {
      height: 45%;
      margin: 0;
    }
    div.block-container > div > div.element-container:nth-child(2) {
      margin: 0;
      margin: 0.5rem 0 0.5rem;
    }
    div.block-container div.markdown-text-container {
      height: 100%;
    }
    div.sidebar-content {
      width: 40rem !important;
    }
    div.sidebar-content pre {
      font-size: 10px;
    }
    div.Widget.row-widget.stRadio > div{
      flex-direction:row;
    }
    div.stBlock-horiz div.stBlock:first-child {
      margin-top: auto;
      margin-bottom: auto;
    }
    div.stBlock-horiz div.stBlock:first-child > div {
      margin-top: 1em;
    }
</style> 
"""
PREAMBLE = (
    "# DISCLAIMER: 'df' refers to the data you passed in when calling 'dtale.show'\n\n"
    "import pandas as pd\n\n"
    "if isinstance(df, (pd.DatetimeIndex, pd.MultiIndex)):\n"
    "\tdf = df.to_frame(index=False)\n\n"
    "# remove any pre-existing indices for ease of use in the D-Tale code, but this is not required\n"
    "df = df.reset_index().drop('index', axis=1, errors='ignore')\n"
    "df.columns = [str(c) for c in df.columns]  # update columns to strings in case they are numbers"
)

runsheet = st.file_uploader("Upload Runsheet", type="xlsx")

curr_instance1 = get_instance("1")
curr_instance2 = get_instance("2")
if curr_instance1 is None:
    summary = pd.read_excel(runsheet, sheet_name="Summary", header=[0, 1])
    # dtale.show(summary)
    startup(data_id="1",data=summary)
    curr_instance1 = get_instance("1")
if curr_instance2 is None:
    sim = pd.read_excel(runsheet, sheet_name="SIM Raw", header=[0, 1])
    startup(data_id="2", data=sim)
    # dtale.show(sim)
    curr_instance2 = get_instance("2")

#{CSS}
html = f"""
<p><a href="/dtale/main/1" target="_blank">Dataframe 1</a></p>
<iframe src="/dtale/main/1" style="height: 400%;width: 100%"/>
"""

#<iframe src="/dtale/main/2" style="height: 100%;width: 100%"/>
st.write(html, unsafe_allow_html=True)



# col1, col2 = st.beta_columns((1, 3))
# reload_columns = col1.button("Reload")
# columns = [c for c in curr_instance1.data.columns]
# if reload_columns:
#     curr_instance1 = get_instance("1")
#     columns = [c for c in curr_instance1.data.columns]
# selected_column = col2.radio("Column Analysis", columns)

# st.markdown(
#     f'<iframe src="/dtale/popup/column-analysis/1?selectedCol={selected_column}" style="height: 100%;width: 100%"/>',
#     unsafe_allow_html=True,
# )

# st.sidebar.title("Building Code w/ D-Tale")
# reload_code = st.sidebar.button("Reload Code")
# code = requests.get("http://localhost:8501/dtale/code-export/1").json()["code"]
# if reload_code:
#     code = requests.get("http://localhost:8501/dtale/code-export/1").json()["code"]
# code = code.replace(
#     PREAMBLE,
#     "import pandas as pd\n\ndf = pd.DataFrame([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])",
# )
# if not code:
#     code = "import pandas as pd\n\ndf = pd.DataFrame([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"
# st.sidebar.markdown(f"<pre>{code}</pre>", unsafe_allow_html=True)
