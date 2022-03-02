import pandas as pd
import numpy as np
import re

class CallsignMatcher():
    def __init__(self, file_loc, data_source='adsbx'):
        # Loading track data
        self.df = pd.read_csv(file_loc)

        # Cleaning Data
        if data_source == "adsbx":
            self.df['time'] = self.df['time'].apply(lambda x: int(x))
        elif data_source == "opensky":
            self.df['time_position'] = self.df['time_position'].apply(lambda x: int(x))


    # TODO: Find a well-integrated way to make the searches restricted to a moment in time.
    # Eg: search only from t-c to t+c where t is time of utterance and c is a constant
    # This will reduce amount of instances of multiple matches.
    # To implement: take t as an input to find_match()
    # Then add filter when defining callsigns_unique


    def find_match(self, callsign, threshold=None, t=-1, c = 1200, data_source = 'adsbx'):
        # Defining time_var_name
        time_var_name = 'time'
        if data_source == 'opensky': # Handles case when adsbx is not the option
            time_var_name = 'time_position'

        # return NA if given NA
        if callsign == 'NA':
            return 'NA'
        
        # calculate levenshtein distance for string on all of the available callsigns
        if t == -1:
            callsigns_unique = pd.Series(self.df['flight'].unique())
        else:
            callsigns_unique = pd.Series(self.df[(self.df[time_var_name] < t + c) & (self.df[time_var_name] > t - c)]['flight'].unique())
        
        l_distances = callsigns_unique.apply(lambda x: self._iterative_levenshtein(callsign, x)).values

        if threshold and len(l_distances) > 0:
            matches = np.where(l_distances == l_distances.min() and l_distances < threshold)
        elif len(l_distances) > 0:
            matches = np.where(l_distances == l_distances.min())
        else:
            return 'NA'

        print(matches)

        if len(matches[0]) == 1:
            return callsigns_unique[int(matches[0][0])]
        else:
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

        s = s.strip()
        t = t.strip()

        if t == s:
            return 0

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
        try:
            return dist[row][col]
        except:
            return 99999