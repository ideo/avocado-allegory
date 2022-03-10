import numpy as np

class Condorcetcounting():
    def __init__(
            self, 
            guac_df, 
            sample_guac_df, 
            sum_ballots_matrix, 
            last_person=False, 
            cazzo=False):
        
        #for debugging
        self.cazzo = cazzo
        self.guac_names = list(guac_df.index)
        self.num_guacs = len(guac_df)
        self.sample_guac_df = sample_guac_df
        
        self.ballot_dict = self.get_ballot_dictionary()        
        self.ballot_matrix = self.create_ballot_matrix()
        
        

        #as ballots are created, we sum the matrices on the fly
        sum_ballots_matrix += self.ballot_matrix

        self.sum_ballots_matrix = sum_ballots_matrix
        

        if last_person:
            self.getSchwartzRelationsMatrix()
        


    def create_ballot_matrix(self):
        """This function converts a ballot containing a score for each guac into
        a matrix of runner (rows) vs opponent (columns), where wins (and only wins) are marked as 1.

        Returns:
            numpy ballot matrix
        """
        
        # Create the ballot matrix, row by row.
        ballot_matrix = []

        #loop on runners
        for runner in self.guac_names:   

            #if this runner wasn't in the ballot, then fill in with 0s and move to the next
            if runner not in self.ballot_dict.keys():
                ballot_matrix.append([0 for i in range(len(self.guac_names))])
                continue

            ballot_array = []
            #loop on opponents
            for opponent in self.guac_names:

                #if this opponent wasn't in the ballot, add a 0 and move to the next
                if opponent not in self.ballot_dict.keys():
                    ballot_array.append(0)
                    continue
                    
                #if runner beats the opponent, record the win
                if self.ballot_dict[runner] > self.ballot_dict[opponent]:
                    ballot_array.append(1)
                else: 
                    ballot_array.append(0)

            #append to then create a ballot matrix
            ballot_matrix.append(ballot_array)
    

        ballot_matrix = np.matrix(ballot_matrix)

        return ballot_matrix


    def get_ballot_dictionary(self):
        """This function extract a dictionary with guac and vote

        Returns:
            guac:vote dictionary
        """
        ballot_dict = dict(zip(self.sample_guac_df['Entrant'], self.sample_guac_df['Subjective Ratings'])) 
        return ballot_dict

    def getSchwartzRelationsMatrix(self):
        """This function creates a matrix of the preferences. True is in positions where a runner is 
        preferred more than the opponent.

        Returns:
            matrix of preferences
        """
        #initialize a matrix with all zeros 
        relationsMatrix = np.zeros([self.num_guacs,self.num_guacs], dtype=np.bool) # Init to False (loss)

        #loop through all guacs and check the runner vs opponent preferences. 
        #when the runner is more preferred than the opponent (by more votes), flip the matrix location to True
        for runner in range(self.num_guacs):
            for opponent in range(self.num_guacs):
                if runner == opponent: break
                if (self.sum_ballots_matrix[runner][opponent] > self.sum_ballots_matrix[opponent][runner]):
                    relationsMatrix[runner][opponent] = True # Victory (no tie)
        
        return relationsMatrix

