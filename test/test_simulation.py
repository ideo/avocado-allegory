import unittest

from src import Simulation
from src import logic as lg


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
