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


def types_of_voters():
    col1, col2, col3 = st.columns(3)
    pepe = col1.slider(
        "What percentage of people in town are like Precocious Pepe?",
        value=10,
        min_value=0,
        max_value=30,
        format="%g%%")

    fra = col2.slider(
        "What percentage of people in town are like Finicky Francisca?",
        value=8,
        min_value=0,
        max_value=30,
        format="%g%%")

    carlos = col3.slider(
        "What percentage of people in town are friends with Cliquey Carlos?",
        value=12,
        min_value=0,
        max_value=30,
        format="%g%%")

    return pepe, fra, carlos