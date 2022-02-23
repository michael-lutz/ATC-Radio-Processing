import pandas as pd
import re

class Preprocessor():
    def __init__(self, file_loc, log=True):
        if log:
            self.read_log(file_loc)
        else:
            self.read_json(file_loc)

        self.df['Length'] = self.df['Transcriptions'].apply(len)
        self.df['Transcriptions'] = self.df['Transcriptions'].apply(self._clean_numbers)

    def read_log(self, file_loc):
        # Loading Data from Log File
        f = open(file_loc)
        string_file = f.read()
        transcriptions = re.findall(r'Transcription: (.*?), cabin', string_file)
        time_stamps = re.findall(r'20(.*?) -', string_file)

        # Creating Pandas Data Frame from Data
        self.df = pd.DataFrame(list(zip(time_stamps, transcriptions)),
                    columns =['Time', 'Transcriptions'])

    def read_json(self, file_loc):
        self.df = pd.read_json(file_loc)
        self.df = self.df[['id', 'endDate', 'utterance']]
        self.df = self.df.rename(columns={'endDate': 'Time', 'utterance': 'Transcriptions'})
        self.df['Time'] = self.df['Time'].apply(lambda x: int(x) + 978307200) # Test to make sure it works

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