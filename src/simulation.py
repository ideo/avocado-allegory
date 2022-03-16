import pandas as pd
import numpy
from .townspeople import Townsperson

TEST_JENNAS_NUMBERS = False
class Simulation:
    def __init__(
            self, guac_df, num_townspeople, st_dev, fullness_factor = 0.0,
            assigned_guacs=20, perc_fra=0.0, perc_pepe=0.0, perc_carlos=0.0
        ):
        self.guac_df = guac_df
        self.num_townspeople = num_townspeople
        self.st_dev = st_dev
        self.fullness_factor = fullness_factor
        self.assigned_guacs = assigned_guacs
        self.perc_fra = perc_fra
        self.perc_pepe = perc_pepe
        self.perc_carlos = perc_carlos
        self.results_df = None
        # self.method = method
        self.objective_winner = guac_df[["Objective Ratings"]].idxmax()[0]
        self.sum_winner = None
        self.success = False
        # self.method = method.lower()

        if TEST_JENNAS_NUMBERS:
            self.num_townspeople = 7
            self.assigned_guacs = 6
            self.guac_df = pd.DataFrame([0,1,2,3,4,5], columns = ['Entrant'])
            self.guac_df['Objective Ratings'] = 0


    def simulate(self, cazzo=False):

        num_pepes, num_fras, num_carlos, num_reasonable = self.create_personas()
         
        #this is by how much we'll be moving the standard deviation used to sample from the Guac God give scores
        person_types = [num_reasonable, num_pepes, num_fras, num_carlos]
        mean_offsets = [0, 3, -3, 0]
        carlos_cronies = [False, False, False, True]

        #Creating the DF that will store the ballots
        self.results_df = pd.DataFrame(list(self.guac_df.index), columns = ["ID"])

        #creating the matrix sum. We'll increment this in the condorcet object
        ballots_matrix_sum = numpy.zeros([len(self.guac_df),len(self.guac_df)])
        
        #filling in the ballots dataframe,for the various characters
        condorcet_elements = None
        for num_people, offset, carlos_crony in zip(person_types, mean_offsets, carlos_cronies):
            if num_people == 0: continue
            condorcet_elements = self.collect_results(ballots_matrix_sum, num_people, offset, carlos_crony)

        # #FIXME to add what this character does. Will we be basically use the same votes across carlos?
        # if num_carlos > 0:
        #     condorcet_elements = self.collect_results(ballots_matrix_sum, num_carlos)

        #putting the results together
        self.results_df.set_index(["ID"], inplace = True)
        columns_to_consider = self.results_df.columns
        self.results_df["sum"] = self.results_df[columns_to_consider].sum(axis=1)
        self.results_df["Mean"] = self.results_df[columns_to_consider].mean(axis=1)
        self.sum_winner = self.results_df[["sum"]].idxmax()[0]
        self.condorcet_winner = condorcet_elements.declare_winner(self.results_df)

        if self.assigned_guacs == len(self.guac_df):
            self.success = self.sum_winner == self.objective_winner
        else:
            self.success = self.condorcet_winner == self.objective_winner
        
        # if num_carlos > 0:
        #     import pdb;pdb.set_trace()


    def create_personas(self):
        """This function creates the counts for the different personas.

        Returns:
           tuple of integers with the count for each persona
        """

        #introducing characters to the simulation
        #num_pepes tend to score people higher
        num_pepes = round(self.num_townspeople * self.perc_pepe)

        #num_fras tend to score people lower
        num_fras = round(self.num_townspeople * self.perc_fra)

        #num_carlos are colluding to vote Carlos the best
        num_carlos = round(self.num_townspeople * self.perc_carlos)

        #num_reasonable tend to score people fair
        num_reasonable = self.num_townspeople - num_pepes - num_fras - num_carlos
        return num_pepes, num_fras, num_carlos, num_reasonable


    def collect_results(self, ballots_matrix_sum, num_people, mean_offset=0, carlos_crony=False):
        """This function collects the results of a simulation on a set of people

        Args:
            num_people (int): number of town people
            mean_offset (float): offset to apply to the objective score (we use this to account for personas)
            ballots_matrix_sum (numpy matrix): matrix needed for the calculation of the condorcet winner

        Returns:
            condorcet counting object containing the details of the condorcet method to compute the winner
        """
        #for each characted, loop through the counts for that
        last_person=False
        condorcet_elements = None
        for np in range(num_people):
            if np == num_people-1:
                last_person=True

            person = Townsperson(
                person_number=np, 
                st_dev=self.st_dev, 
                assigned_guacs=self.assigned_guacs, 
                mean_offset=mean_offset, 
                test_jennas_numbers=TEST_JENNAS_NUMBERS,
                carlos_crony=carlos_crony
                )

            #creating the elements to compute the condorcet winner
            condorcet_elements = person.taste_and_vote(self.guac_df, ballots_matrix_sum, last_person)

            #add the results to the results dataframe with a new column name
            self.results_df[f"Score Person {person.number}"] = self.guac_df["Entrant"].apply(lambda x: condorcet_elements.ballot_dict.get(x, None))

        #returning the last condorcet element calculated. 
        return condorcet_elements
        