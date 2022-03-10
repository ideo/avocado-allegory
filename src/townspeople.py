import numpy as np
import pandas as pd
import random
from .condorcetcounting import Condorcetcounting


# Base Class
class Townsperson:
    def __init__(self, person_number, fullness_factor = 0.0, st_dev=1, assigned_guacs=20, mean_offset=0, 
                min_allowed_vote = 1, max_allowed_vote = 10):
        self.number = person_number
        self.st_dev = st_dev
        self.fullness_factor = fullness_factor
        self.assigned_guacs = int(assigned_guacs)
        self.mean_offset=0
        self.min_allowed_vote = min_allowed_vote
        self.max_allowed_vote = max_allowed_vote


    def taste_and_vote(self, guac_df, ballots_matrix_sum, last_person):
        """This function takes a subset of the guac god data frame and it assigns subjective ratings to each
        guac. The subjective ratings are sampled by a normal distribution centered at the guac god given score (objective ratings) and with a user defined
        standard deviation.
        """
        # Choose guacs 
        sample_guac_df = guac_df.sample(n=self.assigned_guacs, replace=False)
        sample_guac_df['Subjective Ratings'] = sample_guac_df[["Objective Ratings"]].apply(lambda x: self.taste(x, sample_guac_df.index), axis=1)
        condorcet_elements = Condorcetcounting(guac_df, sample_guac_df, ballots_matrix_sum, last_person)
        return condorcet_elements


    def taste(self, row_data, df_index):
        obj_rating = row_data[0]
        taste_order = df_index.get_loc(row_data.name)

        slope = -self.fullness_factor / (len(df_index)/2)
        fullness_offset =  slope * taste_order + self.fullness_factor
        # print(f"taste_order: {taste_order}\t\tfullness_offset: {fullness_offset}")

        obj_rating = row_data[0]
        mu = obj_rating + self.mean_offset + fullness_offset
        subj = np.random.normal(mu, self.st_dev)
        subj = round(subj)
        subj = 10 if subj > 10 else subj
        subj = 0 if subj < 0 else subj
        return subj

