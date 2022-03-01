import streamlit as st
import pandas as pd

from .config import OBJECTIVE_RANKINGS


def objective_ratings():
    col1, col2 = st.columns([2,5])
    scenario = col1.radio("Choose a scenario", options=OBJECTIVE_RANKINGS.keys())

    data = pd.DataFrame(columns=["Rankings"], data=OBJECTIVE_RANKINGS[scenario])
    data["Entrant"] = data.index

    spec = {
        "mark": {"type": "bar"},
        "encoding": {
            "x":    {"field": "Entrant", "tupe": "nominal"},
            "y":    {"field": "Rankings", "type": "quantitative"},
        },
        "title":    scenario,   
    }

    col2.vega_lite_chart(data, spec)