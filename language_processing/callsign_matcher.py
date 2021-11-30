import pandas as pd
import re

class CallsignMatcher():
    def __init__(self, file_loc):
        # Loading Data from Log File
        self.df = pd.read_csv(file_loc)

    def get_transcriptions(self, length=None):
        if length != None:
            return self.df[self.df['Length'] > length]
        return self.df

    def plot_length_distribution(self):
        self.df.hist(column='Length', bins=50,figsize=(12,4))

    # TODO: adjust for edge cases (eg. readbacks where N number follows speed, adding alt) 
    def _clean_numbers(self, command):
        # Use regex to remove spaces between numbers
        while (command != re.sub(r'\d+\s+\d+', self._group_spaced_digits, command)):
            command = re.sub(r'\d+\s+\d+', self._group_spaced_digits, command)
        return command

    def _group_spaced_digits(self, match):
        if len(match.group()) < 4: # NOTE: this only really appiles to approach.
                                   # The logic is that prevents unnecessary joining
            return match.group(0).replace(' ', '')