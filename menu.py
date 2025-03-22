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

# Set DEFAULT_DIRECTORY (around line 14)
DEFAULT_DIRECTORY = os.getcwd()
AUTOMATA_TXT_DIR = os.path.join(DEFAULT_DIRECTORY, "Automata_txt")


class AutomataTextMenu:
    """Class for a text-based menu interface for automata operations"""
    
    def __init__(self):
        self.selected_file = None
        self.created_complement_files = []
        print("\n===== AUTOMATA PROJECT - TEXT MENU =====\n")
    
    def run(self):
        """Run the text menu in a loop until the user exits"""
        while True:
            self.display_main_menu()
            choice = input("\nChoose an option (1-9): ")
            
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
                print("❌ Invalid option, please try again.")
            
            input("\nPress Enter to continue...")
    
    def display_main_menu(self):
        """Display the main menu options"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n===== AUTOMATA PROJECT - TEXT MENU =====\n")
        print("1. Select an automaton from 1 to 44")
        print("2. Test a word")
        print("3. Determinize the automaton")
        print("4. Standardize the automaton")
        print("5. Minimize the automaton")
        print("6. Create the complementary automaton")
        print("7. Check properties")
        print("8. Display the current automaton")
        print("9. Quit")
        
        # Show current automaton if selected
        if self.selected_file:
            print(f"\nCurrent automaton: {os.path.basename(self.selected_file)}")
    
    def select_automaton(self):
        """Let the user select an automaton from available files"""
        files = self.get_txt_files()
        
        if not files:
            print("❌ No automata file found.")
            return
        
        print("\n=== Available Automata ===\n")
        for i, file in enumerate(files, 1):
            print(f"{i}. {os.path.splitext(file)[0]}")
        
        try:
            choice = int(input("\nChoose an automaton (number): "))
            if 1 <= choice <= len(files):
                selected = files[choice - 1]
                self.selected_file = os.path.join(AUTOMATA_TXT_DIR, selected)
                self.display_file_content(self.selected_file)
                print(f"\n✅ Automaton '{selected}' selected.")
            else:
                print("❌ Invalid number.")
        except ValueError:
            print("❌ Please enter a valid number.")
    
    def get_txt_files(self):
        """List available .txt files in the Automata_txt directory and sort them numerically"""
        automata_dir = os.path.join(DEFAULT_DIRECTORY, "Automata_txt")
        if not os.path.exists(automata_dir):
            print(f"⚠️ Directory not found: {automata_dir}")
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
            print("\n=== File Content ===\n")
            print(content)
        except Exception as e:
            print(f"❌ Unable to read the file: {str(e)}")
    
    def display_current_automaton(self):
        """Display the current automaton details"""
        if not self.selected_file:
            print("❌ No automaton selected.")
            return
            
        try:
            A = Automata.from_file(self.selected_file)
            print("\n=== Current Automaton ===\n")
            print(f"File: {os.path.basename(self.selected_file)}")
            
            # Capture and display automaton table
            table_output = self.capture_stdout(A.printCDFA)
            print("\n" + table_output)
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    def test_word(self):
        """Test if a word is recognized by the automaton"""
        if not self.selected_file:
            print("❌ Please select an automaton first.")
            return
            
        word = input("\nEnter a word to test: ").strip()
        if not word:
            print("❌ Please enter a word to test.")
            return
            
        print(f"\n🔍 Testing the word '{word}'...")
            
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
                print(f"\n✅ The word '{word}' is recognized by the automaton.")
            else:
                print(f"\n❌ The word '{word}' is NOT recognized by the automaton.")
            
            if debug_output:
                print(f"\n🔧 Execution details:\n{debug_output}")
                
        except Exception as e:
            sys.stdout = sys.__stdout__
            print(f"\n❌ Error: {str(e)}")
    
    def determinize(self):
        """Perform determinization and display the result"""
        if not self.selected_file:
            print("❌ Please select an automaton first.")
            return
            
        print(f"\n📌 Loading the automaton from {self.selected_file}...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            result = self.capture_stdout(A2.printCDFA)
            print("\n✔ After complete determinization:\n" + result)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    
    def standardize(self):
        """Perform standardization and display the result"""
        if not self.selected_file:
            print("❌ Please select an automaton first.")
            return
            
        print(f"\n📐 Standardization in progress...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            
            if A1.is_standard():
                print("\n✅ The automaton is already standardized.")
                result = self.capture_stdout(A1.printCDFA)
                print("\nStandardized automaton:\n" + result)
                return
                
            A1.standardize()
            result = self.capture_stdout(A1.printCDFA)
            print("\n✅ After standardization:\n" + result)
        except Exception as e:
            sys.stdout = sys.__stdout__
            print(f"\n❌ Error: {str(e)}")
    
    def minimize(self):
        """Perform minimization and display the result"""
        if not self.selected_file:
            print("❌ Please select an automaton first.")
            return
            
        print(f"\n🔧 Minimization in progress...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            A3 = A2.minimization()
            result = self.capture_stdout(A3.printCDFA)
            print("\n✔ After minimization:\n" + result)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    
    def complementary(self):
        """Create the complementary automaton"""
        if not self.selected_file:
            print("❌ Please select an automaton first.")
            return
            
        print(f"\n🔄 Creating the complementary automaton...")
            
        try:
            A1 = Automata.from_file(self.selected_file)
            complementary = A1.complementary_automata()
            result = self.capture_stdout(complementary.printCDFA)
            print("\n✅ Complementary automaton created:\n" + result)
            
            save = input("\nDo you want to save the complementary automaton? (y/n): ").lower()
            if save == 'y' or save == 'yes':
                base_filename = os.path.basename(self.selected_file)
                name_without_ext = os.path.splitext(base_filename)[0]
                save_path = os.path.join(AUTOMATA_TXT_DIR, f"{name_without_ext}_complement.txt")
                
                complementary.to_file(save_path)
                print(f"\n💾 Complementary automaton saved as: {save_path}")
                
                self.created_complement_files.append(save_path)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
    
    def check_properties(self):
        """Check various properties of the automaton"""
        if not self.selected_file:
            print("❌ Please select an automaton first.")
            return
            
        try:
            A = Automata.from_file(self.selected_file)
            
            print("\n=== Checking Properties ===\n")
            
            # Check if deterministic
            det_result = A.is_deterministic()
            print("🔍 Is it deterministic?")
            if det_result == DETERMINISTIC:
                print("   ✅ The automaton is DETERMINISTIC.")
            elif det_result == NOT_DETERM_INPUT:
                print("   ❌ The automaton is NOT deterministic:")
                print("      → The automaton must have exactly one initial state.")
            else:  
                print("   ❌ The automaton is NOT deterministic:")
                print("      → A transition has multiple destinations for the same letter.")
            
            # Check if CDFA
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            
            cdfa_result = A.is_complete_DFA(False)
            
            sys.stdout = sys.__stdout__
            debug_output = output_buffer.getvalue()
            output_buffer.close()
            
            print("\n🔍 Is it a CDFA?")
            if cdfa_result == CDFA:
                print("   ✅ The automaton is a COMPLETE DETERMINISTIC FINITE AUTOMATON.")
            elif cdfa_result == NOT_DETERM_INPUT:
                print("   ❌ The automaton is NOT a CDFA:")
                print("      → The automaton must have exactly one initial state.")
            elif cdfa_result == NOT_DETERM_TRANSITIONS:
                print("   ❌ The automaton is NOT a CDFA:")
                print("      → A transition has multiple destinations for the same letter.")
            elif cdfa_result == DETER_NOT_COMPLETE:
                print("   ❌ The automaton is NOT a CDFA:")
                print("      → The automaton is deterministic but not complete.")
                
            if debug_output:
                print(f"\n      Details: {debug_output}")
            
            # Check if standard
            std_result = A.is_standard()
            print("\n🔍 Is it standardized?")
            if std_result:
                print("   ✅ The automaton is STANDARD.")
            else:
                print("   ❌ The automaton is NOT standardized.")
                
        except Exception as e:
            sys.stdout = sys.__stdout__
            print(f"\n❌ Error: {str(e)}")
    
    def capture_stdout(self, func, *args):
        """Capture the output of functions and return it as text"""
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        try:
            func(*args)
        except Exception as e:
            sys.stdout = sys.__stdout__
            return f"❌ Error: {str(e)}"
        sys.stdout = sys.__stdout__
        result = output_buffer.getvalue()
        output_buffer.close()
        return result
    
    def handle_exit(self):
        """Handle program exit and cleanup"""
        if self.created_complement_files:
            print(f"\nYou have created {len(self.created_complement_files)} complementary automaton file(s).")
            delete = input("Do you want to delete them? (y/n): ").lower()
            
            if delete == 'y' or delete == 'yes':
                files_deleted = 0
                for file_path in self.created_complement_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            files_deleted += 1
                    except Exception as e:
                        print(f"Error deleting {file_path}: {str(e)}")
                
                print(f"{files_deleted} complementary automaton file(s) deleted.")
        
        print("\nThank you for using Automata Project! Goodbye.")


class AutomataApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.created_complement_files = []
       
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title("Automata Project")
        self.geometry("1920x1080") 
        self.center_window(padding_percent=10)
        
        self.top_container = ctk.CTkFrame(self, fg_color="transparent")
        self.top_container.pack(fill="x", padx=100, pady=5)
        self.selected_file = None  
        self.current_automata = None  

       
        self.label_title = ctk.CTkLabel(
            self.top_container, 
            text="AUTOMATA PROJECT", 
            font=("Impact", 80, "bold"),  
            text_color="#00BFFF"  
        )
        self.label_title.pack(side="left", pady=10, padx=10)

        
        self.file_menu_frame = ctk.CTkFrame(self.top_container)
        self.file_menu_frame.pack(side="right", fill=None, expand=False, pady=5)
        
        
        self.file_label = ctk.CTkLabel(self.file_menu_frame, text="Select a file:", font=("Arial", 14))
        self.file_label.pack(padx=40, pady=(5, 0))
        
        self.file_list_frame = ctk.CTkFrame(self.file_menu_frame)
        self.file_list_frame.pack(padx=10, pady=5)
        
        
        self.file_listbox = ctk.CTkScrollableFrame(self.file_list_frame, width=300, height=100)
        self.file_listbox.pack(fill="both", expand=True)

    
        self.file_buttons = []
        for file in self.get_txt_files():

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

        # Main frame (File content, Image display, Automata table)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=5)  

        # Left column: File content display
        self.textbox = ctk.CTkTextbox(self.main_frame, height=150, wrap="word", font=("Courier", 16))
        self.textbox.pack(side="left", fill="both", expand=True, padx=10, pady=5)

        # Middle column: Automata image display
        self.image_frame = ctk.CTkFrame(self.main_frame)
        self.image_frame.pack(side="left", padx=10, pady=5, fill="both", expand=True)
        self.image_label = ctk.CTkLabel(self.image_frame, text="(No image)")
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
        self.button_frame.pack(pady=5, fill="x", padx=20)  

        # Word recognition frame
        self.word_frame = ctk.CTkFrame(self.button_frame)
        self.word_frame.pack(side="left", expand=True, fill="x", padx=5, pady=5)
        
        self.word_label = ctk.CTkLabel(self.word_frame, text="Test word:", font=("Arial", 12))
        self.word_label.pack(side="left", padx=5)
        
        self.word_entry = ctk.CTkEntry(self.word_frame, width=100)
        self.word_entry.pack(side="left", padx=(5, 2))  
        
        self.test_button = ctk.CTkButton(self.word_frame, text="🔍 Test", command=self.test_word)
        self.test_button.pack(side="left", padx=(0, 5))
        
        
        self.word_frame.configure(fg_color="transparent")
        
 
        self.word_input_frame = ctk.CTkFrame(self.word_frame)
        self.word_input_frame.pack(side="left", pady=5)
        
    
        self.word_entry.pack_forget()
        self.test_button.pack_forget()
        
        self.word_entry = ctk.CTkEntry(self.word_input_frame, width=100)
        self.word_entry.pack(side="left", padx=(5, 2))
        
        self.test_button = ctk.CTkButton(self.word_input_frame, text="🔍 Test", command=self.test_word)
        self.test_button.pack(side="left", padx=(2, 5))

        self.determinize_button = ctk.CTkButton(self.button_frame, text="⚙ Determinize", command=self.determinize)
        self.determinize_button.pack(side="left", expand=True, padx=5, pady=5)
        
        self.standardize_button = ctk.CTkButton(self.button_frame, text="📐 Standardize", command=self.standardize)
        self.standardize_button.pack(side="left", expand=True, padx=5, pady=5)
        
        self.minimize_button = ctk.CTkButton(self.button_frame, text="🔧 Minimize", command=self.minimize)
        self.minimize_button.pack(side="right", expand=True, padx=5, pady=5)

        self.complement_button = ctk.CTkButton(self.button_frame, text="🔄 Complementary", command=self.complementary)
        self.complement_button.pack(side="right", expand=True, padx=5, pady=5)

        
        self.check_frame = ctk.CTkFrame(self)
        self.check_frame.pack(pady=5, fill="x", padx=20)

        self.check_label = ctk.CTkLabel(self.check_frame, text="Verifications:", font=("Arial", 14, "bold"))
        self.check_label.pack(side="left", padx=(5, 15))

       
        self.check_deterministic = ctk.CTkButton(self.check_frame, text="🔍 Is it deterministic?", 
                                                command=self.check_is_deterministic)
        self.check_deterministic.pack(side="left", expand=True, padx=5, pady=5)

        self.check_complete = ctk.CTkButton(self.check_frame, text="🔍 Is it a CDFA?", 
                                        command=self.check_is_complete_dfa)
        self.check_complete.pack(side="left", expand=True, padx=5, pady=5)

        self.check_standard = ctk.CTkButton(self.check_frame, text="🔍 Is it standardized?", 
                                        command=self.check_is_standard)
        self.check_standard.pack(side="left", expand=True, padx=5, pady=5)

      
        self.result_label = ctk.CTkLabel(self, text="Results:", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=5)

        
        self.result_textbox = ctk.CTkTextbox(self, height=300, wrap="word", font=("Courier", 14))
        self.result_textbox.pack(pady=5, fill="both", expand=True, padx=20)
        
        self.selected_file = None  
        
    def center_window(self, padding_percent=10):
        """Center the window with a percentage-based padding"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()

      
        x_padding = 0
        y_padding = 0

     
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
        
       
        def get_file_number(filename):
            try:
           
                return int(filename.split('_')[1].split('.')[0])
            except (IndexError, ValueError):
                return float('inf')
        
        files.sort(key=get_file_number)
        return files

    def on_file_selected(self, selected_file):
        """Load the selected file, display its content, associated image, and automata table"""
        if selected_file:
           
            selected_display_name = os.path.splitext(selected_file)[0]
            for button in self.file_buttons:
                if button.cget("text") == selected_display_name:
                    button.configure(fg_color=("gray75", "gray25"))
                else:
                    button.configure(fg_color="transparent")
                    
            self.selected_file = os.path.join(AUTOMATA_TXT_DIR, selected_file)
            self.display_file_content(self.selected_file)
            
          
            self.update_idletasks()
            self.display_automata_image(selected_file)
            
          
            try:
                A = Automata.from_file(self.selected_file)
                table_output = self.capture_stdout(A.printCDFA)
                self.table_textbox.delete("1.0", "end")
                self.table_textbox.insert("1.0", table_output)
            except Exception as e:
                self.table_textbox.delete("1.0", "end")
                self.table_textbox.insert("1.0", f"Error: {str(e)}")

    def display_file_content(self, file_path):
        """Display the content of the selected file"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.textbox.delete("1.0", "end")
            self.textbox.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Unable to read the file: {str(e)}")

    def display_automata_image(self, txt_filename):
        """Resize and display the automaton image to fill the entire frame while keeping proportions"""
        
        # Check if this is a complementary automata file
        is_complement = "_complement" in txt_filename
        
        if is_complement:
            
            self.photo = None
            self.image_label.configure(
                image=None, 
                text="[Complementary Automaton]\n\nNo image available for\ncomplementary automata",
                font=("Arial", 16, "bold")
            )
           
            self.image_label.image = None
            return
                
       
        image_path = os.path.join(DEFAULT_DIRECTORY, "Automata_img", txt_filename.replace(".txt", ".png"))

        if os.path.exists(image_path):
            img = Image.open(image_path)
            
          
            frame_width = self.image_frame.winfo_width()
            frame_height = self.image_frame.winfo_height()
            
            # Define maximum dimensions
            MAX_WIDTH = 600
            MAX_HEIGHT = 500
            
            # Calculate dimensions that respect both aspect ratio and maximum size
            img_width, img_height = img.size
            width_ratio = MAX_WIDTH / img_width if img_width > MAX_WIDTH else 1
            height_ratio = MAX_HEIGHT / img_height if img_height > MAX_HEIGHT else 1
            
            # Use the smaller ratio to ensure the image fits within both constraints
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
            self.image_label.configure(image=None, text=f"(Image not found at {image_path})")
            print(f"Image not found: {image_path}")

    def capture_stdout(self, func, *args):
        """Capture the output of printCDFA() and return it as text"""
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        try:
            func(*args)
        except Exception as e:
            sys.stdout = sys.__stdout__
            return f"❌ Error: {str(e)}"
        sys.stdout = sys.__stdout__
        result = output_buffer.getvalue()
        output_buffer.close()
        return result

    def test_word(self):
        """Test if a word is recognized by the automaton"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        word = self.word_entry.get().strip()
        if not word:
            messagebox.showerror("Error", "Please enter a word to test.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"🔍 Testing the word '{word}'...\n")

        try:
            A = Automata.from_file(self.selected_file)
            
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            
            result = A.recognize_word(word)
            
            sys.stdout = sys.__stdout__
            debug_output = output_buffer.getvalue()
            output_buffer.close()
            
          
            if result:
                self.result_textbox.insert("end", f"\n✅ The word '{word}' is recognized by the automaton.\n")
            else:
                self.result_textbox.insert("end", f"\n❌ The word '{word}' is NOT recognized by the automaton.\n")
            
            
            if debug_output:
                self.result_textbox.insert("end", f"\n🔧 Execution details:\n{debug_output}")
                
        except Exception as e:
            sys.stdout = sys.__stdout__  
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Error: {str(e)}")

    def determinize(self):
        """Perform determinization and display the result"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"📌 Loading the automaton from {self.selected_file}...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            result = self.capture_stdout(A2.printCDFA)
            self.result_textbox.insert("end", "\n✔ After complete determinization:\n" + result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def minimize(self):
        """Perform minimization and display the result"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"🔧 Minimization in progress...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            A2 = A1.determinize_complete()
            A3 = A2.minimization()
            result = self.capture_stdout(A3.printCDFA)
            self.result_textbox.insert("end", "\n✔ After minimization:\n" + result)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def standardize(self):
        """Perform standardization and display the result"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"📐 Standardization in progress...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            
            # Check if already standardized
            if A1.is_standard():
                self.result_textbox.insert("end", "\n✅ The automaton is already standardized.\n")
                result = self.capture_stdout(A1.printCDFA)
                self.result_textbox.insert("end", "\nStandardized automaton:\n" + result)
                return
                
            # Standardize the automaton
            A1.standardize()
            result = self.capture_stdout(A1.printCDFA)
            self.result_textbox.insert("end", "\n✅ After standardization:\n" + result)
        except Exception as e:
            sys.stdout = sys.__stdout__  # Ensure stdout is reset
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Error: {str(e)}")

    def complementary(self):
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return

        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", f"🔄 Creating the complementary automaton...\n")

        try:
            A1 = Automata.from_file(self.selected_file)
            complementary = A1.complementary_automata()
            result = self.capture_stdout(complementary.printCDFA)
            self.result_textbox.insert("end", "\n✅ Complementary automaton created:\n" + result)
            
         
            if messagebox.askyesno("Save", "Do you want to save the complementary automaton to a file?"):
           
                base_filename = os.path.basename(self.selected_file)
                name_without_ext = os.path.splitext(base_filename)[0]
                save_path = os.path.join(AUTOMATA_TXT_DIR, f"{name_without_ext}_complement.txt")
                
                complementary.to_file(save_path)
                self.result_textbox.insert("end", f"\n💾 Complementary automaton saved as: {save_path}\n")
                
              
                self.created_complement_files.append(save_path)
                
                self.refresh_file_list()
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Error: {str(e)}")

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
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "🔍 Checking if the automaton is deterministic...\n")
        
        try:
            A = Automata.from_file(self.selected_file)
            result = A.is_deterministic()
            
            if result == DETERMINISTIC:
                self.result_textbox.insert("end", "✅ The automaton is DETERMINISTIC.\n")
            elif result == NOT_DETERM_INPUT:
                self.result_textbox.insert("end", "❌ The automaton is NOT deterministic:\n")
                self.result_textbox.insert("end", "   → The automaton must have exactly one initial state.\n")
            else:  # result == NOT_DETERM_TRANSITIONS
                self.result_textbox.insert("end", "❌ The automaton is NOT deterministic:\n")
                self.result_textbox.insert("end", "   → A transition has multiple destinations for the same letter.\n")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Error: {str(e)}")

    def check_is_complete_dfa(self):
        """Check if the automaton is a complete deterministic finite automaton"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "🔍 Checking if the automaton is a CDFA...\n")
        
        try:
            A = Automata.from_file(self.selected_file)
            
            # Capture any potential output from the function
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            
            result = A.is_complete_DFA(False)
            
            sys.stdout = sys.__stdout__
            debug_output = output_buffer.getvalue()
            output_buffer.close()
            
            if result == CDFA:
                self.result_textbox.insert("end", "✅ The automaton is a COMPLETE DETERMINISTIC FINITE AUTOMATON.\n")
            elif result == NOT_DETERM_INPUT:
                self.result_textbox.insert("end", "❌ The automaton is NOT a CDFA:\n")
                self.result_textbox.insert("end", "   → The automaton must have exactly one initial state.\n")
            elif result == NOT_DETERM_TRANSITIONS:
                self.result_textbox.insert("end", "❌ The automaton is NOT a CDFA:\n")
                self.result_textbox.insert("end", "   → A transition has multiple destinations for the same letter.\n")
            elif result == DETER_NOT_COMPLETE:
                self.result_textbox.insert("end", "❌ The automaton is NOT a CDFA:\n")
                self.result_textbox.insert("end", "   → The automaton is deterministic but not complete.\n")
            
            # Add any debug details if available
            if debug_output:
                self.result_textbox.insert("end", f"\n🔧 Details:\n{debug_output}")
        
        except Exception as e:
            sys.stdout = sys.__stdout__  # Ensure stdout is restored
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Error: {str(e)}")

    def check_is_standard(self):
        """Check if the automaton is standardized"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a file first.")
            return
        
        self.result_textbox.delete("1.0", "end")
        self.result_textbox.insert("1.0", "🔍 Checking if the automaton is standardized...\n")
        
        try:
            A = Automata.from_file(self.selected_file)
            result = A.is_standard()
            
            if result:
                self.result_textbox.insert("end", "✅ The automaton is STANDARD.\n")
            else:
                self.result_textbox.insert("end", "❌ The automaton is NOT standardized.\n")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.result_textbox.insert("end", f"\n❌ Error: {str(e)}")
    
    def on_closing(self):
        """Handle the window closing event by deleting created complementary files"""
        if self.created_complement_files:
            if messagebox.askyesno("Confirmation", 
                                  f"Do you want to delete the {len(self.created_complement_files)} complementary automaton file(s) created during this session?"):
                files_deleted = 0
                for file_path in self.created_complement_files:
                    try:
                        if os.path.exists(file_path):
                            os.remove(file_path)
                            files_deleted += 1
                    except Exception as e:
                        print(f"Error deleting {file_path}: {str(e)}")
                
                print(f"{files_deleted} complementary automaton file(s) deleted.")
        
        self.destroy()


def main():
    """Main function to choose the interface mode"""
    print("=== AUTOMATA PROJECT ===")
    print("1. Text mode (CLI)")
    print("2. Graphical mode (GUI)")
    
    while True:
        choice = input("\nChoose the interface mode (1 or 2): ")
        
        if choice == '1':
            text_menu = AutomataTextMenu()
            text_menu.run()
            break
        elif choice == '2':
            app = AutomataApp()
            app.mainloop()
            break
        else:
            print("❌ Invalid option, please choose 1 or 2.")


if __name__ == "__main__":
    main()
