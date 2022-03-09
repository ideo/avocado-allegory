import pandas as pd

from .townspeople import Townsperson


class Simulation:
    def __init__(
            self, guac_df, num_townspeople, st_dev, 
            num_guac_per_person=20, perc_fra=0.0, perc_pepe=0.0, 
            fullness_factor=0
        ):
        self.guac_df = guac_df
        self.num_townspeople = num_townspeople
        self.st_dev = st_dev
        self.fullness_factor = fullness_factor
        self.num_guac_per_person = num_guac_per_person
        self.perc_fra = perc_fra
        self.perc_pepe = perc_pepe
        self.results_df = None
        self.objective_winner = guac_df[["Objective Ratings"]].idxmax()[0]
        self.winner = None
        self.fra_joe = 'joe'
        # self.method = method.lower()


    def simulate(self):
        num_pepes = round(self.num_townspeople * self.perc_pepe)
        num_fras = round(self.num_townspeople * self.perc_fra)
        num_reasonable = self.num_townspeople - num_pepes - num_fras

        name = 0
        self.results_df = pd.DataFrame(index=self.guac_df.index)

        person_types = [num_reasonable, num_pepes, num_fras]
        mean_offsets = [0, 3, -3]

        for num_people, offset in zip(person_types, mean_offsets):
            for _ in range(num_people):
                person = Townsperson(name=name, st_dev=self.st_dev, num_guac_per_person=self.num_guac_per_person, mean_offset=offset, fullness_factor=self.fullness_factor)
                self.results_df[person.name] = person.taste_and_vote(self.guac_df)
                name += 1

        self.results_df["sum"] = self.results_df.sum(axis=1)
        self.winner = self.results_df[["sum"]].idxmax()[0]

        # sum_of_votes = self.results_df.sum(axis=1)
        # avg_of_votes = self.results_df.mean(axis=1)
        # med_of_votes = self.results_df.median(axis=1)
        # self.results_df["sum"] = sum_of_votes
        # self.results_df["avg"] = avg_of_votes
        # self.results_df["med"] = med_of_votes

        
