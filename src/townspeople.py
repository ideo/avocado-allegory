import numpy as np
import pandas as pd


# Base Class
class Townsperson:
    def __init__(self, name, st_dev=1, limit=20, mean_offset=0):
        self.name = name
        self.st_dev = st_dev
        self.limit = limit
        self.mean_offset=0

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


    def taste(self, obj_rating):
        mu, sigma = obj_rating+self.mean_offset, self.st_dev
        subj = np.random.normal(loc=mu, scale=sigma)
        subj = round(subj)
        subj = 10 if subj > 10 else subj
        subj = 0 if subj < 0 else subj
        return subj



# # Inherited Classes
# class UnreasonableTownsperson(Townsperson):
#     def __init__(self, offset, *args, **kwargs):
#         super(Townsperson, self).__init__(*args, **kwargs)
#         self.st_dev += offset



