## TEST FOR IMPORTING AND EXPORTING IN TXT ##

s1 = State(2,0)
s1.set_in()
s1.add_dest('a', 1)
s1.add_dest('b', 2)

s2 = State(2,1)
s2.add_dest('b', 2)
s2.add_dest('b', 1)
s2.set_in()
s2.set_out()

s3 = State(2,2)

A = Automata(2, 3)

A.add_state(s1)
A.add_state(s2)
A.add_state(s3)
print(A)

s4 = State(2, 5)
s5 = State(2,4)

s5.set_out()
s4.add_dest('a',4)
s3.add_dest('a',4)
s3.add_dest('b',3)

A.add_state(s4)
A.add_state(s5)

print(A)

#A = Automata.from_file('automata1.txt')
#print(A)

fPath = 'test.txt'

A.to_file(fPath)

A2 = Automata.from_file(fPath)
print(A2)

## TESTS FOR is STANDARD ##

paths = ['test.txt', 'automata1.txt', 'automata2.txt']

cur_path_id = 0
A1 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A1)
print(A1.is_standard())

cur_path_id = 1
A2 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A2)
print(A2.is_standard())

cur_path_id = 2
A3 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A3)
print(A3.is_standard())



## TESTS FOR IS DETERMINISTIC  ##

paths = ['test.txt', 'automata1.txt', 'automata2.txt']

cur_path_id = 0
A1 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A1)
print(A1.is_deterministic())

cur_path_id = 1
A2 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A2)
print(A2.is_deterministic())

cur_path_id = 2
A3 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A3)
print(A3.is_deterministic())




# TESTS FOR DFA COMPLETE


paths = ['test.txt', 'automata1.txt', 'automata2.txt','automata3.txt']

cur_path_id = 0
A1 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A1)
print(A1.is_complete_DFA())

cur_path_id = 1
A2 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A2)
print(A2.is_complete_DFA())

cur_path_id = 2
A3 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A3)
print(A3.is_complete_DFA())

cur_path_id = 3
A4 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A4)
print(A4.is_complete_DFA())




## TESTS FOR STANDARDIZATION ##

paths = ['test.txt', 'automata1.txt', 'automata2.txt']

cur_path_id = 0
A1 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A1)
istd = A1.is_standard()
print(istd)
if not istd:
    print('Standardizing the automata')
    A1.standardize()
    print(A1)

cur_path_id = 1
A2 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A2)
istd = A2.is_standard()
print(istd)
if not istd:
    print('Standardizing the automata')
    A2.standardize()
    print(A2)

cur_path_id = 2
A3 = Automata.from_file(paths[cur_path_id])
print(paths[cur_path_id])
print(A3)
istd = A3.is_standard()
print(istd)
if not istd:
    print('Standardizing the automata')
    A3.standardize()
    print(A3)





## TESTS FOR COMPLETION ##

for path in paths:
    A1 = Automata.from_file(path)
    print(path)
    print(A1)
    is_comp = A1.is_complete_DFA()
    print(is_comp)
    if not is_comp:
        print('Completing the automata')
        A1.completion()
        print(A1)
paths = ['test.txt', 'automata1.txt', 'automata2.txt']



