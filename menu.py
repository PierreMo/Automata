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


class AutomataTextMenu:
    """Class for text-based menu interface for automata operations"""
    
    def __init__(self):
        self.selected_file = None
        self.created_complement_files = []
        print("\n===== AUTOMATA PROJECT - TEXT MENU =====\n")
    
    def run(self):
        """Run the text menu in a loop until user exits"""
        while True:
            self.display_main_menu()
            choice = input("\nChoisissez une option (1-9): ")
            
            if choice == '1':
                self.select_automaton()
            elif choice == '2':
                self.test_word()
            elif choice == '3':
                self.determinize()
            elif choice == '4':
                self.standardize()
            elif choice == '5':
                self.minimize()
            elif choice == '6':
                self.complementary()
            elif choice == '7':
                self.check_properties()
            elif choice == '8':
                self.display_current_automaton()
            elif choice == '9':
                self.handle_exit()
                break
            else:
                print("❌ Option invalide, veuillez réessayer.")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def display_main_menu(self):
        """Display the main menu options"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== AUTOMATA PROJECT - TEXT MENU =====\n")
        print("1. Sélectionner un automate de 1 à 44")
        print("2. Tester un mot")
        print("3. Déterminiser l'automate")
        print("4. Standardiser l'automate")
        print("5. Minimiser l'automate")
        print("6. Créer l'automate complémentaire")
        print("7. Vérifier les propriétés")
        print("8. Afficher l'automate courant")
        print("9. Quitter")
        
        # Show current automaton if selected
        if self.selected_file:
            print(f"\nAutomate actuel: {os.path.basename(self.selected_file)}")
    
    def select_automaton(self):
        """Let the user select an automaton from available files"""
        files = self.get_txt_files()
        
        if not files:
            print("❌ Aucun fichier d'automate trouvé.")
            return
        
        print("\n=== Automates disponibles ===\n")
        for i, file in enumerate(files, 1):
            print(f"{i}. {os.path.splitext(file)[0]}")
        
        try:
            choice = int(input("\nChoisissez un automate (numéro): "))
            if 1 <= choice <= len(files):
                selected = files[choice-1]
                self.selected_file = os.path.join(AUTOMATA_TXT_DIR, selected)
                self.display_file_content(self.selected_file)
                print(f"\n✅ Automate '{selected}' sélectionné.")
            else:
                print("❌ Numéro invalide.")
        except ValueError:
            print("❌ Veuillez entrer un numéro valide.")
    
    def get_txt_files(self):
        """List available .txt files in the Automata_txt directory and sort them numerically"""
        automata_dir = os.path.join(DEFAULT_DIRECTORY, "Automata_txt")
        if not os.path.exists(automata_dir):
            print(f"⚠️ Répertoire non trouvé: {automata_dir}")
            return []
        
        # Get all text files
        files = [f for f in os.listdir(automata_dir) if f.endswith(".txt")]
        
        # Sort files numerically by extracting the number from automata_X.txt
        def get_file_number(filename):
            try:
                return int(filename.split('_')[1].split('.')[0])
            except (IndexError, ValueError):
                return float('inf')
        
        files.sort(key=get_file_number)
        return files
    
    def display_file_content(self, file_path):
        """Display the content of the selected file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            print("\n=== Contenu du fichier ===\n")
            print(content)
        except Exception as e:
            print(f"❌ Impossible de lire le fichier : {str(e)}")
    
    def display_current_automaton(self):
        """Display the current automaton details"""
        if not self.selected_file:
            print("❌ Aucun automate sélectionné.")
            return
            
        try:
            A = Automata.from_file(self.selected_file)
            print("\n=== Automate courant ===\n")
            print(f"Fichier: {os.path.basename(self.selected_file)}")
            
            # Capture and display automaton table
            table_output = self.capture_stdout(A.printCDFA)
            print("\n" + table_output)
            
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
    
    def test_word(self):
        """Test if a word is recognized by the automaton"""
        if not self.selected_file:
            print("❌ Veuillez d'abord sélectionner un automate.")
            return
            
        word = input("\nEntrez un mot à tester: ").strip()
        if not word:
            print("❌ Veuillez entrer un mot à tester.")
            return
            
        print(f"\n🔍 Test du mot '{word}'...")
            
        try:
            A = Automata.from_file(self.selected_file)
            
            # Capture print statements
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            
            result = A.recognize_word(word)
            
            sys.stdout = sys.__stdout__
            debug_output = output_buffer.getvalue()
            output_buffer.close()
            
            if result:
                print(f"\n✅ Le mot '{word}' est reconnu par l'automate.")
            else:
                print(f"\n❌ Le mot '{word}' n'est PAS reconnu par l'automate.")
            
            if debug_output:
                print(f"\n🔧 Détails de l'exécution:\n{debug_output}")
                
        except Exception as e:
            sys.stdout = sys.__stdout__
            print(f"\n❌ Erreur: {str(e)}")
    
    def determinize(self):
        """Perform determinization and display the result"""
        if not self.selected_file:
            print("❌ Veuillez d'abord sélectionner un automate.")
            return
            
        print(f"\n📌 Chargement de l'automate depuis {self.selected_file}...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            result = self.capture_stdout(A2.printCDFA)
            print("\n✔ Après déterminisation complète :\n" + result)
        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
    
    def standardize(self):
        """Perform standardization and display the result"""
        if not self.selected_file:
            print("❌ Veuillez d'abord sélectionner un automate.")
            return
            
        print(f"\n📐 Standardisation en cours...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            
            if A1.is_standard():
                print("\n✅ L'automate est déjà standardisé.")
                result = self.capture_stdout(A1.printCDFA)
                print("\nAutomate standardisé :\n" + result)
                return
                
            A1.standardize()
            result = self.capture_stdout(A1.printCDFA)
            print("\n✅ Après standardisation :\n" + result)
        except Exception as e:
            sys.stdout = sys.__stdout__
            print(f"\n❌ Erreur: {str(e)}")
    
    def minimize(self):
        """Perform minimization and display the result"""
        if not self.selected_file:
            print("❌ Veuillez d'abord sélectionner un automate.")
            return
            
        print(f"\n🔧 Minimisation en cours...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            A3 = A2.minimization()
            result = self.capture_stdout(A3.printCDFA)
            print("\n✔ Après minimisation :\n" + result)
        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
    
    def complementary(self):
        """Create complementary automaton"""
        if not self.selected_file:
            print("❌ Veuillez d'abord sélectionner un automate.")
            return
            
        print(f"\n🔄 Création de l'automate complémentaire...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            complementary = A1.complementary_automata()
            result = self.capture_stdout(complementary.printCDFA)
            print("\n✅ Automate complémentaire créé :\n" + result)
            
            save = input("\nVoulez-vous sauvegarder l'automate complémentaire? (o/n): ").lower()
            if save == 'o' or save == 'oui':
                base_filename = os.path.basename(self.selected_file)
                name_without_ext = os.path.splitext(base_filename)[0]
                save_path = os.path.join(AUTOMATA_TXT_DIR, f"{name_without_ext}_complement.txt")
                
                complementary.to_file(save_path)
                print(f"\n💾 Automate complémentaire sauvegardé sous : {save_path}")
                
                self.created_complement_files.append(save_path)
        except Exception as e:
            print(f"\n❌ Erreur: {str(e)}")
    
    def check_properties(self):
        """Check various properties of the automaton"""
        if not self.selected_file:
            print("❌ Veuillez d'abord sélectionner un automate.")
            return
            
        try:
            A = Automata.from_file(self.selected_file)
            
            print("\n=== Vérification des propriétés ===\n")
            
            # Check if deterministic
            det_result = A.is_deterministic()
            print("🔍 Est déterministe?")
            if det_result == DETERMINISTIC:
                print("   ✅ L'automate est DÉTERMINISTE.")
            elif det_result == NOT_DETERM_INPUT:
                print("   ❌ L'automate n'est PAS déterministe:")
                print("      → L'automate doit avoir exactement un état initial.")
            else:  # NOT_DETERM_TRANSITIONS
                print("   ❌ L'automate n'est PAS déterministe:")
                print("      → Une transition a plusieurs destinations pour une même lettre.")
            
            # Check if CDFA
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            
            cdfa_result = A.is_complete_DFA(False)
            
            sys.stdout = sys.__stdout__
            debug_output = output_buffer.getvalue()
            output_buffer.close()
            
            print("\n🔍 Est un CDFA?")
            if cdfa_result == CDFA:
                print("   ✅ L'automate est un AUTOMATE FINI DÉTERMINISTE COMPLET.")
            elif cdfa_result == NOT_DETERM_INPUT:
                print("   ❌ L'automate n'est PAS un CDFA:")
                print("      → L'automate doit avoir exactement un état initial.")
            elif cdfa_result == NOT_DETERM_TRANSITIONS:
                print("   ❌ L'automate n'est PAS un CDFA:")
                print("      → Une transition a plusieurs destinations pour une même lettre.")
            elif cdfa_result == DETER_NOT_COMPLETE:
                print("   ❌ L'automate n'est PAS un CDFA:")
                print("      → L'automate est déterministe mais n'est pas complet.")
                
            if debug_output:
                print(f"\n      Détails : {debug_output}")
            
            # Check if standard
            std_result = A.is_standard()
            print("\n🔍 Est standard?")
            if std_result:
                print("   ✅ L'automate est STANDARD.")
            else:
                print("   ❌ L'automate n'est PAS standard.")
                
        except Exception as e:
            sys.stdout = sys.__stdout__
            print(f"\n❌ Erreur: {str(e)}")
    
    def capture_stdout(self, func, *args):
        """Capture the output of functions and return as text"""
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
    
    def handle_exit(self):
        """Handle program exit and cleanup"""
        if self.created_complement_files:
            print(f"\nVous avez créé {len(self.created_complement_files)} fichiers d'automates complémentaires.")
            delete = input("Voulez-vous les supprimer? (o/n): ").lower()
            
            if delete == 'o' or delete == 'oui':
                files_deleted = 0
                for file_path in self.created_complement_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            files_deleted += 1
                    except Exception as e:
                        print(f"Erreur lors de la suppression de {file_path}: {str(e)}")
                
                print(f"{files_deleted} fichiers d'automates complémentaires supprimés.")
        
        print("\nMerci d'avoir utilisé Automata Project! Au revoir.")


class AutomataApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Add a list to track created complement files
        self.created_complement_files = []
        
        # Add protocol to intercept the window close event
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Automata Project")
        self.geometry("1920x1080")  # Larger size for better image display
        self.center_window(padding_percent=10)
        # Top container with transparent background
        self.top_container = ctk.CTkFrame(self, fg_color="transparent")
        self.top_container.pack(fill="x", padx=100, pady=5)
        self.selected_file = None  # Stores selected file
        self.current_automata = None  # Stocke l'automate actuel en mémoire

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
            # Display name without .txt extension
            display_name = os.path.splitext(file)[0]
            button = ctk.CTkButton(
                self.file_listbox, 
                text=display_name,
                command=lambda f=file: self.on_file_selected(f),  # Keep full filename for internal use
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

        self.complement_button = ctk.CTkButton(self.button_frame, text="🔄 Complémentaire", command=self.complementary)
        self.complement_button.pack(side="right", expand=True, padx=5, pady=5)

        # Move the verification frame here - BEFORE the results display
        self.check_frame = ctk.CTkFrame(self)
        self.check_frame.pack(pady=5, fill="x", padx=20)

        self.check_label = ctk.CTkLabel(self.check_frame, text="Vérifications:", font=("Arial", 14, "bold"))
        self.check_label.pack(side="left", padx=(5, 15))

        # Boutons de vérification
        self.check_deterministic = ctk.CTkButton(self.check_frame, text="🔍 Est déterministe?", 
                                                command=self.check_is_deterministic)
        self.check_deterministic.pack(side="left", expand=True, padx=5, pady=5)

        self.check_complete = ctk.CTkButton(self.check_frame, text="🔍 Est CDFA?", 
                                        command=self.check_is_complete_dfa)
        self.check_complete.pack(side="left", expand=True, padx=5, pady=5)

        self.check_standard = ctk.CTkButton(self.check_frame, text="🔍 Est standard?", 
                                        command=self.check_is_standard)
        self.check_standard.pack(side="left", expand=True, padx=5, pady=5)

        # Results display - now AFTER the verification frame
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
        x_padding = 0
        y_padding = 0

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
            # Highlight the selected file button - comparing with display names (without .txt)
            selected_display_name = os.path.splitext(selected_file)[0]
            for button in self.file_buttons:
                if button.cget("text") == selected_display_name:
                    button.configure(fg_color=("gray75", "gray25"))
                else:
                    button.configure(fg_color="transparent")
                    
            self.selected_file = os.path.join(AUTOMATA_TXT_DIR, selected_file)
            self.display_file_content(self.selected_file)
            
            # Ensure the image frame is sized before displaying the image
            self.update_idletasks()
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
        
        # Check if this is a complementary automata file
        is_complement = "_complement" in txt_filename
        
        if is_complement:
            # Clear any previous image by removing references
            self.photo = None
            self.image_label.configure(
                image=None, 
                text="[Automate complémentaire]\n\nAucune image disponible pour\nles automates complémentaires",
                font=("Arial", 16, "bold")
            )
            # Remove persistent image reference to ensure no background image is displayed
            self.image_label.image = None
            return
                
        # Update the path to use Automata_img folder
        image_path = os.path.join(DEFAULT_DIRECTORY, "Automata_img", txt_filename.replace(".txt", ".png"))

        if os.path.exists(image_path):
            img = Image.open(image_path)
            
            # Get frame dimensions
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()
            
            # Define maximum dimensions
            MAX_WIDTH = 600
            MAX_HEIGHT = 500
            
            # Calculate dimensions that respect both aspect ratio and maximum size
            img_width, img_height = img.size
            width_ratio = MAX_WIDTH / img_width if img_width > MAX_WIDTH else 1
            height_ratio = MAX_HEIGHT / img_height if img_height > MAX_HEIGHT else 1
            
            # Use the smaller ratio to ensure image fits within both constraints
            scale_ratio = min(width_ratio, height_ratio, 1.0)
            
            # Calculate final dimensions
            final_width = int(img_width * scale_ratio)
            final_height = int(img_height * scale_ratio)
            
            # Create a CTkImage with the calculated size
            self.photo = ctk.CTkImage(light_image=img, dark_image=img, size=(final_width, final_height))
            self.image_label.configure(image=self.photo, text="")
            # Keep a reference to avoid garbage collection
            self.image_label.image = self.photo
        else:
            self.image_label.configure(image=None, text=f"(Image non trouvée à {image_path})")
            print(f"Image not found: {image_path}")

        
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

    def complementary(self):
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"🔄 Création de l'automate complémentaire...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            complementary = A1.complementary_automata()
            result = self.capture_stdout(complementary.printCDFA)
            self.result_textbox.insert("end", "\n✅ Automate complémentaire créé :\n" + result)
            
            # Option de sauvegarde
            if messagebox.askyesno("Sauvegarder", "Voulez-vous sauvegarder l'automate complémentaire dans un fichier?"):
                # Créer le nom du fichier basé sur l'original
                base_filename = os.path.basename(self.selected_file)
                name_without_ext = os.path.splitext(base_filename)[0]
                save_path = os.path.join(AUTOMATA_TXT_DIR, f"{name_without_ext}_complement.txt")
                
                complementary.to_file(save_path)
                self.result_textbox.insert("end", f"\n💾 Automate complémentaire sauvegardé sous : {save_path}\n")
                
                # Track the created complement file
                self.created_complement_files.append(save_path)
                
                # Optionnellement, recharger la liste de fichiers
                self.refresh_file_list()
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Erreur: {str(e)}")

    def refresh_file_list(self):
        """Refresh the file list after saving a new automaton"""
        # Remove old buttons
        for button in self.file_buttons:
            button.destroy()
        self.file_buttons = []
        
        # Add new buttons
        for file in self.get_txt_files():
            # Display name without .txt extension
            display_name = os.path.splitext(file)[0]
            button = ctk.CTkButton(
                self.file_listbox, 
                text=display_name,
                command=lambda f=file: self.on_file_selected(f),
                anchor="w",
                height=25,
                fg_color="transparent",
                hover_color=("gray70", "gray30")
            )
            button.pack(fill="x", pady=1)
            self.file_buttons.append(button)

    def check_is_deterministic(self):
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "🔍 Vérification si l'automate est déterministe...\n")
        
        try:
            A = Automata.from_file(self.selected_file)
            result = A.is_deterministic()
            
            if result == DETERMINISTIC:
                self.result_textbox.insert("end", "✅ L'automate est DÉTERMINISTE.\n")
            elif result == NOT_DETERM_INPUT:
                self.result_textbox.insert("end", "❌ L'automate n'est PAS déterministe : \n")
                self.result_textbox.insert("end", "   → L'automate doit avoir exactement un état initial.\n")
            else:  # result == NOT_DETERM_TRANSITIONS
                self.result_textbox.insert("end", "❌ L'automate n'est PAS déterministe : \n")
                self.result_textbox.insert("end", "   → Une transition a plusieurs destinations pour une même lettre.\n")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Erreur: {str(e)}")

    def check_is_complete_dfa(self):
        """Check if the automaton is a complete deterministic finite automaton"""
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "🔍 Vérification si l'automate est un CDFA...\n")
        
        try:
            A = Automata.from_file(self.selected_file)
            
            # Capture les sorties potentielles de la fonction
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            
            result = A.is_complete_DFA(False)
            
            sys.stdout = sys.__stdout__
            debug_output = output_buffer.getvalue()
            output_buffer.close()
            
            if result == CDFA:
                self.result_textbox.insert("end", "✅ L'automate est un AUTOMATE FINI DÉTERMINISTE COMPLET.\n")
            elif result == NOT_DETERM_INPUT:
                self.result_textbox.insert("end", "❌ L'automate n'est PAS un CDFA : \n")
                self.result_textbox.insert("end", "   → L'automate doit avoir exactement un état initial.\n")
            elif result == NOT_DETERM_TRANSITIONS:
                self.result_textbox.insert("end", "❌ L'automate n'est PAS un CDFA : \n")
                self.result_textbox.insert("end", "   → Une transition a plusieurs destinations pour une même lettre.\n")
            elif result == DETER_NOT_COMPLETE:
                self.result_textbox.insert("end", "❌ L'automate n'est PAS un CDFA : \n")
                self.result_textbox.insert("end", "   → L'automate est déterministe mais n'est pas complet.\n")
            
            # Ajouter les détails de debug s'ils existent
            if debug_output:
                self.result_textbox.insert("end", f"\n🔧 Détails :\n{debug_output}")
        
        except Exception as e:
            sys.stdout = sys.__stdout__  # S'assurer de restaurer stdout
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Erreur: {str(e)}")

    def check_is_standard(self):
        """Check if the automaton is standard"""
        if not self.selected_file:
            messagebox.showerror("Erreur", "Veuillez d'abord sélectionner un fichier.")
            return
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "🔍 Vérification si l'automate est standard...\n")
        
        try:
            A = Automata.from_file(self.selected_file)
            result = A.is_standard()
            
            if result:
                self.result_textbox.insert("end", "✅ L'automate est STANDARD.\n")
            else:
                self.result_textbox.insert("end", "❌ L'automate n'est PAS standard.\n")
        
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur est survenue : {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Erreur: {str(e)}")
    
    def on_closing(self):
        """Handle window closing event by deleting created complement files"""
        if self.created_complement_files:
            if messagebox.askyesno("Confirmation", 
                                  f"Voulez-vous supprimer les {len(self.created_complement_files)} fichiers d'automates complémentaires créés pendant cette session?"):
                files_deleted = 0
                for file_path in self.created_complement_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            files_deleted += 1
                    except Exception as e:
                        print(f"Erreur lors de la suppression de {file_path}: {str(e)}")
                
                print(f"{files_deleted} fichiers d'automates complémentaires supprimés.")
        
        self.destroy()


def main():
    """Main function to choose interface mode"""
    print("=== AUTOMATA PROJECT ===")
    print("1. Mode texte (CLI)")
    print("2. Mode graphique (GUI)")
    
    while True:
        choice = input("\nChoisissez le mode d'interface (1 ou 2): ")
        
        if choice == '1':
            text_menu = AutomataTextMenu()
            text_menu.run()
            break
        elif choice == '2':
            app = AutomataApp()
            app.mainloop()
            break
        else:
            print("❌ Option invalide, veuillez choisir 1 ou 2.")


if __name__ == "__main__":
    main()