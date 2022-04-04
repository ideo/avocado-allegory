from src import logic as lg
from src import Simulation


def test_election():
    # scenario = "A Close Call"
    scenario = "A Lot of Contenders"
    df = lg.get_scenario_dataframe(scenario)

    num_townspeople = 200
    st_dev = 3
    method = "rank"
    sim = Simulation(df, 
        num_townspeople=num_townspeople, 
        st_dev=st_dev,
        method=method,
        seed=43
        )
    sim.simulate()


if __name__ == "__main__":
    test_election()