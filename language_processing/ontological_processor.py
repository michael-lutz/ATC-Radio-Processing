import pandas as pd
import re

class OntologicalProcessor():
    def __init__(self):
        self.known_callsign_prefixes = ['american', 'envoy', 'biztex', 'frontier', 'skywest', 'sioux', 'cessna', 'grumman', 'speedbird']

    def find_alt(self, command): # TODO: use NLTK synonyms instead
        command = str.lower(command)
        command = str.split(command)

        number_loc = [i for (i, x) in enumerate(command) if x.isdigit() and (len(x) > 3) and (int(x)%100 == 0)] # Note: the divisibility by 100 excludes speed (and often callsigns)

        # locate the index of ascend
        key_loc = [i for (i, x) in enumerate(command) if (x == 'up') or ('down' in x) or ('descend' in x) 
                    or ('ascend' in x) or ('climb' in x) or ('altitude' in x) 
                    or ('maintain' in x and 'knots' not in command[i:i+5] and 'speed' not in command[i:i+5])]

        # If there exists no keyword, there exists a number devisible by 100 
        if ((len(key_loc) == 0) and (len(number_loc) > 0)):
            return 'Possibly Missing KW' # NOTE: this can be used to predict speaker role w/ ML
        # If there exists no number and no command (note: doesn't account for edge case of callsign being divisible by 100)
        elif (len(key_loc)==0):
            return 'NA'
        # key_loc must be populated, but unsure about whether number_loc exists / actual altitude exists
        try:
            filtered_numbers = [i for i in number_loc if i > key_loc[-1]]
            return int(command[filtered_numbers[0]])
        # If above fails, must be because altutde does not exist but keyword exists
        except:
            return 'Missing ST' # doesn't account for edge cases
        

    def find_turn(self, command):
        command = str.lower(command)
        command = str.split(command)

        # locate the index of heading change - TODO: implement stuff for like 10 degrees right and left
        key_loc = [i for (i, x) in enumerate(command) if ('heading' in x) or ('degrees' in x) or ('turn' in x) or ('left' in x) or ('right' in x)]

        # If no key locations, return NA
        if (len(key_loc)==0):
            return 'NA'
        
        try:
             # Note: length of 3 is beacuse headings are always 3 digits, but "turn 10 degrees right" is not
            number_loc = [i for (i, x) in enumerate(command) if x.isdigit() and (len(x) == 3)] 
            filtered_numbers = [i for i in number_loc if i > key_loc[0] and i <= key_loc[-1]+2] # makes sure it's directly after the keyword
            return command[filtered_numbers[0]]
        except:
            try:
                # If not 3 digits, must be a turn __ degrees right/left command
                number_loc = [i for (i, x) in enumerate(command) if x.isdigit() and (len(x) == 2)] 
                filtered_numbers = [i for i in number_loc if i < key_loc[-1]] # < becuase "right/left" will register last
                return command[filtered_numbers[-1]]+command[key_loc[-1]] # last element because we're switching the order
            except:
                return 'Missing ST' # doesn't account for edge cases

        # TODO: possibly implement Missing KW (if no keyword is found -> if find way to reliably do so)

    def find_contact(self, command):
        command = str.lower(command)
        return ('contact' in command) or ('tower' in command) or ('radio' in command) or ('.' in command)

    def find_speed(self, command):
        command = str.lower(command)
        return ('speed' in command) or ('reduce' in command) or ('slow' in command) or ('knots' in command)

    def find_clearance(self, command):
        command = str.lower(command)
        return ('clear' in command)

    def find_callsign(self, command):
        command = str.lower(command)
        prefix = set(str.split(command, " ")).intersection(set(self.known_callsign_prefixes))
        if prefix:
            prefix = prefix.pop()
            command_list = str.split(command)
            suffix_loc = [i for i, x in enumerate(command_list) if x==prefix]
            suffix = command_list[suffix_loc[0]+1]
            return prefix + suffix
        return False