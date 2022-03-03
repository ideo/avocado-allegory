from copy import copy
from dataclasses import replace

import numpy as np
import pandas as pd


class Townsperson:
    def __init__(self, name, st_dev=1, limit=20):
        self.name = name
        self.st_dev = st_dev
        self.limit = limit

    def taste_and_vote(self, guac_df):
        """
        Randomly select guacs from the dataframe to taste.
        Taste and generate 'subjective' rating.
        """
        # Choose guacs
        guacs_to_try = np.random.choice(guac_df.index.tolist(), 
            size=self.limit, 
            replace=False)

        # Taste
        votes = {}
        for guac_id in guacs_to_try:
            obj_score = guac_df["Objective Ratings"].iloc[guac_id]
            sbj_score = self.taste(obj_score)
            votes[guac_id] = sbj_score

        votes_cast = pd.DataFrame(index=guac_df.index)
        votes_cast["Vote"] = pd.Series(votes)
        return votes_cast
        # votes_cast = pd.DataFrame(index=guac_df.index, columns=["Vote"])
        # votes_cast["Vote"] = guac_df["Objective Ratings"].apply(
        #     lambda obj_rating: self.taste(obj_rating)
        # )
        # return votes_cast


    def taste(self, obj_rating):
        subj = np.random.normal(loc=obj_rating, scale=self.st_dev)
        subj = round(subj)
        subj = 10 if subj > 10 else subj
        subj = 0 if subj < 0 else subj
        return subj



class Simulation:
    def __init__(self, guac_df, num_townspeople, st_dev, limit=20):
        self.guac_df = guac_df
        self.num_townspeople = num_townspeople
        self.st_dev = st_dev
        self.limit = limit
        self.results_df = None
        self.objective_winner = guac_df[["Objective Ratings"]].idxmax()[0]


    def simulate(self):
        # self.results_df = copy(self.guac_df)
        self.results_df = pd.DataFrame(index=self.guac_df.index)
        for ii in range(self.num_townspeople):
            person = Townsperson(name=ii, st_dev=self.st_dev)
            self.results_df[person.name] = person.taste_and_vote(self.guac_df)

        sum_of_votes = self.results_df.sum(axis=1)
        avg_of_votes = self.results_df.mean(axis=1)
        med_of_votes = self.results_df.median(axis=1)
        self.results_df["Sum"] = sum_of_votes
        self.results_df["Avg"] = avg_of_votes
        self.results_df["Med"] = med_of_votes
