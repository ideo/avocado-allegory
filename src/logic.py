import streamlit as st
import pandas as pd

from .config import OBJECTIVE_RATINGS


def objective_ratings():
    col1, col2 = st.columns([2,5])
    scenario = col1.radio(
        "Choose a scenario", 
        options=OBJECTIVE_RATINGS.keys())

    df = pd.DataFrame(
        columns=["Objective Ratings"], 
        data=OBJECTIVE_RATINGS[scenario])
    df["Entrant"] = df.index

    spec = {
        "mark": {"type": "bar"},
        "encoding": {
            "x":    {"field": "Entrant", "tupe": "nominal"},
            "y":    {"field": "Objective Ratings", "type": "quantitative"},
        },
        "title":    scenario,   
    }

    col2.vega_lite_chart(df, spec)
    return df


def simulation_parameters():
    col1, _, col2 = st.columns([4, 1, 4])
    num_townspeople = col1.slider("How many townspeople are there?", 
        value=250, 
        min_value=10, 
        max_value=500)
    st_dev = col2.number_input("What is the st. dev. of their randomly generated scores?",
        value=1.0,
        min_value=0.1,
        max_value=5.0,
        step=0.1
        )
    return num_townspeople, st_dev
    

def tally_votes(sim):
    col1, col2 = st.columns([2,5])
    method = col1.radio(
        "How would you like to tally the votes?",
        options=[
            "Sum up all the scores", 
            "Compute the average",
            "Compute the median"]
    )
    if method == "Sum up all the scores":
        y_field = "Sum"
    elif method == "Compute the average":
        y_field = "Avg"
    else:
        y_field = "Med"

    # y_field = "Sum" if method == "Sum up all the scores" else "Avg"
    chart_df = sim.results_df[[y_field]]
    winning_guac = chart_df.idxmax()[0]
    chart_df["Entrant"] = sim.guac_df["Entrant"]

    spec = {
        "mark": {"type": "bar"},
        "encoding": {
            "x":    {"field": "Entrant", "tupe": "nominal"},
            "y":    {"field": y_field, "type": "quantitative"},
        },
        "title":    f"Our Winner is Guacamole No. {winning_guac}!",   
    }
    col2.vega_lite_chart(chart_df, spec)
    return y_field


def declare_a_winner(sim, y_field):
    winning_guac = sim.results_df[[y_field]].idxmax()[0]
    top_score = sim.results_df[[y_field]].max()

    # Make sure only one guac got the top score
    if (sim.results_df[[y_field]] == top_score).astype(int).sum(axis=0)[0] > 1:
        st.text("Oh no! We have a tie!")
    elif winning_guac == sim.objective_winner:
        st.text("Hooray! Democracy Prevails!")
    else:
        st.text("Oh no! We done fucked up!")



# Not getting here yet
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