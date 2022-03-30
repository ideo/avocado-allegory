from re import sub
import numpy as np
import pandas as pd
from .condorcetcounting import Condorcetcounting


# Base Class
class Townsperson:
    def __init__(self, st_dev = 1, assigned_guacs = 20, fullness_factor = 0.0, 
                person_number = None, 
                min_allowed_vote = 1, max_allowed_vote = 10, 
                mean_offset = 0, carlos_crony = False):
        self.number = person_number
        self.st_dev = st_dev
        self.fullness_factor = fullness_factor
        self.assigned_guacs = int(assigned_guacs)
        self.mean_offset = mean_offset
        self.min_allowed_vote = min_allowed_vote
        self.max_allowed_vote = max_allowed_vote
        self.carlos_crony = carlos_crony
        self.carlos_index = None
        self.voted_for_our_boy = False
        self.ballot = None
        # self.test_jennas_numbers=test_jennas_numbers


    def taste_and_vote(self, guac_df):
        """This function takes a subset of the guac god data frame and it 
        assigns subjective ratings to each guac. The subjective ratings are 
        sampled by a normal distribution centered at the guac god given score 
        (objective ratings) and with a user defined standard deviation.

        Args:
            guac_df (datafrane): dataframe with objective scores
        Returns:
            This agent's ballot of subjective rankings
        """
        self.ballot = guac_df.sample(n=self.assigned_guacs, replace=False)
        self.ballot['Subjective Ratings'] = self.ballot[["Objective Ratings"]].apply(lambda x: self.taste(x, self.ballot.index), axis=1)
        return self.ballot


    def taste(self, row_data, df_index):
        """This function uses the objective rating score to compute the subjective one, based on some assumptions

        Args:
            row_data (list): objective rating
            df_index (Int64Index): index containing all guac IDs

        Returns:
            float: subjective rating
        """
        obj_rating = row_data[0]
        taste_order = df_index.get_loc(row_data.name)

        if self.carlos_crony and row_data.name==self.carlos_index:
            # We votin' for our boy!
            self.voted_for_our_boy = True
            return self.max_allowed_vote

        else:
            # Here the fullness_offset is modeled as a straight line going from -1 to +1. 
            # The FF is just a multiplicative factor that moves the offset and increases/decreases the slope.
            # When fullness_factor = 1, you recover the equation of a straight line. 
            # When fullness_factor = 0, the effect is off        
            slope = -self.fullness_factor / (len(df_index)/2)
            fullness_offset =  slope * taste_order + self.fullness_factor

            obj_rating = row_data[0]
            mu = obj_rating + self.mean_offset + fullness_offset
            subj = np.random.normal(mu, self.st_dev)

            #allowing townspeople to use decimal points, but not more precision than that...
            subj = round(subj, 1)
            subj = self.max_allowed_vote if subj > self.max_allowed_vote else subj
            subj = self.min_allowed_vote if subj < self.min_allowed_vote else subj
            return subj

