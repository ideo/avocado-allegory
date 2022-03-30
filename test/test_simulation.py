import unittest

# import pandas as pd

# from src.simulation import Simulation
# import src.logic as lg
from src import Simulation
from src import logic as lg


def construct_jenna_example_df():
    # TODO: Fra, can you help set this up, please?  I couldn't follow it.
    # if TEST_JENNAS_NUMBERS:
    #     self.num_townspeople = 7
    #     self.assigned_guacs = 6
    #     self.guac_df = pd.DataFrame([0,1,2,3,4,5], columns = ['Entrant'])
    #     self.guac_df['Objective Ratings'] = 0

    # if self.test_jennas_numbers:
    #     jennas_data = {}
    #     jennas_data[0] = [(2,2), (4,3), (5,1)]
    #     jennas_data[1] = [(2,2), (4,5), (5,10)]
    #     jennas_data[2] = [(2,7),(3,2), (4,3.3), (5,4)]
    #     jennas_data[3] = [(0,9), (1,9.5), (2,10), (3,3)]
    #     jennas_data[4] = [(0,9), (1,9.5), (3,0), (5,10)]
    #     jennas_data[5] = [(1,5), (3,4), (4,8)]
    #     jennas_data[6] = [(0,6),(1,8),(3,10),(4,7)]        
    #     sample_guac_df = pd.DataFrame(jennas_data[self.number], columns = ["ID", 'Subjective Ratings'])
    pass


class TestSimulation(unittest.TestCase):
    def setUp(self):
        # setUp and tearDown are run multiple times, before and after each test
        self.df = lg.get_scenario_dataframe("One Clear Winner")
        self.num_townspeople = 200
        self.assigned_guacs = 18

        self.sim = Simulation(
            self.df, 
            num_townspeople = self.num_townspeople,
            assigned_guacs = self.assigned_guacs,
            )


    def test_agent_construction(self):
        self.sim.create_agents()
        assert len(self.sim.townspeople) == self.num_townspeople


    def test_tasting_and_ballot_construction(self):
        self.sim.create_agents()
        self.sim.taste_and_vote()
        assert self.sim.results_df.shape[0] == self.df.shape[0]
        assert self.sim.results_df.shape[1] == self.num_townspeople + 1


    def tearDown(self):
        pass

        
if __name__ == '__main__':
    unittest.main()
