import pandas as pd

from .townspeople import Townsperson


class Simulation:
    def __init__(
            self, guac_df, num_townspeople, st_dev, 
            num_guac_per_person=20, perc_fra=0.0, perc_pepe=0.0, method="sum"
        ):
        self.guac_df = guac_df
        self.num_townspeople = num_townspeople
        self.st_dev = st_dev
        self.num_guac_per_person = num_guac_per_person
        self.perc_fra = perc_fra
        self.perc_pepe = perc_pepe
        self.results_df = None
        self.objective_winner = guac_df[["Objective Ratings"]].idxmax()[0]
        self.fra_joe = 'joe'
        self.method = method.lower()


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

        cols_to_use = self.results_df.columns
        sum_of_votes = self.results_df[cols_to_use].sum(axis=1)
        avg_of_votes = self.results_df[cols_to_use].mean(axis=1)
        med_of_votes = self.results_df[cols_to_use].median(axis=1)
        self.results_df["sum"] = sum_of_votes
        self.results_df["avg"] = avg_of_votes
        self.results_df["med"] = med_of_votes

        self.winner = self.results_df[[self.method]].idxmax()[0]
