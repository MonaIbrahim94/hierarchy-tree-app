import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Streamlit Page Setup
# ------------------------------------------------------------
st.set_page_config(page_title="Hierarchy Treemap", layout="wide")
st.title("Data Hierarchy")

# ------------------------------------------------------------
# Hierarchy Columns (in order)
# ------------------------------------------------------------
HIER_COLS = [
    "Data Domain L1",
    "Data Domain L2",
    "Data Domain L3",
]

# ------------------------------------------------------------
# Load CSV
# ------------------------------------------------------------
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    return df

df = load_data("data/Hierarchy.csv")

# ------------------------------------------------------------
# Sidebar: Optionally upload alternative CSV
# ------------------------------------------------------------
with st.sidebar:
    uploaded = st.file_uploader("Upload CSV (same column names)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.success("✅ File uploaded!")

# ------------------------------------------------------------
# Filter required columns
# ------------------------------------------------------------
df = df[HIER_COLS].copy()

# Clean
INVALIDS = {"nan", "none", "undefined", ""}
for col in HIER_COLS:
    df[col] = (
        df[col]
        .astype(str)
        .str.strip()
        .apply(lambda x: None if x.lower() in INVALIDS else x)
    )

# ------------------------------------------------------------
# Build Treemap
# ------------------------------------------------------------
fig = px.treemap(
    df,
    path=HIER_COLS,
)

fig.update_layout(
    height=900,   # Big chart
)

fig.update_traces(
    textfont_size=18,   # Larger labels
)

st.plotly_chart(fig, use_container_width=True)
