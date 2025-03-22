Automata Project

Our code is in Python 3.12
To use our project as a library for automatas you just need automat.py and state.py, without any library
To use our project with its interface you need to install the libraries: customtkinter, pillow, colorama. And then lunch menu.py

Our code allow to
-	Read a FA from a text file, displaying it (Automata.from_file(path), print(A), A.printCDFA())
- Knowing if a FA is: deterministic? deterministic and complete? Standard? (A.is_deterministic(), A.is_complete_DFA(), A.is_standard())
- Obtain a standardized FA of another (A.standardize())
- Obtain a determinized FA of another (A.determinize_complete())
- Obtain a minimized FA of another (A.minimization())
- Know if a given word is recognized by an FA (A.recognize_word())
- Create the complentary automata of another (A.complementary_automata())
- Additional features: writing automatas in file, creating automatas with methods (A.to_file(path)...)

Our Project do NOT deal with Asynchronous automatas
