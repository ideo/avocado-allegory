from collections import Counter

import pandas as pd

from src.simulation import Simulation
from src.config import ENTRANTS


def simulate_N_times(sim_params, scenario, N=100):
    """
    Run the simulation N times and record how many times each person won
    """
    guac_df = choose_scenario(scenario)
    filename = f"data/simulate_{N}_times_sum.csv"
    results_df = load_dataframe(sim_params, filename)

    sim = Simulation(guac_df, **sim_params)
    winners = []
    for ii in range(N):
        sim.simulate()
        winner_this_round = str(sim.sum_winner)
        print(f"Round {ii} winner is... Guac #{winner_this_round}")
        winners.append(winner_this_round)

    results = {**sim_params, **Counter(winners)}
    results["scenario"] = scenario
    results_df = results_df.append(pd.Series(data=results), ignore_index=True)
    results_df.to_csv(filename)


def choose_scenario(scenario):
    df = pd.DataFrame(data=ENTRANTS)
    df["Objective Ratings"] = df[scenario].copy()
    return df


def load_dataframe(sim_params, filename):
    try:
        df = pd.read_csv(filename)
        df.drop(columns=["Unnamed: 0"], inplace=True)
    except FileNotFoundError:
        # Create Dataframe
        columns = list(sim_params.keys()) + ["scenario"]
        df = pd.DataFrame(columns=columns)
    return df


if __name__ == "__main__":

    st_dev = 1.0
    for assigned_guacs in range(2, 21):

        sim_params = {
            "num_townspeople":  200,
            "st_dev":           st_dev,
            "assigned_guacs":   assigned_guacs,
            "perc_fra":         0.0,
            "perc_pepe":        0.0,
            "perc_carlos":      0.0,
        }
        scenarios = [
            "One Clear Winner",
            "A Close Call",
            "A Lot of Contenders",
        ]
        N = 100

        for scenario in scenarios:
            simulate_N_times(sim_params, scenario, N)