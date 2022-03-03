import pandas as pd

from .townspeople import Townsperson


class Simulation:
    def __init__(
            self, guac_df, num_townspeople, st_dev, 
            limit=20, perc_fra=0.0, perc_pepe=0.0
        ):
        print("what's going on>>>>>>???????")
        self.guac_df = guac_df
        self.num_townspeople = num_townspeople
        self.st_dev = st_dev
        self.limit = limit
        self.perc_fra = perc_fra
        self.perc_pepe = perc_pepe
        self.results_df = None
        self.objective_winner = guac_df[["Objective Ratings"]].idxmax()[0]


    def simulate(self):
        num_pepes = round(self.num_townspeople * self.perc_pepe)
        num_fras = round(self.num_townspeople * self.perc_fra)
        num_reasonable = self.num_townspeople - num_pepes - num_fras

        # This can be more DRY
        name = 0
        self.results_df = pd.DataFrame(index=self.guac_df.index)
        for _ in range(num_reasonable):
            person = Townsperson(name=name, st_dev=self.st_dev)
            self.results_df[person.name] = person.taste_and_vote(self.guac_df)
            name += 1

        for _ in range(num_pepes):
            offset = 3
            person = Townsperson(name=name, st_dev=self.st_dev, mean_offset=offset)
            self.results_df[person.name] = person.taste_and_vote(self.guac_df)
            name += 1

        for _ in range(num_fras):
            offset = -3
            person = Townsperson(name=name, st_dev=self.st_dev, mean_offset=offset)
            self.results_df[person.name] = person.taste_and_vote(self.guac_df)
            name += 1

        sum_of_votes = self.results_df.sum(axis=1)
        avg_of_votes = self.results_df.mean(axis=1)
        med_of_votes = self.results_df.median(axis=1)
        self.results_df["Sum"] = sum_of_votes
        self.results_df["Avg"] = avg_of_votes
        self.results_df["Med"] = med_of_votes
