import pandas as pd
import numpy as np
import re

class CallsignMatcher():
    def __init__(self, file_loc):
        # Loading Data from Log File
        self.df = pd.read_csv(file_loc)

    def find_match(self, callsign, threshold=None):
        # calculate levenshtein distance for string on all of the available callsigns
        l_distances = self.df['callsign'].apply(lambda x: self._iterative_levenshtein(callsign, x))
        if type(np.where(l_distances.values == l_distances.min().values)) != int:
            return self.df.iloc[l_distances.idxmin()]
        return 'NA'


    def _iterative_levenshtein(self, s, t):
        """ 
            iterative_levenshtein(s, t) -> ldist
            ldist is the Levenshtein distance between the strings 
            s and t.
            For all i and j, dist[i,j] will contain the Levenshtein 
            distance between the first i characters of s and the 
            first j characters of t
        """
        if not type(t) == str or t == "NA":
            return 99999

        rows = len(s)+1
        cols = len(t)+1
        dist = [[0 for x in range(cols)] for x in range(rows)]

        # source prefixes can be transformed into empty strings 
        # by deletions:
        for i in range(1, rows):
            dist[i][0] = i

        # target prefixes can be created from an empty source string
        # by inserting the characters
        for i in range(1, cols):
            dist[0][i] = i
            
        for col in range(1, cols):
            for row in range(1, rows):
                if s[row-1] == t[col-1]:
                    cost = 0
                else:
                    cost = 1
                dist[row][col] = min(dist[row-1][col] + 1,      # deletion
                                    dist[row][col-1] + 1,      # insertion
                                    dist[row-1][col-1] + cost) # substitution
        return dist[row][col]