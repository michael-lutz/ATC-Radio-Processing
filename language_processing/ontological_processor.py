import pandas as pd
import re

class OntologicalProcessor():
    def __init__(self):
        self.known_callsign_prefixes = ['american', 'envoy', 'biztex', 'frontier', 'skywest', 'sioux', 'cessna', 'grumman', 'speedbird']

    def find_alt(self, command):
        command = str.lower(command)
        if ('descend' in command) or ('ascend' in command) or ('climb' in command) or ('altitude' in command):
            # check if maintain / descend is here -> then check to see if the nubmer is greater than 1000
            # get the next word in the string
            command_list = str.split(command)
            alt_loc = [i for i, x in enumerate(command_list) if x=='maintain' or x=='' or x=='']
            alt = command_list[alt_loc[0]+1]
            if alt.isdigit():
                return int(alt)

            # check where a number exists in the string -> then return the number
            alt_loc = [i for i, x in enumerate(command_list) if x.isdigit()]
            alt = command_list[alt_loc[0]]
            
        return False

    def find_turn(self, command):
        command = str.lower(command)
        return ('turn' in command) or ('heading' in command) or ('left' in command) or ('right' in command)

    def find_contact(self, command):
        command = str.lower(command)
        return ('contact' in command) or ('tower' in command) or ('radio' in command) or ('up' in command) or ('climb' in command)

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