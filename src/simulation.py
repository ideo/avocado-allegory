import sys
import random
from collections import Counter

import numpy as np
import pandas as pd

from .townspeople import Townsperson
from .condorcet_counting import CondorcetCounting
from .ranked_choice_voting import RankChoiceVoting


class Simulation:
    def __init__(
            self, guac_df, num_townspeople=200, st_dev=1.0, fullness_factor = 0.0,
            assigned_guacs=20, perc_fra=0.0, perc_pepe=0.0, perc_carlos=0.0,
            method="sum", rank_limit=None, seed=None
        ):
        self.guac_df = guac_df
        self.num_townspeople = num_townspeople
        self.townspeople = []
        self.st_dev = st_dev
        self.fullness_factor = fullness_factor
        self.assigned_guacs = assigned_guacs
        self.perc_fra = perc_fra
        self.perc_pepe = perc_pepe
        self.perc_carlos = perc_carlos
        self.method = method.lower()
        self.rank_limit=rank_limit if self.method == "rcv" else None
        if seed:
            random.seed(seed)

        # Initalizing
        self.results_df = None
        self.objective_winner = self.guac_df["Objective Ratings"].idxmax()
        self.success = False
        self.rankings = None


    @property
    def params(self):
        param_dict = {
            "num_townspeople":  self.num_townspeople,
            "assigned_guacs":   self.assigned_guacs,
            "st_dev":           self.st_dev,
            "fullness_factor":  self.fullness_factor,
            "perc_fra":         self.perc_fra,
            "perc_pepe":        self.perc_pepe,
            "perc_carlos":      self.perc_carlos,
            "method":           self.method,
            "rank_limit":       self.rank_limit,
            # "num_entrants":     self.guac_df.shape[0],
            # "scenario":       scenario,
        }
        return param_dict


    def simulate(self):
        """TODO: For unittests, we can update this to have inputs and outputs"""
        self.create_agents()
        self.results_df = self.taste_and_vote()
        self.winner = self.tally_votes(self.results_df)
        self.record_outcome()      
        

    def create_agents(self):
        """Create the agents to be used in the simulation

        Returns: None
        """
        #Pepes tend to score people higher
        if self.perc_pepe > 0:
            num_pepes = self.num_townspeople * self.perc_pepe
            num_pepes = int(round(num_pepes))
            for _ in range(num_pepes):
                self.add_agent(mean_offset=3, carlos_crony=False)

        #Fras tend to score people lower
        if self.perc_fra > 0:
            num_fras = self.num_townspeople * self.perc_fra
            num_fras = int(round(num_fras))
            for _ in range(num_fras):
                self.add_agent(mean_offset=-3, carlos_crony=False)

        #Carlos's Cronies are colluding to vote Carlos the best
        if self.perc_carlos > 0:
            num_carlos = self.num_townspeople * self.perc_carlos
            num_carlos = int(round(num_carlos))
            for _ in range(num_carlos):
                self.add_agent(mean_offset=0, carlos_crony=True)
        
        #Reasonable townspeopole tend to score people fairly
        num_reasonable = self.num_townspeople - len(self.townspeople)
        for _ in range(num_reasonable):
                self.add_agent()

        for ii, person in enumerate(self.townspeople):
            person.number = ii


    def add_agent(self, mean_offset=0, carlos_crony=False):
        agent = Townsperson(
            st_dev=self.st_dev, 
            assigned_guacs=self.assigned_guacs, 
            mean_offset=mean_offset, 
            carlos_crony=carlos_crony,
            )
        self.townspeople.append(agent)


    def taste_and_vote(self):
        """Tabulate each voter's ballot into one dataframe"""
        df = pd.DataFrame(list(self.guac_df.index), columns = ["ID"])
        for person in self.townspeople:
            ballot = person.taste_and_vote(self.guac_df)
            df[f"Scores {person.number}"] = ballot["Subjective Ratings"]
        return df


    def tally_votes(self, results_df):
        if self.method == "sum":
            winner = self.tally_by_summing()

        elif self.method == "condorcet":
            winner = self.tally_by_condorcet_method()

        elif self.method == "rcv":
            winner = self.tally_by_ranked_choice(N=self.rank_limit)

        elif self.method == "fptp":
            winner = self.tally_by_first_past_the_post(results_df)

        return winner


    def record_outcome(self):
        """This is here in case we need to expand it"""
        # TODO: we need consistency in how we save the winner, name or ID
        if isinstance(self.winner, str):
            # winner is a name, convert to ID
            ind = self.guac_df[self.guac_df["Entrant"] == self.winner].index[0]
            self.winner = ind

        self.success = self.winner == self.objective_winner

        
    def tally_by_summing(self):
        """This function determines the winner considering the sum.

        Returns:
            integer: guac ID of winner
        """
        #putting the results together
        self.results_df.set_index(["ID"], inplace = True)
        self.results_df["sum"] = self.results_df.sum(axis=1)
        
        #sort the scores to have the sum at the top
        sorted_scores = self.results_df.sort_values(by="sum", ascending=False)
        sorted_scores['ID'] = sorted_scores.index

        #extract highest sum        
        winning_sum = sorted_scores.iloc[0]["sum"]

        #create a dictionary of sums - winners to catch multiple winners
        sum_winners_dict = {}
        for s, w in zip(sorted_scores["sum"].tolist(), sorted_scores['ID'].tolist()):
            if s in sum_winners_dict.keys():
                sum_winners_dict[s].append(w)
            else:
                sum_winners_dict[s] = [w]

        self.sum_winners = sum_winners_dict[winning_sum]
        self.sum_winner = self.sum_winners[0]
        # self.sum_success = self.sum_winner == self.objective_winner

        if len(self.sum_winners) > 1:
            print("\n\n\nMultiple sum winners, picking one at random...\n\n\n")

        return self.sum_winner


    def tally_by_condorcet_method(self):
        #finding the mean
        columns_to_consider = self.results_df.columns
        # columns_to_consider.remove("sum")
        self.results_df["Mean"] = self.results_df[columns_to_consider].mean(axis=1)

        #creating the list that will contain each matrix ballot (needed for condorcet)
        # ballots_matrix_list = []
        
        #filling in the ballots dataframe, for the various characters
        # condorcet_elements = None
        condorcet_elements, ballots_matrix_list = self.condorcet_results()
        self.condorcet_winner = condorcet_elements.declare_winner(self.results_df, ballots_matrix_list)
        self.condorcet_winners = condorcet_elements.winners
        # self.condo_success = self.condorcet_winner == self.objective_winner
        return self.condorcet_winner


    def condorcet_results(self, ballots_matrix_list=[]):
        """This function collects the results of a simulation on a set of people

        Args:
            num_people (int): number of town people
            mean_offset (float): offset to apply to the objective score (we use this to account for personas)
            ballots_matrix_sum (numpy matrix): matrix needed for the calculation of the condorcet winner

        Returns:
            condorcet counting object containing the details of the condorcet method to compute the winner
        """
        condorcet_elements = None

        for person in self.townspeople:

            #creating the elements to compute the condorcet winner
            condorcet_elements = CondorcetCounting(self.guac_df, person.ballot)
            # condorcet_elements = person.taste_and_vote(self.guac_df)

            #collect ballox matrices
            ballots_matrix_list.append(condorcet_elements.ballot_matrix)

            #add the results to the results dataframe with a new column name
            # self.results_df[f"Scores {person.number}"] = self.guac_df["ID"].apply(lambda x: condorcet_elements.ballot_dict.get(x, None))

            if len(self.results_df[self.results_df[f"Scores {person.number}"].isnull()]) == len(self.results_df):
                sys.exit(f"No scores recorder from person.number {person.number}. Something is wrong...") 
            
        #returning the last condorcet element calculated. 
        return condorcet_elements, ballots_matrix_list


    def tally_by_ranked_choice(self, N=None):
        """TODO: Incorporate N"""

        # I want to display their names not their IDs
        self.results_df["Entrant"] = self.guac_df["Entrant"]
        self.results_df.set_index("Entrant", inplace=True)
        self.results_df.drop(columns=["ID"], inplace=True)

        rcv = RankChoiceVoting(N)
        ranks = rcv.convert_score_ballots_to_implicit_ranks(self.results_df)
        self.rankings = rcv.tally_results(ranks)
        self.rcv = rcv
        return self.rankings[0][0]


    def tally_by_first_past_the_post(self, results_df):
        """
        Interpret each voter's top score as their one favorite choice. Tally
        all these single choices with first-past-the-post.

        If there is a tie, it is broken randomly simply by calling .idxmax()
        """
        results_df.drop(columns=["ID"], inplace=True)
        names = self.guac_df["Entrant"]
        votes = []

        choose_fav = lambda ballot: votes.append(names.iloc[ballot.idxmax()])
        results_df.apply(choose_fav, axis=0)

        tallies = [(name, count) for name, count in Counter(votes).items()]
        self.rankings = sorted(tallies, key=lambda x: x[1], reverse=True)
        return self.rankings[0][0]