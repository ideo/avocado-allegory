import pandas as pd
import numpy as np
from .townspeople import Townsperson

#TODO, allow people to sort guacs? or give point percentages?
class Simulation_unknown_best:
    def __init__(
            self, num_townspeople, 
            num_guacs_total, 
            num_guacs_per_person, 
            sensitive_tastebuds = False
            ):
        self.num_townspeople = num_townspeople
        self.num_guacs_per_person = num_guacs_per_person
        self.guac_names = [str(i) for i in range(num_guacs_total)]
        self.results_df = pd.DataFrame(self.guac_names, columns = ['guac'])
        self.winner = None
        self.scores_cols = []
        self.fra_joe = 'fra'
        self.sensitive_tastebuds = sensitive_tastebuds

    def simulate(self, votes_from_testing_all = pd.DataFrame()):
        """This function simulate scores.
        The math behind the ballot matrices is explained here:https://en.wikipedia.org/wiki/Condorcet_method#:~:text=The%20number%20of%20votes%20for,A%20beats%20every%20other%20candidate.

        """
        all_ballots_matrix = []
        person_number = 0
        
        for _ in range(self.num_townspeople):            
            person = Townsperson(person_number, self.sensitive_tastebuds)
            
            #simulate score for each guac and determine ballot matrix
            ballot_matrix, ballot_dict = person.fill_in_ballot(self.num_guacs_per_person, 
                                                                self.guac_names, 
                                                                person_number, 
                                                                votes_from_testing_all)

            #collect all ballots matrices to then sum them to find the winner
            all_ballots_matrix.append(ballot_matrix)

            #collect all scores in a dataframe to combine them later
            self.results_df[f"score_person_{person_number}"] = self.results_df['guac'].apply(lambda x: ballot_dict.get(x, np.nan))

            person_number += 1

        ballots_matrix_sum = all_ballots_matrix[0]
        for m in all_ballots_matrix[1:]:
            ballots_matrix_sum += m
        
        #compute winner
        self.winner = self.find_winner(ballots_matrix_sum)

        #compute score for each guac
        self.results_df.set_index('guac', inplace = True)
        self.scores_cols = self.results_df.columns        
        self.compute_scores()
        self.results_df['guac'] = self.results_df.index
        
    def compute_scores(self):
        self.results_df['Sum'] = self.results_df[self.scores_cols].sum(axis=1)
        self.results_df['Avg'] = self.results_df[self.scores_cols].mean(axis=1)
        self.results_df['Med'] = self.results_df[self.scores_cols].median(axis=1)


    def find_winner(self, ballots_matrix_sum):
        df = pd.DataFrame(ballots_matrix_sum, columns = self.guac_names)
        df['sum'] = df.apply(lambda x: x.sum(),1)
        df['runner'] = self.guac_names
        df.sort_values(['sum'], ascending=False, inplace = True)
        
        return df.iloc[0]['runner']        


