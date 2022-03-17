import pandas as pd
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
         
        #Creating the DF that will store the ballots
        self.results_df = pd.DataFrame(list(self.guac_df.index), columns = ["ID"])

        #creating the list that will contain each matrix ballot (needed for condorcet)
        ballots_matrix_list = []
        
        #filling in the ballots dataframe,for the various characters
        condorcet_elements = None

        #this is by how much we'll be moving the standard deviation used to sample from the Guac God give scores
        person_types = [num_reasonable, num_pepes, num_fras]
        mean_offsets = [0, 3, -3]
        carlos_cronies = [False, False, False, True]

        for num_people_type, offset_type, carlos_crony in zip(person_types, mean_offsets, carlos_cronies):
            if num_people_type == 0: continue
            condorcet_elements, ballots_matrix_list = self.collect_results(ballots_matrix_list, num_people_type, offset_type, carlos_crony)
                    
        #putting the results together
        self.results_df.set_index(["ID"], inplace = True)
        columns_to_consider = self.results_df.columns
        self.results_df["sum"] = self.results_df[columns_to_consider].sum(axis=1)
        self.results_df["Mean"] = self.results_df[columns_to_consider].mean(axis=1)
        
        self.sum_winner = self.get_sum_winner()
        
        self.condorcet_winner = condorcet_elements.declare_winner(self.results_df, ballots_matrix_list)

        self.sum_success = self.sum_winner == self.objective_winner
        self.condo_success = self.condorcet_winner == self.objective_winner
        #FIXME reminder you have this one in here. I assume it will become an if/else at some point. 
        self.success = self.sum_success

        
    def get_sum_winner(self):
        """This function determines the winner considering the sum.

        Returns:
            integer: guac ID of winner
        """
        sorted_scores = self.results_df.sort_values(by='sum', ascending=False)
        sorted_scores['Entrant'] = sorted_scores.index
        
        top1_score = sorted_scores.iloc[0]['sum']
        top1_winner = sorted_scores.iloc[0]['Entrant']

        top2_score = sorted_scores.iloc[1]['sum']
        
        #Just to be aware of the possibility of getting the same sum
        #FIXME
        if top1_score == top2_score:
            print("\n\n\nMULTIPLE WINNERS! PICKING ONE AT RANDOM...\n\n\n")
         
        return top1_winner

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

    def collect_results(self, ballots_matrix_list, num_people, mean_offset = 0, carlos_crony=False):
        """This function collects the results of a simulation on a set of people

        Args:
            num_people (int): number of town people
            mean_offset (float): offset to apply to the objective score (we use this to account for personas)
            ballots_matrix_sum (numpy matrix): matrix needed for the calculation of the condorcet winner

        Returns:
            condorcet counting object containing the details of the condorcet method to compute the winner
        """
        condorcet_elements = None

        for np in range(num_people):
            person = Townsperson(
                person_number=np, 
                st_dev=self.st_dev, 
                assigned_guacs=self.assigned_guacs, 
                mean_offset=mean_offset, 
                test_jennas_numbers=TEST_JENNAS_NUMBERS
                )

            #creating the elements to compute the condorcet winner
            condorcet_elements = person.taste_and_vote(self.guac_df)

            #collect ballox matrices
            ballots_matrix_list.append(condorcet_elements.ballot_matrix)

            #add the results to the results dataframe with a new column name
            self.results_df[f"Score Person {person.number}"] = self.guac_df["ID"].apply(lambda x: condorcet_elements.ballot_dict.get(x, None))

            if len(self.results_df[self.results_df[f"Score Person {person.number}"].isnull()]) == len(self.results_df):
                sys.exit(f"No scores recorder from person.number {person.number}. Something is wrong...") 
            
        #returning the last condorcet element calculated. 
        return condorcet_elements, ballots_matrix_list
        