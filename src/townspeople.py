import numpy as np
import pandas as pd
import random
from .condorcetcounting import Condorcetcounting


# Base Class
class Townsperson:
    def __init__(self, person_number, fullness_factor = 0.0, st_dev=1, assigned_guacs=20, mean_offset=0, 
                min_allowed_vote = 1, max_allowed_vote = 10, carlos_crony=False,
                test_jennas_numbers = False):
        self.number = person_number
        self.st_dev = st_dev
        self.fullness_factor = fullness_factor
        self.assigned_guacs = int(assigned_guacs)
        self.mean_offset=0
        self.min_allowed_vote = min_allowed_vote
        self.max_allowed_vote = max_allowed_vote
        self.carlos_crony = carlos_crony
        self.carlos_index = None
        self.test_jennas_numbers=test_jennas_numbers


    def taste_and_vote(self, guac_df):
        """This function takes a subset of the guac god data frame and it assigns subjective ratings to each
        guac. The subjective ratings are sampled by a normal distribution centered at the guac god given score (objective ratings) and with a user defined
        standard deviation.

        Args:
            guac_df (datafrane): dataframe with objective scores
        Returns:
            A Condorcetcounting object
        """
        if self.test_jennas_numbers == False:
            self.carlos_index = guac_df[guac_df["Entrant"] == "Cliquey Carlos"].index[0]

        sample_guac_df = guac_df.sample(n=self.assigned_guacs, replace=False)
        sample_guac_df['Subjective Ratings'] = sample_guac_df[["Objective Ratings"]].apply(lambda x: self.taste(x, sample_guac_df.index), axis=1)

        if self.test_jennas_numbers:
            jennas_data = {}
            jennas_data[0] = [(2,2), (4,3), (5,1)]
            jennas_data[1] = [(2,2), (4,5), (5,10)]
            jennas_data[2] = [(2,7),(3,2), (4,3.3), (5,4)]
            jennas_data[3] = [(0,9), (1,9.5), (2,10), (3,3)]
            jennas_data[4] = [(0,9), (1,9.5), (3,0), (5,10)]
            jennas_data[5] = [(1,5), (3,4), (4,8)]
            jennas_data[6] = [(0,6),(1,8),(3,10),(4,7)]        
            sample_guac_df = pd.DataFrame(jennas_data[self.number], columns = ["ID", 'Subjective Ratings'])

        condorcet_elements = Condorcetcounting(guac_df, sample_guac_df)
        return condorcet_elements


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
            # We voting for our boy!
            return 10

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
            subj = round(subj,1)
            subj = 10 if subj > 10 else subj
            subj = 0 if subj < 0 else subj
            return subj

