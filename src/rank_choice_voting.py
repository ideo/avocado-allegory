import numpy as np
import pandas as pd


class RankChoiceVoting:
    def __init__(self):
        self.rankings = []


    def convert_score_ballots_to_implicit_ranks(self, ballot_df, max_score=10):
        """
        Given a dataframe of ballots from score voting, where each vote is a 
        score from min_vote to max_vote, return a dataframe of ranks, where the 
        max_vote is ranked 1, second highest is ranked 2, and so on. When two 
        scores are equal, the tie is broken dumbly by np.argmax(), simply
        choosing the entrant that appears first. 

        Input:
            ballot_df:
                Expects Entrant IDs as the index. The only columns should be
                ballots. It also assumes max_score is higher than min_score, as
                in 'rank these options from 1 to 10, with 10 for the best'.

        Returns:
            Dataframe of ranked choice ballots
        """
        columns = ballot_df.columns.tolist()
        reverse_scores = pd.DataFrame(index=ballot_df.index)
        ranked_df = pd.DataFrame(index=ballot_df.index)

        # We get ranks by sorting. But it sorts smallest to greatest.
        # So we need to flip the scores.
        for col in columns:
            reverse_scores[col] = ballot_df[col].apply(
                lambda score: max_score-score
            )

        # Turn scores into ranks by chaining argsort
        # Add 1 so your first choice is not your 0th choice
        for ii, col in enumerate(columns):
            ranked_df[f"Ranks {ii}"] = reverse_scores[[col]].apply(
                lambda scores: np.argsort(scores.values.argsort()) + 1
            )

        return ranked_df


    def tally_results(self, ranks):
        """
        TODO:
            - tally all ranks
            - tally top N ranks
            - docstring
        """
        counts = ranks.apply(lambda s: s.value_counts(), axis=1)
        num_voters = ranks.shape[1]
        num_first_place_votes = counts[1].max()

        # if counts.shape[0] == 20:
        #     print(counts)
 
        # Majority Win
        if num_first_place_votes > num_voters/2:
            # print("\nWin by majority")
            winner_id = counts[1].argmax()
            winner_name = counts.index[winner_id]
            winning_votes = counts.iloc[winner_id, 1]
            
            self.rankings.insert(0, (winner_name, int(winning_votes)))
            return self.rankings

        # Only two contestants left
        elif counts.shape[0] == 2:
            # print("\nWin by whittling down")
            second_place_ind = counts[1].argmin()
            second_place_name = counts.index[second_place_ind]
            second_place_votes = counts.iloc[second_place_ind, 1]
            self.rankings.insert(0, (second_place_name, int(second_place_votes)))

            first_place_ind = counts[1].argmax()
            first_place_name = counts.index[first_place_ind]
            first_place_votes = counts.iloc[first_place_ind, 1]
            self.rankings.insert(0, (first_place_name, int(first_place_votes)))
            return self.rankings

        # No majority win. Remove the person with the least 1st place ranks
        # TODO: This ignores people with no first place votes. They should be 
        # dropped first.
        else:
            loser_indices = np.where(counts[1] == counts[1].min())[0]
            loser_names = counts.index[loser_indices]

            for ind in loser_indices:
                name = counts.index[ind]
                vote_count = counts.iloc[ind, 1]
                try:
                    vote_count = int(vote_count)
                except ValueError:
                    vote_count = 0
                self.rankings.insert(0, (name, int(vote_count)))

            # Find ballots that had this guac as their #1
            ballot_mask = (ranks.loc[loser_names] == 1).any(axis=0)
            ballot_names = ranks.columns[ballot_mask.values]

            new_ranks = ranks.drop(index=loser_names)
            for col in ballot_names:
                new_ranks[col] = new_ranks[col].apply(lambda r: r-1)

            return self.tally_results(new_ranks)




