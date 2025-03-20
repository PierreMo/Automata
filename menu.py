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

# Default directory for .txt and .png files
DEFAULT_DIRECTORY = os.getcwd()


class AutomataApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automata Project")
        self.geometry("900x700")  # Larger size for better image display
        self.center_window(padding_percent=10)

        # Title
        self.label_title = ctk.CTkLabel(self, text="AUTOMATA PROJECT", font=("Helvetica", 24, "bold"))
        self.label_title.pack(pady=10)

        # Top frame (File selection)
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(fill="x", padx=20, pady=10)

        # File selection dropdown
        self.file_label = ctk.CTkLabel(self.top_frame, text="Sélectionnez un fichier :", font=("Arial", 14))
        self.file_label.pack(side="left", padx=10, pady=5)

        self.file_dropdown = ctk.CTkComboBox(
            self.top_frame, values=self.get_txt_files(), command=self.on_file_selected
        )
        self.file_dropdown.pack(side="right", padx=10, pady=5)

        # Main frame (File content, Image display, Automata table)
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

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
        self.button_frame.pack(pady=10, fill="x", padx=20)

        self.determinize_button = ctk.CTkButton(self.button_frame, text="⚙ Déterminiser", command=self.determinize)
        self.determinize_button.pack(side="left", expand=True, padx=5, pady=5)

        self.minimize_button = ctk.CTkButton(self.button_frame, text="🔧 Minimiser", command=self.minimize)
        self.minimize_button.pack(side="right", expand=True, padx=5, pady=5)

        # Results display
        self.result_label = ctk.CTkLabel(self, text="Résultats :", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=5)

        self.result_textbox = ctk.CTkTextbox(self, height=200, wrap="word", font=("Courier", 14))
        self.result_textbox.pack(pady=5, fill="both", padx=20)

        self.selected_file = None  # Stores selected file

    def center_window(self, padding_percent=10):
        """Center the window with a percentage-based padding"""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()

        # Calculate padding in pixels
        x_padding = int(screen_width * (padding_percent / 100))
        y_padding = int(screen_height * (padding_percent / 100))

        # Centered position with padding
        x_position = (screen_width - window_width) // 2 - x_padding
        y_position = (screen_height - window_height) // 2 - y_padding

        self.geometry(f"+{x_position}+{y_position}")

    def get_txt_files(self):
        """List available .txt files in the directory"""
        return [f for f in os.listdir(DEFAULT_DIRECTORY) if f.endswith(".txt")]

    def on_file_selected(self, selected_file):
        """Load the selected file, display its content, associated image, and automata table"""
        if selected_file:
            self.selected_file = os.path.join(DEFAULT_DIRECTORY, selected_file)
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


if __name__ == "__main__":
    app = AutomataApp()
    app.mainloop()