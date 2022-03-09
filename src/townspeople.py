import numpy as np
import pandas as pd
import random
from .condorcetcounting import Condorcetcounting


# Base Class
class Townsperson:
    def __init__(self, person_number, st_dev=1, assigned_guacs=20, mean_offset=0, 
                min_allowed_vote = 1, max_allowed_vote = 10):
        self.number = person_number
        self.st_dev = st_dev
        self.assigned_guacs = assigned_guacs
        self.mean_offset=0
        self.min_allowed_vote = min_allowed_vote
        self.max_allowed_vote = max_allowed_vote

    def taste_and_vote(self, guac_df, ballots_matrix_sum):
        """This function takes a subset of the guac god data frame and it assigns subjective ratings to each
        guac. The subjective ratings are sampled by a normal distribution centered at the guac god given score (objective ratings) and with a user defined
        standard deviation.

        Args:
            guac_df (dataframe): dataframe with objective ratings

        Returns:
            dataframe with subjective ratings
        """

        # Choose guacs 
        sample_guac_df = guac_df.sample(n=self.assigned_guacs, replace=False)
        sample_guac_df['Subjective Ratings'] = sample_guac_df["Objective Ratings"].apply(lambda x: self.taste(x))
        condorcet_elements = Condorcetcounting(guac_df, sample_guac_df, ballots_matrix_sum)
        return condorcet_elements

    def taste(self, obj_rating):
        """This function creates the subjective rating by sampling from a normal distribution
        Args:
            obj_rating (float): objective rating

        Returns:
            float: subjective rating
        """
        subj = np.random.normal(obj_rating, self.st_dev)
        subj = 10 if subj > 10 else subj
        subj = 0 if subj < 0 else subj
        return subj

