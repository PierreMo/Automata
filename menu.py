import os
import sys
import io
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageOps
from automata import *
from colorama import init

# Initialize Colorama
init(autoreset=True)

# Set CustomTkinter theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Replace the DEFAULT_DIRECTORY line (around line 14)
DEFAULT_DIRECTORY = os.getcwd()
AUTOMATA_TXT_DIR = os.path.join(DEFAULT_DIRECTORY, "Automata_txt")


class AutomataApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automata Project")
        self.geometry("1920x1080")  # Larger size for better image display
        self.center_window(padding_percent=10)
        # Top container with transparent background
        self.top_container = ctk.CTkFrame(self, fg_color="transparent")
        self.top_container.pack(fill="x", padx=100, pady=5)

        # Title positioned to the left - now larger and blue
        self.label_title = ctk.CTkLabel(
            self.top_container, 
            text="AUTOMATA PROJECT", 
            font=("Impact", 80, "bold"),  # Changed to Impact font and increased size
            text_color="#00BFFF"  # Changed to a brighter blue (Deep Sky Blue)
        )
        self.label_title.pack(side="left", pady=10, padx=10)

        # File selection menu - positioned to the right
        self.file_menu_frame = ctk.CTkFrame(self.top_container)
        self.file_menu_frame.pack(side="right", fill=None, expand=False, pady=5)
        
        # File selection label
        self.file_label = ctk.CTkLabel(self.file_menu_frame, text="Sélectionnez un fichier :", font=("Arial", 14))
        self.file_label.pack(padx=40, pady=(5, 0))
        
        # Create a frame to hold the listbox
        self.file_list_frame = ctk.CTkFrame(self.file_menu_frame)
        self.file_list_frame.pack(padx=10, pady=5)
        
        # Create the scrollable frame - RÉDUIT LA HAUTEUR
        self.file_listbox = ctk.CTkScrollableFrame(self.file_list_frame, width=300, height=100)
        self.file_listbox.pack(fill="both", expand=True)

        # Add files to the listbox as buttons - RÉDUIT LA HAUTEUR DES BOUTONS
        self.file_buttons = []
        for file in self.get_txt_files():
            button = ctk.CTkButton(
                self.file_listbox, 
                text=file,
                command=lambda f=file: self.on_file_selected(f),
                anchor="w",
                height=25,
                fg_color="transparent",  # Make it look like a list item
                hover_color=("gray70", "gray30")  # Light hover effect
            )
            button.pack(fill="x", pady=1)
            self.file_buttons.append(button)

        # Main frame (File content, Image display, Automata table)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=5)  # Réduit le pady de 10 à 5

        # Left column: File content display
        self.textbox = ctk.CTkTextbox(self.main_frame, height=150, wrap="word", font=("Courier", 16))
        self.textbox.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # Middle column: Automata image display
        self.image_frame = ctk.CTkFrame(self.main_frame)
        self.image_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        self.image_label = ctk.CTkLabel(self.image_frame, text="(Aucune image)")
        self.image_label.pack(expand=True, fill="both")

        # Right column: Automata table display
        self.table_frame = ctk.CTkFrame(self.main_frame)
        self.table_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        self.table_label = ctk.CTkLabel(self.table_frame, text="Automata Table", font=("Arial", 14))
        self.table_label.pack(pady=(0, 5))
        self.table_textbox = ctk.CTkTextbox(self.table_frame, wrap="word", font=("Courier", 16))
        self.table_textbox.pack(fill="both", expand=True)

        # Buttons frame
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(pady=5, fill="x", padx=20)  # Réduit le pady de 10 à 5

        # Word recognition frame
        self.word_frame = ctk.CTkFrame(self.button_frame)
        self.word_frame.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        
        self.word_label = ctk.CTkLabel(self.word_frame, text="Test word:", font=("Arial", 12))
        self.word_label.pack(side="left", padx=5)
        
        self.word_entry = ctk.CTkEntry(self.word_frame, width=100)
        self.word_entry.pack(side="left", padx=(5, 2))  # Added 2px right padding for small space
        
        self.test_button = ctk.CTkButton(self.word_frame, text="🔍 Test", command=self.test_word)
        self.test_button.pack(side="left", padx=(0, 5))
        
        # Change the word_frame to have transparent background
        self.word_frame.configure(fg_color="transparent")
        
        # Create a subframe with background just for the entry and button
        self.word_input_frame = ctk.CTkFrame(self.word_frame)
        self.word_input_frame.pack(side="left", pady=5)
        
        # Move the entry and button to this new subframe
        self.word_entry.pack_forget()
        self.test_button.pack_forget()
        
        self.word_entry = ctk.CTkEntry(self.word_input_frame, width=100)
        self.word_entry.pack(side="left", padx=(5, 2))
        
        self.test_button = ctk.CTkButton(self.word_input_frame, text="🔍 Test", command=self.test_word)
        self.test_button.pack(side="left", padx=(2, 5))

        self.determinize_button = ctk.CTkButton(self.button_frame, text="⚙ Déterminiser", command=self.determinize)
        self.determinize_button.pack(side="left", expand=True, padx=5, pady=5)
        
        self.standardize_button = ctk.CTkButton(self.button_frame, text="📐 Standardiser", command=self.standardize)
        self.standardize_button.pack(side="left", expand=True, padx=5, pady=5)
        
        self.minimize_button = ctk.CTkButton(self.button_frame, text="🔧 Minimiser", command=self.minimize)
        self.minimize_button.pack(side="right", expand=True, padx=5, pady=5)

        # Results display
        self.result_label = ctk.CTkLabel(self, text="Résultats :", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=5)

        # AUGMENTÉ LA HAUTEUR DE LA ZONE DE RÉSULTATS
        self.result_textbox = ctk.CTkTextbox(self, height=300, wrap="word", font=("Courier", 14))
        self.result_textbox.pack(pady=5, fill="both", expand=True, padx=20)

        self.selected_file = None  # Stores selected file

    def center_window(self, padding_percent=10):
        """Center the window with a percentage-based padding"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Calculate padding in pixels
        x_padding = 20
        y_padding = 20  

        # Centered position with padding
        x_position = (screen_width - window_width) // 2 - x_padding
        y_position = (screen_height - window_height) // 2 - y_padding

        self.geometry(f"+{x_padding}+{y_padding}")
        
    def get_txt_files(self):
        """List available .txt files in the Automata_txt directory and sort them numerically"""
        automata_dir = os.path.join(DEFAULT_DIRECTORY, "Automata_txt")
        if not os.path.exists(automata_dir):
            messagebox.showwarning("Warning", f"Directory not found: {automata_dir}")
            return []
        
        # Get all text files
        files = [f for f in os.listdir(automata_dir) if f.endswith(".txt")]
        
        # Sort files numerically by extracting the number from automata_X.txt
        def get_file_number(filename):
            try:
                # Extract the number between 'automata_' and '.txt'
                return int(filename.split('_')[1].split('.')[0])
            except (IndexError, ValueError):
                return float('inf')  # Put files without proper numbering at the end
        
        # Sort files by their numeric value
        files.sort(key=get_file_number)
        return files

    def on_file_selected(self, selected_file):
        """Load the selected file, display its content, associated image, and automata table"""
        if selected_file:
            # Highlight the selected file button
            for button in self.file_buttons:
                if button.cget("text") == selected_file:
                    button.configure(fg_color=("gray75", "gray25"))
                else:
                    button.configure(fg_color="transparent")
                    
            self.selected_file = os.path.join(AUTOMATA_TXT_DIR, selected_file)
            self.display_file_content(self.selected_file)
            self.display_automata_image(selected_file)
            # Load automata and display its table in the third column
            try:
                A = Automata.from_file(self.selected_file)
                table_output = self.capture_stdout(A.printCDFA)
                self.table_textbox.delete("1.0", "end")
                self.table_textbox.insert("1.0", table_output)
            except Exception as e:
                self.table_textbox.delete("1.0", "end")
                self.table_textbox.insert("1.0", f"Erreur: {str(e)}")

    def display_file_content(self, file_path):
        """Display the content of the selected file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de lire le fichier : {str(e)}")

    def display_automata_image(self, txt_filename):
        """Resize and display the automaton image to fill the entire frame while keeping proportions"""
        image_path = os.path.join(DEFAULT_DIRECTORY, txt_filename.replace(".txt", ".png"))

        if os.path.exists(image_path):
            img = Image.open(image_path)
            
            # Get frame dimensions
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()

            # Resize while maintaining aspect ratio but filling the entire space
            img = ImageOps.contain(img, (frame_width, frame_height))

            self.photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self.photo, text="")
            self.image_label.image = self.photo  # Prevent garbage collection
        else:
            self.image_label.configure(image=None, text="(Aucune image)")

    def capture_stdout(self, func, *args):
        """Capture the output of printCDFA() and return as text"""
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        try:
            func(*args)
        except Exception as e:
            sys.stdout = sys.__stdout__
            return f"❌ Erreur : {str(e)}"
        sys.stdout = sys.__stdout__
        result = output_buffer.getvalue()
        output_buffer.close()
        return result

    def test_word(self):
        """Test if a word is recognized by the automaton"""
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return

        word = self.word_entry.get().strip()
        if not word:
            messagebox.showerror("Erreur", "Veuillez entrer un mot à tester.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"🔍 Test du mot '{word}'...\n")

        try:
            A = Automata.from_file(self.selected_file)
            # Capture print statements from recognize_word method
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            
            result = A.recognize_word(word)
            
            sys.stdout = sys.__stdout__
            debug_output = output_buffer.getvalue()
            output_buffer.close()
            
            # Display the result with an appropriate emoji
            if result:
                self.result_textbox.insert("end", f"\n✅ Le mot '{word}' est reconnu par l'automate.\n")
            else:
                self.result_textbox.insert("end", f"\n❌ Le mot '{word}' n'est PAS reconnu par l'automate.\n")
            
            # Add debug output if there is any
            if debug_output:
                self.result_textbox.insert("end", f"\n🔧 Détails de l'exécution:\n{debug_output}")
                
        except Exception as e:
            sys.stdout = sys.__stdout__  # Make sure to reset stdout
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Erreur: {str(e)}")

    def determinize(self):
        """Perform determinization and display the result"""
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"📌 Chargement de l'automate depuis {self.selected_file}...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            result = self.capture_stdout(A2.printCDFA)
            self.result_textbox.insert("end", "\n✔ Après déterminisation complète :\n" + result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

    def minimize(self):
        """Perform minimization and display the result"""
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"🔧 Minimisation en cours...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            A3 = A2.minimization()
            result = self.capture_stdout(A3.printCDFA)
            self.result_textbox.insert("end", "\n✔ Après minimisation :\n" + result)
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")

    def standardize(self):
        """Perform standardization and display the result"""
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"📐 Standardisation en cours...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            
            # Check if already standard
            if A1.is_standard():
                self.result_textbox.insert("end", "\n✅ L'automate est déjà standardisé.\n")
                result = self.capture_stdout(A1.printCDFA)
                self.result_textbox.insert("end", "\nAutomate standardisé :\n" + result)
                return
                
            # Standardize the automaton
            A1.standardize()
            result = self.capture_stdout(A1.printCDFA)
            self.result_textbox.insert("end", "\n✅ Après standardisation :\n" + result)
        except Exception as e:
            sys.stdout = sys.__stdout__  # Make sure to reset stdout
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Erreur: {str(e)}")

if __name__ == "__main__":
    app = AutomataApp()
    app.mainloop()