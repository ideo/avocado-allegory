import numpy as np
import pandas as pd
import random


# Base Class
class Townsperson:
    def __init__(self, name, has_different_ingredients = False, st_dev=1, num_guac_per_person=20, mean_offset=0, 
                min_allowed_vote = 1, max_allowed_vote = 10):
        self.name = name
        self.person_number = name
        self.st_dev = st_dev
        self.num_guac_per_person = num_guac_per_person
        self.mean_offset=0
        self.min_allowed_vote = min_allowed_vote
        self.max_allowed_vote = max_allowed_vote
        self.cazzo = False
        self.has_different_ingredients = has_different_ingredients

    def taste_and_vote(self, guac_df):
        """
        Randomly select guacs from the dataframe to taste.
        Taste and generate 'subjective' rating.
        """
        
        # Choose guacs 
        sample_guac_df = guac_df.sample(n=self.num_guac_per_person, replace=False)
        sample_guac_df['Subjective Ratings'] = sample_guac_df["Objective Ratings"].apply(lambda x: self.taste(x))                
        votes_cast = pd.DataFrame(index=guac_df.index)
        votes_cast = votes_cast.join(sample_guac_df[['Subjective Ratings']])
        # import pdb;pdb.set_trace()                           
        
        # votes_cast

        # # Choose guacs        
        # guacs_to_try = np.random.choice(guac_df.index.tolist(), 
        #     size=self.num_guac_per_person, 
        #     replace=False)

        # # Taste
        # votes = {}
        # for guac_id in guacs_to_try:
        #     obj_score = guac_df["Objective Ratings"].iloc[guac_id]
        #     sbj_score = self.taste(obj_score)
        #     votes[guac_id] = sbj_score

        # votes_cast = pd.DataFrame(index=guac_df.index)
        # votes_cast["Vote"] = pd.Series(votes)

        # import pdb;pdb.set_trace()

        return votes_cast


    def taste(self, obj_rating):
        mu, sigma = obj_rating+self.mean_offset, self.st_dev
        subj = np.random.normal(loc=mu, scale=sigma)
        subj = round(subj)
        subj = 10 if subj > 10 else subj
        subj = 0 if subj < 0 else subj
        return subj

    def fill_in_ballot(self, 
                        num_guacs_per_person, 
                        guac_names, 
                        person_number,
                        votes_from_testing_all = pd.DataFrame()):
        """This function compute the ballot and ballot matrix or each voter.
        The ballot matrix is used to compute the winner

        Args:
            num_guacs_per_person (int): number of guacs each person can taste
            guac_names (str): name of the guac
            seed (int): random seed currently assigned to the person ID
            votes_from_testing_all (dataframe, optional): votes computed when everyone tried all guacs. We sample from these when everyone tries only a few. Defaults to pd.DataFrame().

        Returns:
            ballot matrix and ballot dictionary containins the mapping guac - score
        """
       # If no previouly calculated scores are given, we let people vote on all
        if len(votes_from_testing_all) == 0:
            #each person is a seet
            random.seed(person_number)

            # Create a list of uniformly spaced votes from min to max.
            # This assumes all guacs a similar
            possible_votes = np.linspace(self.min_allowed_vote,self.max_allowed_vote,num_guacs_per_person).tolist()
            
            #create the ballot
            ballot  = random.sample(possible_votes, num_guacs_per_person)            

            #create the ballot dictionary, storing the vote for each guac
            ballot_dict = dict(zip(guac_names, ballot)) 
            
            #if some guacs have better ingredients that others, adjust the scores for those
            if self.has_different_ingredients:        
                ballot_dict = self.adjust_for_different_ingredients(ballot_dict, num_guacs_per_person)

            #create the ballot matrix (used to compute winner)
            this_ballot_matrix = self.create_ballot_matrix(ballot_dict, guac_names)

        #If each person is given a fixed number of guacs, 
        #we sample from the scores previously calculated
        else:
            sampled_votes = votes_from_testing_all.sample(n=num_guacs_per_person, replace=False).copy()
            ballot_dict = dict(zip(sampled_votes['guac'].tolist(), 
                                   sampled_votes[f"score_person_{self.person_number}"].tolist()))
            self.cazzo = True                                   
            this_ballot_matrix = self.create_ballot_matrix(ballot_dict, guac_names)

             
        return this_ballot_matrix, ballot_dict


    def create_ballot_matrix(self, ballot_dict, guac_names):
        """This function converts a ballot containing a score for each guac into
        a matrix of runner vs opponent, following the logic here:
        https://en.wikipedia.org/wiki/Condorcet_method#:~:text=The%20number%20of%20votes%20for,A%20beats%20every%20other%20candidate.        

        Args:
            ballot_dict (dict): guac name-score mapping
            guac_names (list): list of names

        Returns:
            numpy ballot matrix
        """
        # Create the ballot matrix:
        ballot_matrix = []
        for runner in guac_names:            
            ballot_array = []
            for opponent in guac_names:
                ballot_array.append(self.assign_score(runner,opponent, ballot_dict))
            ballot_matrix.append(ballot_array)
    
        ballot_matrix = np.matrix(ballot_matrix)
        return ballot_matrix
    
    @staticmethod
    def assign_score(runner, opponent, ballot_dict):
        """This function convert a ballot into a -1/0/1 score based on whether
        the runner lost/tied/won against the opponent in a pairwise comparison

        see: https://en.wikipedia.org/wiki/Condorcet_method#:~:text=The%20number%20of%20votes%20for,A%20beats%20every%20other%20candidate.
        for more.

        Args:
            runner (float): runner score
            opponent (float): opponent score
            ballot_dict (dict): guac name-score mapping

        Returns:
            int: -1/0/1 score based on whether
        the runner lost/tied/won against the opponent
        """
        
        #if those avocados weren't compared, assign a 0
        if runner not in ballot_dict.keys() or opponent not in ballot_dict.keys(): return 0
        #assign to diagonals 0
        if runner == opponent: return 0
        #if runner wins assign 1
        elif ballot_dict[runner] > ballot_dict[opponent]: return 1
        #if there's a tye assign 0
        elif ballot_dict[runner] == ballot_dict[opponent]: return 0
        #if runner loses assign -1
        else: return -1

    def adjust_for_different_ingredients(self, ballot_dict, num_guacs_per_person):
        """This function tries to account for some guacs being better than others in terms of
        ingredients

        Args:
            ballot_dict (dictionary): guac ID - score mapping

        Returns:
            ballot_dict (dictionary): aupdated guac ID - score mapping accounting for taste
        """
        #Some guacs (9 and 13) are made ONLY with organic ingredients, 
        #mashed by hand every single day and they are legittimately better
        #we create a skewed list of numbers to sample from
        new_min = int(1 + (self.max_allowed_vote - self.min_allowed_vote)/2)
        possible_votes = np.linspace(new_min,self.max_allowed_vote,num_guacs_per_person).tolist()
        
        for i in ['9', '13']:
            ballot_dict[i] = random.sample(possible_votes, 1)
            ballot_dict[i] = ballot_dict[i][0]
        
        #Some other guacs (2, 7, 5) are cheap and contain a bunch
        #of chemicals, rather than organic ingredients
        #we create a skewed list of numbers to sample from
        new_max = int((self.max_allowed_vote - self.min_allowed_vote)/2 - 1)
        possible_votes = np.linspace(self.min_allowed_vote,new_max,num_guacs_per_person).tolist()
        for i in ['2', '7', '5']:
            ballot_dict[i] = random.sample(possible_votes, 1)
            ballot_dict[i] = ballot_dict[i][0]
        
        return ballot_dict

# # Inherited Classes
# class UnreasonableTownsperson(Townsperson):
#     def __init__(self, offset, *args, **kwargs):
#         super(Townsperson, self).__init__(*args, **kwargs)
#         self.st_dev += offset



