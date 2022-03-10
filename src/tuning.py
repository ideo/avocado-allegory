import streamlit as st
import pandas as pd
import numpy as np

from .simulation import Simulation
import matplotlib.pyplot as plt

def create_histogram(guac_df):

    num_guacs = 20
    nt_color_map = {50: 'orange', 100: 'blue', 200: 'green', 400: 'grey'}

    
    for std in [1,2,3]:
        rows = []
        for nt in [50,100,200]:
            row = {}    
            row['std'] = std
            row['nt'] = nt

            min_guac_to_recover_winners = run_a_bunch_of_simulations(num_guacs, guac_df, nt, std)

            row['guacs_limit'] = '|'.join([str(i) for i in min_guac_to_recover_winners])

            plt.hist(min_guac_to_recover_winners, 
                    density = True, 
                    label = nt, 
                    color = nt_color_map[nt], 
                    alpha = 0.5)
            rows.append(row)

        df = pd.DataFrame(rows)
        df.to_csv(f"Distribution_varying_townpeople_{std}_std_{num_guacs}total_guacs.csv")
        plt.xlabel('# guacs/person yielding true winner')
        plt.ylabel('%')
        plt.title(f"Initial number of guacs = {num_guacs}, standard dev on people score = {std}")
        plt.legend(loc = 2)
        plt.ylim(0, 0.8)
        plt.savefig(f"Distribution_varying_townpeople_{std}stev_{num_guacs}total_guacs.pdf")
        plt.close()
    # import pdb;pdb.set_trace()

def run_a_bunch_of_simulations(num_guacs, guac_df, nt, std):
    min_guac_to_recover_winners = []
    min_guac_to_recover_winner = 20
    for n in range(200):
        print('nt = ', nt, 'n = ', n)
        
        for ngpp in range(num_guacs, 0, -1):

            sim = Simulation(guac_df, nt, std, assigned_guacs=ngpp)
            
            sim.simulate() 
            
            if sim.objective_winner == sim.condorcet_winner:
                min_guac_to_recover_winner = ngpp
            else:
                min_guac_to_recover_winners.append(min_guac_to_recover_winner)
                break
    
    return min_guac_to_recover_winners
    


def tune_simulation(guac_df):
    st.subheader("Tuning the Simulation")
    msg = """
    This process will exacerbate the ratio of tasters to sampling limit until 
    the simulated winner is no longer valid.
    """
    st.write(msg)

    num_guacs, num_townspeople, assigned_guacs, st_dev = set_parameters(guac_df)
    tuning_df = load_dataframe()
      
    tune = st.button("Tune the Parameters")
    if tune:
        # valid_results = True
        # while valid_results:
        for _ in range(100):
            for num_townspeople in [10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300, 350, 400]:
                for assigned_guacs in np.linspace(2, 20, 19):
                    print(num_townspeople, assigned_guacs)
                
                    sim = Simulation(guac_df, num_townspeople, assigned_guacs=assigned_guacs, st_dev=st_dev)
                    sim.simulate()
                    valid_results = sim.objective_winner == sim.winner

                    output = {
                        "Guac Entrants":        num_guacs,
                        "Townspeople":          num_townspeople,
                        "Sampling Limit":       assigned_guacs,
                        "Std. Deviation":       st_dev,
                        "Valid":                valid_results,
                    }
                    tuning_df = tuning_df.append(output, ignore_index=True)
                    print(output)

                    # assigned_guacs -= 1
                    # if num_townspeople < 100:
                    #     num_townspeople += 10
                    # elif num_townspeople < 1000:
                    #     num_townspeople += 50
                    # else:
                    #     num_townspeople += 250

                    # if assigned_guacs == 1:
                    #     break

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
        value=1.5,
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
    col1, col2 = st.columns(2)
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

    # spec = {
    #     "mark": {"type": "point", "tooltip": True},
    #     "title": {
    #         "text": "Simulation Tuning",
    #         "subtitle": f"{num_guacs} guacamoles, tasters votes vary +/- {st_dev}"},
    #     "encoding": {
    #         "x": {"field": "Sampling Limit", "type": "quantitative"},
    #         "y": {"field": "Townspeople", "type": "quantitative"},
    #         "color": {"field": "Valid", "type": "nominal"},
    #         "shape": {"field": "Valid", "type": "nominal"}
    #         }
    #     }

    chart_df["Sampling Limit (Valid)"] = chart_df[chart_df["Valid"]]["Sampling Limit"]
    chart_df["Sampling Limit (Invalid)"] = chart_df[~chart_df["Valid"]]["Sampling Limit"]
    chart_df["Townspeople (Valid)"] = chart_df[chart_df["Valid"]]["Townspeople"]
    chart_df["Townspeople (Invalid)"] = chart_df[~chart_df["Valid"]]["Townspeople"]

    scatter_plot = {
            "mark": {"type": "point", "tooltip": True},
            "encoding": {
                "x": {"field": "Sampling Limit", "type": "quantitative"},
                "y": {"field": "Townspeople", "type": "quantitative"},
                "color": {"field": "Valid", "type": "nominal"},
                "shape": {"field": "Valid", "type": "nominal"}
                }
            }

    spec = {
        "title": {
            "text": "Simulation Tuning",
            "subtitle": f"{num_guacs} guacamoles, tasters votes vary +/- {st_dev}"},
        "vconcat":  [
            {
            "hconcat":  [scatter_plot,
            {
            "mark": "bar",
            "encoding": {
                "x": {
                    "bin": True, 
                    "field": "Sampling Limit (Valid)", 
                    "scale": {"domain": [0, 20]},
                    # "axis": None,
                    },
                "y": {"aggregate": "count"},
                "color": {"value": "#ff9900"}
                }
            },
            scatter_plot],
        },
            {
                "hconcat":  [{
                "mark": "bar",
                "encoding": {
                    "y": {
                        "bin": True, 
                        "field": "Townspeople (Invalid)", 
                        "scale": {"domain": [0, int(chart_df["Townspeople"].max())]},
                        # "axis": None,
                        },
                    "x": {"aggregate": "count"},
                    # "color": {"value": "#ff9900"}
                    }
            },
            scatter_plot,
            {
                "mark": "bar",
                "encoding": {
                    "y": {
                        "bin": True, 
                        "field": "Townspeople (Valid)", 
                        "scale": {"domain": [0, int(chart_df["Townspeople"].max())]},
                        # "axis": None,
                        },
                    "x": {"aggregate": "count"},
                    "color": {"value": "#ff9900"}
                    }
            }
            ]},
            {"hconcat": [scatter_plot,
                {
            "mark": "bar",
            "encoding": {
                "x": {
                    "bin": True, 
                    "field": "Sampling Limit (Invalid)", 
                    "scale": {"domain": [0, 20]},
                    # "axis": None,
                    },
                "y": {"aggregate": "count"},
                }
            },scatter_plot]}]
    }
    st.vega_lite_chart(chart_df, spec, use_container_width=True)
    # st.write(chart_df)
    
    invalid_results = chart_df[~chart_df["Valid"]]
    invalid_results["Ratio"] = \
        invalid_results["Townspeople"] / invalid_results["Sampling Limit"]
    # st.write(invalid_results)
