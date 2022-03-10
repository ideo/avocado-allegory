import pandas as pd
import numpy
from .townspeople import Townsperson


class Simulation:
    def __init__(
            self, guac_df, num_townspeople, st_dev, fullness_factor = 0.0,
            assigned_guacs=20, perc_fra=0.0, perc_pepe=0.0
        ):
        self.guac_df = guac_df
        self.num_townspeople = num_townspeople
        self.st_dev = st_dev
        self.fullness_factor = fullness_factor
        self.assigned_guacs = assigned_guacs
        self.perc_fra = perc_fra
        self.perc_pepe = perc_pepe
        self.results_df = None
        self.objective_winner = guac_df[["Objective Ratings"]].idxmax()[0]
        self.winner = None
        # self.method = method.lower()


    def simulate(self, cazzo=False):

        #introducing characters to the simulation
        #num_pepes tend to score people lower
        num_pepes = round(self.num_townspeople * self.perc_pepe)

        #num_fras tend to score people higher
        num_fras = round(self.num_townspeople * self.perc_fra)

        #num_reasonable tend to score people fair
        num_reasonable = self.num_townspeople - num_pepes - num_fras


        person_types = [num_reasonable, num_pepes, num_fras]
        #this is by how much we'll be moving the standard deviation used to sample from the Guac God give scores
        mean_offsets = [0, 3, -3]

        
        #Creating the DF that will store the ballots
        self.results_df = pd.DataFrame(list(self.guac_df.index), columns = ['Entrant'])

        #creating the matrix sum. We'll increment this in the condorcet object
        ballots_matrix_sum = numpy.zeros([len(self.guac_df),len(self.guac_df)])

        #filling in the ballots dataframe, looping through the various characters
        for num_people, offset in zip(person_types, mean_offsets):
            last_person=False
            for np in range(num_people):
                if np == num_people-1:last_person=True
                person = Townsperson(person_number=np, st_dev=self.st_dev, assigned_guacs=self.assigned_guacs, mean_offset=offset)
                #creating the elements to compute the condorcet winner
                condorcet_elements = person.taste_and_vote(self.guac_df, ballots_matrix_sum, last_person)
                self.results_df[f"Score Person {person.number}"] = self.results_df['Entrant'].apply(lambda x: condorcet_elements.ballot_dict.get(x, None))


        self.results_df.set_index(['Entrant'], inplace = True)
        self.results_df["sum"] = self.results_df.sum(axis=1)
        self.sum_winner = self.results_df[["sum"]].idxmax()[0]

        
        
