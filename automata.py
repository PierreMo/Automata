import csv
from collections import deque
from state import State, ALPH, LETTER_ID

DETER_NOT_COMPLETE = -2
NOT_DETERM_INPUT = -1
TRANSITION_BEGIN, NOT_DETERM_TRANSITIONS = 0, 0
TRANSITION_CHAR, DETERMINISTIC, CDFA = 1, 1, 1
TRANSITION_END = 2
MAX_STATE_NB_EXPECTED = 30


class Automata:
    def __init__(self, alph_size: int, nb_states: int):
        # TODO MAKE IT STRONGER
        self.__alph_size = alph_size
        self.__nb_states = nb_states
        self.__states = [State(self.__alph_size,i) for i in range(self.__nb_states)]
        # These variable will be put to True when necessary, but will be but to False again at any modification
        # This will avoid to compute multiple time the same thing
        self.__is_deter = False
        self.__is_complete = False
        self.__is_standard = False
        self.__is_valid = False
    
    # The getters:
    def get_nb_states(self) -> int:
        '''Getter for the number of states'''
        return self.__nb_states
    def get_alph_size(self) -> int:
        '''Getter for the number of symbols'''
        return self.__alph_size
    def get_nb_in_states(self) -> int:
        '''Getter for the number of input states'''
        nb_in = 0
        for id_state in range(self.get_nb_states()):
            if self.get_state(id_state).is_in():
                nb_in += 1
        return nb_in
    def get_nb_out_states(self) -> int:
        '''Getter for the number of output states'''
        nb_out = 0
        for id_state in range(self.get_nb_states()):
            if self.get_state(id_state).is_out():
                nb_out += 1
        return nb_out
    def get_state(self, state_id: int) -> State:
        '''Getter to get the state associated to a given id'''
        return self.__states[state_id]
    
    def is_standard(self) -> bool:
        '''Method wether the automata is standard'''
        if self.__is_standard:
            return True
        else:
            is_std = True

            # should have 1 input
            if self.get_nb_in_states() != 1:
                is_std = False
                return is_std

            # identifying the input state
            cur_state_id = 0
            while not self.get_state(cur_state_id).is_in(): # The previous condition force that there is at least 1 input
                cur_state_id += 1
            in_state_id = cur_state_id

            # should have no transition to the input state
            cur_state_id = 0
            while is_std and cur_state_id < self.get_nb_states():
                cur_alph_id = 0
                while is_std and cur_alph_id < self.get_alph_size():
                    if in_state_id in self.get_state(cur_state_id).get_dests(ALPH[cur_alph_id]):
                        is_std = False
                    cur_alph_id += 1
                cur_state_id += 1

            self.__is_standard = is_std
            return is_std
    
    def is_deterministic(self) -> int:
        '''
        Method which says wether an automata is deterministic
        Return :
            An integer:
                - 1 if deterministic (DETERMINISTIC)
                - -1 if not due to the number of input (NOT_DETERM_INPUT)
                - 0 if not due to multiple destinations (NOT_DETERM_TRANSITIONS)
        '''
        if self.__is_deter:
            return True
        else:
            # Automata should have one input state
            if self.get_nb_in_states() != 1:
                return NOT_DETERM_INPUT

            # Each destination should lead to 0 or 1 state
            is_deter = True
            cur_state_id = 0
            while is_deter and cur_state_id < self.get_nb_states():
                cur_alph_id = 0
                while is_deter and cur_alph_id < self.get_alph_size():
                    if len(self.get_state(cur_state_id).get_dests(ALPH[cur_alph_id])) > 1:
                        is_deter = False
                    cur_alph_id += 1
                cur_state_id += 1
            if is_deter:
                self.__is_deter = True
                return DETERMINISTIC
            else:
                return NOT_DETERM_TRANSITIONS
    
    def is_complete_DFA(self) -> int:
        '''
        Method which says wether a FA is a complete deterministic automata
        Return :
            An integer:
                - 1 if CDFA (CDFA)
                - -1,0 if not deterministic (NOT_DETERM_INPUT, NOT_DETERM_TRANSITIONS)
                - -2 if deterministic but not complete (first problematic state will be printed) (
        '''
        if self.__is_deter and self.__is_complete:
            return True
        else:
            #
            if self.get_nb_in_states() != 1:
                print('Algorithm isn\'t CDFA: it is not a deterministic one.')
                return NOT_DETERM_INPUT
            #
            is_complete = True
            cur_state_id = 0
            while is_complete and cur_state_id < self.get_nb_states():
                cur_alph_id = 0
                while is_complete and cur_alph_id < self.get_alph_size():
                    if len(self.get_state(cur_state_id).get_dests(ALPH[cur_alph_id])) != 1:
                        if len(self.get_state(cur_state_id).get_dests(ALPH[cur_alph_id])) == 0:
                            print('Algorithm isn\'t CDFA: it is not complete for sure and may not be deterministic due to numerous destinations.'
                                  +'\n\t'+'Not complete for state, transition: '+str(cur_state_id)+', '+ALPH[cur_alph_id])
                            output = NOT_DETERM_TRANSITIONS
                        else:
                            print('Algorithm isn\'t CDFA: it is not deterministic for sure and may not be complete.' +
                                  '\n\tNot deterministic for state, transition, number of destinations: '
                                  + str(cur_state_id) + ', ' + ALPH[cur_alph_id] + ', '+  str(len(self.get_state(cur_state_id).get_dests(ALPH[cur_alph_id]))))
                            output = DETER_NOT_COMPLETE
                        is_complete = False
                    cur_alph_id += 1
                cur_state_id += 1
            if is_complete:
                self.__is_deter = True
                self.__is_complete = True
                return CDFA
            else:
                return output
        
    def is_valid(self) -> bool:
        '''Method to know if an Automata is valid
            (verify only for the destinations since the method add_state already ensure, for added states, the size of the alphabet and correct id)'''
        if self.__is_valid:
            return True
        else:
            # check if the destinations exists
            validity = True
            id_state = 0
            while validity and id_state < self.get_nb_states():
                alph_id = 0
                while validity and alph_id < self.get_alph_size():
                    destinations = self.get_state(id_state).get_dests(ALPH[alph_id])
                    if any(dest >= self.get_nb_states() or dest < 0 for dest in destinations):
                        validity = False
                    alph_id += 1
                id_state += 1
            self.__is_valid = validity
            return validity
    
    
    # The setters:
    # Methods for Automata
    def add_state(self, state: State):
        '''
        Method to add a state in an Automata, safely (cohesion of data ensured with alphabet size and id of the nodes)
        (will replace the node the exist with the same id)
        '''
        if state.get_alph_size() != self.__alph_size:
            print("\033[91mIncompatible alphabet size, couldn\'t add the state\033[0m")
        else:
            if state.get_id() >= self.get_nb_states():
                state.mod_id(self.__nb_states)
                self.__nb_states += 1
                self.__states.append(state)
                print('Number of state successfuly increased by 1')
            else :
                self.__states[state.get_id()]=state
                print('State successfuly replaced')
            self.__is_deter = False
            self.__is_complete = False
            self.__is_standard = False
            self.__is_valid = False
    
    def standardize(self) -> bool:
        if self.is_standard():
            return False
        else :
            # looking for the entry states, removing their Input arrow
            entries_id = []
            for i in range(self.get_nb_states()):
                if self.get_state(i).is_in():
                    entries_id.append(i)
                    self.get_state(i).set_not_in()

            # looking: if an entry is an output, where the entries points
            is_output = False
            # using a state so that I don't do multiple times the same transition
            destinations = set()
            for iD in entries_id:
                #if output
                if self.get_state(iD).is_out():
                    is_output = True
                # storing destinations
                for cur_alph_id in range(self.get_alph_size()):
                    cur_dests = self.get_state(iD).get_dests(ALPH[cur_alph_id])
                    for dest in cur_dests:
                        destinations.add(ALPH[cur_alph_id] + str(dest))

            # creating the new state i
            # init
            state_i = State(self.get_alph_size(), self.get_nb_states())
            # entry
            state_i.set_in()
            # output ?
            if is_output:
                state_i.set_out()
            # destinations
            for dest in destinations:
                state_i.add_dest(dest[0], dest[1:])
            # adding to the automata
            self.add_state(state_i)
            self.__is_deter = False
            self.__is_complete = False
            self.__is_standard = True
            return True
    
    def completion(self):
        ''' Method to complete a deterministic Automata'''
        if not self.is_complete_DFA():
            if not self.is_deterministic():
                print("The Automata should be deterministic first")
            else:
                # Completion
                # Add a Garbage state G
                g = State(self.get_alph_size(), self.get_nb_states())
                g.set_label('G')
                for alph_id in range(self.get_alph_size()):
                    g.add_dest(ALPH[alph_id], self.get_nb_states())
                g_id = self.get_nb_states()
                self.add_state(g)
                # Find all the transitions that are empty and put G as destination
                for dest_id in range(self.get_nb_states()):
                    for alph_id in range(self.get_alph_size()):
                        if len(self.get_state(dest_id).get_dests(ALPH[alph_id])) == 0:
                            self.get_state(dest_id).add_dest(ALPH[alph_id], g_id)
                self.__is_complete = True
                # may not be changed but prefer to be safe
                self.__is_standard = False


    
    def determinize_complete(self) -> 'Automata':
        '''
        Method to determinize an Automata, the result will be also complete
        :return
            None if failled
            Automata object if success
        '''
        # ( for each new state (begining with the combination of the states) add the combined destination and if destination is a new state, add it)
        # Identify the input states
        entries_id = []
        for i in range(self.get_nb_states()):
            if self.get_state(i).is_in():
                entries_id.append(i)

        automat_alph_size = self.get_alph_size()
        new_automata = Automata(automat_alph_size, 1)
        # creating a dictionary to store which combination has which id, intiat it with the inputs states
        cur_label = '.'.join([str(state_id) for state_id in entries_id])
        new_states = {cur_label: 0}
        # create a queue to know which state you have to treat
        state_queue = deque()
        state_queue.append(cur_label)

        # run through all  states and process to adding when needed until the queue is empty
        working = True
        count = 0
        while working and state_queue:
            # Propose to close in case of endless loop
            if count == MAX_STATE_NB_EXPECTED:
                print('We arrived at 100 more states, should we continue? Y/N')
                answer = input()
                while answer != 'Y' and answer != 'N':
                    answer = input()
                if answer == 'Y':
                    count = 0
                else:
                    working = False

            # Initialization of the state and it's destinations
            cur_label = state_queue.popleft()
            cur_state = State(automat_alph_size, new_states[cur_label])
            current_destinations = [set() for _ in range(automat_alph_size)]
            cur_state.set_label(cur_label)
            # Running through the states composing the current state
            for state_str in cur_label.split('.'):
                if state_str:
                    if self.get_state(int(state_str)).is_out():
                        cur_state.set_out()
                    for alph_id in range(automat_alph_size):
                        for dest_id in self.get_state(int(state_str)).get_dests(ALPH[alph_id]):
                            current_destinations[alph_id].add(dest_id)
            # Running through the destinations of the current state
            for alph_id in range(automat_alph_size):
                cur_alph_dests = list(current_destinations[alph_id])
                if cur_alph_dests:
                    cur_alph_dests.sort()
                    dest_state_str = '.'.join([str(e) for e in cur_alph_dests])
                    if dest_state_str not in new_states:
                        new_states[dest_state_str] = len(new_states)
                        state_queue.append(dest_state_str)
                    cur_state.add_dest(ALPH[alph_id], new_states[dest_state_str])
            new_automata.add_state(cur_state)
            count += 1

        new_automata.get_state(0).set_in()

        if not working:
            return None

        new_automata.completion()
        # __is_deter, __is_complete and __is_standard have been updated by previous calls to fcts
        return new_automata

    def printCDFA(self):
        '''Method to print Automata with label (for Determinitics ones for exemple)'''
        # Example array with strings of different sizes, including empty strings
        ch = 'Displaying Automata \n'
        array = self._str_label_list()

        # Determine the maximum width for each column, ignoring empty strings
        col_widths = [max(len(item) for item in col if item) for col in zip(*array)]

        # Display the array with aligned columns, ignoring empty strings
        for row in array:
            formatted_row = " | ".join(f"{item:<{width}}" if item else " " * width for item, width in zip(row, col_widths))
            print(formatted_row)

    def _str_label_list(self) -> list:
        '''
        Method to display the state with print()
        '''

        row = self.get_nb_states() + 1
        col = self.get_alph_size() + 2

        items = [['' for _ in range(col)] for __ in range(row)]
        for i in range(2,col):
            items[0][i] = ALPH[i-2]
        for row_nbr in range(1,row):
            # if it is an input or output state
            state_id = row_nbr - 1
            arrow = ""
            if self.get_state(state_id).is_out():
                arrow += '<'
                if not (self.get_state(state_id).is_in()):
                    arrow += '-'
            if self.get_state(state_id).is_in():
                arrow += '->'
            items[row_nbr][0] = arrow
            # It's id or label
            if self.get_state(state_id).get_label() is None:
                name = str(self.get_state(state_id).get_id())
            else:
                name = "(" + str(self.get_state(state_id).get_label()) + ")"
            items[row_nbr][1] = name
            # All the transitions
            for col_nbr in range(2,col):
                alph_id = col_nbr - 2
                transitions_str = ""
                for dest_id in self.get_state(state_id).get_dests(ALPH[alph_id]):
                    if self.get_state(dest_id).get_label() is None:
                        transitions_str += str(dest_id)
                    else:
                        transitions_str += "(" + self.get_state(dest_id).get_label() + ")"
                    transitions_str += '/'
                if not transitions_str:
                    transitions_str += '--'
                else:
                    transitions_str = transitions_str[:-1]
                items[row_nbr][col_nbr] = transitions_str + ''
        return items


    def __split(self, group : list, association : dict) -> list:
        '''
        Method that split the group depending on the group of dest of each state given by association (minimization)
        :return list of list
        '''
        splited_group = {}
        for state_id in group:
            # join the group of destination of the state for each letter of the alphabet, [0] bc deterministic
            cur_group_dest = ','.join([str(association[self.get_state(state_id).get_dests(ALPH[alph_id])[0]]) for alph_id in range(self.get_alph_size())])
            if cur_group_dest not in splited_group:
                splited_group[cur_group_dest] = []
            splited_group[cur_group_dest].append(state_id)
        # sorting to be sure to obtain the same order (avoiding problem in minim. w/ old==groups)
        return [splited_group[key] for key in sorted(splited_group.keys())]
    def minimization(self) -> 'Automata':
        '''
        Method to build a minimized Automata
        return: Automata minimized
        '''
        if self.is_complete_DFA() == CDFA:
            # Splitting in two groups, terminal states and non-terminal states
            groups = [[],[]]
            for state_id in range(self.get_nb_states()):
                groups[self.get_state(state_id).is_out()].append(state_id)
            # Associating each state to its group
            association = {state_id: grp_id for grp_id in range(2) for state_id in groups[grp_id]}

            # Running through the groups and splitting them until it is stable
            old_groups = []
            while old_groups != groups:
                old_groups = groups
                groups = []
                for group in old_groups:
                    for new_group in self.__split(group, association):
                        groups.append(new_group)
                # Update the association dictionary
                association.clear()
                association = {state_id: grp_id for grp_id in range(len(groups)) for state_id in groups[grp_id]}
            if len(groups) == self.get_nb_states():
                print("The Automata was already minimized.")
            # Construct an Automata with the groups obtained
            new_automata = Automata(self.get_alph_size(), self.get_nb_states())
            state_id = 0
            entry_state_id = -1
            while entry_state_id == -1 and state_id < self.get_nb_states():
                entry_state_id = state_id
                state_id += 1
            for group_id in range(len(groups)):
                group = groups[group_id]
                new_state = State(self.get_alph_size(), group_id)
                if entry_state_id in group:
                    new_state.set_in()
                # thanks to theta 0
                if self.get_state(group[0]).is_out():
                    new_state.set_out()
                for alph_id in range(self.get_alph_size()):
                    # putting the correct destination since it is deterministic
                    new_state.add_dest(ALPH[alph_id], self.get_state(group[0]).get_dests(ALPH[alph_id])[0])
                # adding a label to the group
                cur_group_dest = ', '.join([self.get_state(state_id).get_label() if self.get_state(state_id).get_label() is not None else state_id for state_id in group])
                new_state.set_label(cur_group_dest)
                #adding the group state to the new Automata
                new_automata.add_state(new_state)
            return new_automata
        else:
            print("Can't minimize, your Automata should first be a complete and deterministic one")

    def __str__(self) -> str:
        '''
                Method to display the state with print()
                '''
        ch = 'Displaying Automata \n'
        ch += '     \t' + '\t'.join(ALPH[:self.__alph_size]) + '\n'
        # Here we could have directly print the states, but we want to show the labels in the transitions
        for state_id in range(self.get_nb_states()):
            ch += str(self.get_state(state_id)) + '\n'
        return ch


    # The overwrited functions and additional init
    @classmethod
    def from_file(cls, path: str) -> 'Automata':
        '''
        Function to create the Automata associated to a text file
        '''
        try:
            with open(path, 'r') as file:
                # reading the nb of symbols and states
                nb_symbols = int(file.readline())
                nb_states = int(file.readline())
                A = cls(nb_symbols, nb_states)
                # reading the nb of input states and their states number, applying it
                in_states_str = file.readline().split()
                for i in range(1, int(in_states_str[0])+1):
                    A.get_state(int(in_states_str[i])).set_in()
                # reading the nb of output states and their states number, applying it
                out_states_str = file.readline().split()
                for i in range(1, int(out_states_str[0])+1):
                    A.get_state(int(out_states_str[i])).set_out()

                # adding all the destinations, takin in count the case of multiple digits stat id
                nb_transitions = int(file.readline())
                transitions = file.read().split()
                for i in range(nb_transitions):
                    digits_before = []
                    letter = ''
                    digits_after = []
                    for char in transitions[i]:
                        ascii_value = ord(char)
                        # check for digit
                        if 48 <= ascii_value <= 57:
                            if letter:
                                digits_after.append(char)
                            else:
                                digits_before.append(char)
                        elif 97 <= ascii_value <= 122:
                        # check for lowercase letter
                            if letter:
                                raise ValueError("The transition should be one letter.")
                            letter = char
                        else:
                            raise ValueError("The transition contains invalid characters.")
                    # Convert lists to integers
                    from_state_id = int(''.join(digits_before))
                    to_state_id = int(''.join(digits_after))
                    cur_transi = transitions[i]
                    A.get_state(from_state_id).add_dest(letter, to_state_id)

                # ensuring that destinations exist
                validity = A.is_valid()
                if not validity:
                    print("\033[91mBE AWARE YOUR AUTOMATA IS NOT VALID (found a destination that don\'t exists)\033[0m")
                return A

        except FileNotFoundError:
            raise FileNotFoundError("The file does not exist.")
        except IOError:
            raise IOError("An error occurred while reading the file.")
        
    # Other methods
    def to_file(self, path:str):
        '''Method to write the automata in a file text'''
        with open(path, 'w') as file:
            file.write(str(self.get_alph_size()) + '\n')
            file.write(str(self.get_nb_states()) + '\n')
            # writing input states
            ch = str(self.get_nb_in_states()) + ' '
            ch += ' '.join([str(self.__states[i].get_id()) for i in range(self.get_nb_states()) if self.__states[i].is_in()])
            file.write(ch + '\n')
            # writing output states
            ch = str(self.get_nb_out_states()) + ' '
            ch += ' '.join([str(self.__states[i].get_id()) for i in range(self.get_nb_states()) if self.__states[i].is_out()])
            file.write(ch + '\n')
            
            transistions = [str(num_state) + ALPH[num_char] + str(destination)
                            for num_state in range(self.get_nb_states())
                                for num_char in range(self.get_alph_size())
                                    for destination in self.get_state(num_state).get_dests(ALPH[num_char])]
            
            file.write(str(len(transistions))+'\n')
            file.write('\n'.join(transistions))



## TESTS FOR determinize_complete ##

# paths = ['test.txt', 'automata1.txt', 'automata2.txt']


# A1 = Automata.from_file(paths[0])
# print(A1)
# A2 = A1.determinize_complete()
# print("After determinize_complete")
# A2.printCDFA()

# A3 = A2.minimization()
# print("After Minimization")
# A3.printCDFA()



