ALPH = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
LETTER_ID = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18,
    't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24, 'z': 25
}


class State :
    def __init__(self, alph_size: int, state_id: int):
        self.__in_state = False
        self.__out_state = False
        self.__alph_size = alph_size
        self.__state_id = state_id
        self.__dest_states= [set() for _ in range(self.__alph_size)]
        self.__label = None
    
    # Getters
    def get_id(self)->int:
        '''Return the number of the state'''
        return self.__state_id
    def get_dests(self, letter: str) -> list:
        '''Return the list of destinations of the state for the given letter'''
        return list(self.__dest_states[LETTER_ID[letter]])
    def is_in(self) -> bool:
        '''
        Indicates if the state is an input state
        Returns:
            bool
        '''
        return self.__in_state
    def is_out(self) -> bool:
        '''
        Indicates if the state is an output state
        Returns:
            bool
        '''
        return self.__out_state
    def get_alph_size(self) -> int:
        '''Getter for the size of the alphabet'''
        return self.__alph_size

    def get_label(self) -> str:
        '''Getter for the label of the state'''
        return self.__label

    # Setters
    def set_in(self):
        '''Set the state as an input state'''
        self.__in_state = True
    def set_out(self):
        '''Set the state as an output state'''
        self.__out_state = True
    
    def set_not_in(self):
        '''Set the state as not an input state'''
        self.__in_state = False 
    def set_not_out(self):
        '''Set the state as not an output state'''
        self.__out_state = False

    def set_label(self, label: str):
        ''' Method to set a label to the state (will be displaying instead of id when the state is printed)'''
        self.__label = label

    def add_dest(self, letter : str, num_dest: int):
        '''Add a destination state from a given character if it is in the alphabet'''
        if LETTER_ID[letter] < self.get_alph_size():
            self.__dest_states[LETTER_ID[letter]].add((num_dest))
        else:
            assert KeyError('Letter isn\'t in the alphabet of this state')
    
    def mod_id(self, new_id: int):
        ''' Dangerous, modify the id of the state'''
        print('Modifying the id of state ' + str(self.get_id()) + ' to ' + str(new_id))
        self.__state_id = new_id
    
    # Overwriting
    def copy(self) -> 'State':
        '''
        Method to copy a state
        :return: same state with a different address
        '''
        new_state = State()
        new_state.__in_state = self.__in_state
        new_state.__out_state = self.__out_state
        new_state.__alph_size = self.alph_size
        new_state.__state_id = self.__state_id
        new_state.__dest_states = [self.__dest_states[alph_id].copy() for alph_id in range(self.__alph_size)]
        new_state.__label = self.get_label()

    def __str__(self) -> str:
        '''Method to display the state with print(), by id (not with labels)'''
        ch=''
        # Showing if input or output state
        if self.is_out():
            ch+='<'
            if not(self.is_in()):
                ch+='-'
        else:
            ch += ' '
        if self.is_in():
            ch+='->'
        elif self.is_out():
            ch += ' '
        else :
            ch += '  '
        ch+='  '

        ch += str(self.get_id())+'\t'

        # Showing the transitions
        for alph_id in range(self.__alph_size):
            for dest_id in self.get_dests(ALPH[alph_id]):
                ch += str(dest_id) + ','
            if ch[-1] == '\t':
                ch += '--'
            else:
                ch = ch[:-1]
            ch += '\t'
        
        return ch




