import streamlit as st
import pandas as pd

from .simulation import Simulation


def tune_simulation(guac_df):
    st.subheader("Tuning the Simulation")
    msg = """
    This process will exacerbate the ratio of tasters to sampling limit until 
    the simulated winner is no longer valid.
    """
    st.write(msg)
    num_guacs, num_townspeople, sl, st_dev = set_parameters(guac_df)
    tuning_df = load_dataframe()
      
    tune = st.button("Tune the Parameters")
    if tune:
        valid_results = True
        while valid_results:
            sim = Simulation(guac_df, num_townspeople, limit=sl, st_dev=st_dev)
            sim.simulate()
            valid_results = sim.objective_winner == sim.winner

            output = {
                "Guac Entrants":        num_guacs,
                "Townspeople":          num_townspeople,
                "Sampling Limit":       sl,
                "Std. Deviation":       st_dev,
                "Valid":                valid_results,
            }
            tuning_df = tuning_df.append(output, ignore_index=True)
            print(output)

            sl -= 1
            if num_townspeople < 100:
                num_townspeople += 10
            elif num_townspeople < 1000:
                num_townspeople += 50
            else:
                num_townspeople += 250

            if sl == 1:
                break

    # st.write(tuning_df) 
    save_dataframe(tuning_df)
    plot_results(tuning_df)
    st.markdown("___")


def set_parameters(guac_df):
    num_guac_entrants = guac_df.shape[0]
    col1, col2, col3 = st.columns(3)
    num_townspeople = col1.slider("How many townspeople taste and vote in the contest?",
        value=300,
        min_value=10,
        max_value=1000,
        step=10)
    sl = col2.slider("Set the Sampling Limit", 
        value=20, 
        min_value=1, 
        max_value=20)
    st_dev = col3.number_input("The Std. Deviation of voters' scores of the same guacs.", 
        value=3.0,
        min_value=0.5,
        max_value=5.0,
        step=0.5)
    return num_guac_entrants, num_townspeople, sl, st_dev


def load_dataframe():
    columns=[
        "Guac Entrants",
        "Townspeople", 
        "Sampling Limit",
        "Std. Deviation",
        "Valid"]

    try:
        df = pd.read_csv("tuning_df.csv")
        df.drop(columns=["Unnamed: 0"], inplace=True)
    except FileNotFoundError:
        df = pd.DataFrame(columns=columns)
    return df


def save_dataframe(df):
    df.to_csv("tuning_df.csv")


def plot_results(df):
    st.markdown("##### Plot the Results")
    col1, col2, col3 = st.columns(3)
    num_guacs = col1.selectbox(
        "Guac Entrants", 
        options=df["Guac Entrants"].value_counts().index.tolist()
        )
    st_dev = col2.selectbox(
        "Std. Deviation", 
        options=df["Std. Deviation"].value_counts().index.tolist()
        )

    chart_df = df[
        (df["Guac Entrants"] == num_guacs) &
        (df["Std. Deviation"] == st_dev)
        ]

    spec = {
        "mark": "point",
        "encoding": {
            "x": {"field": "Sampling Limit", "type": "quantitative"},
            "y": {"field": "Townspeople", "type": "quantitative"},
            "color": {"field": "Valid", "type": "nominal"},
            "shape": {"field": "Valid", "type": "nominal"}
            }
        }
    st.vega_lite_chart(chart_df, spec, use_container_width=True)
    # st.write(chart_df)