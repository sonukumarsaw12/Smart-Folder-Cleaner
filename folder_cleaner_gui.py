import os
import shutil
import threading
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox

# ---------------- CONFIGURATION ---------------- #

ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".ppt", ".xlsx", ".xls", ".csv", ".md", ".json"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z", ".iso"],
    "Programs": [".exe", ".msi", ".bat", ".sh", ".apk"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css", ".php", ".rb", ".go", ".ts"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
}

# ---------------- BACKEND LOGIC ---------------- #

class FileOrganizer:
    def __init__(self, log_callback, progress_callback):
        self.log = log_callback
        self.progress = progress_callback
        self.running = False

    def get_category(self, extension):
        for category, extensions in FILE_CATEGORIES.items():
            if extension in extensions:
                return category
        return "Others"

    def get_unique_filename(self, target_path, filename):
        """
        If a file exists at target_path/filename, returns a new name like filename_1.ext
        """
        base_name, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        
        while os.path.exists(os.path.join(target_path, new_filename)):
            new_filename = f"{base_name}_{counter}{ext}"
            counter += 1
            
        return new_filename

    def start_cleaning(self, folder_path):
        self.running = True
        if not os.path.isdir(folder_path):
            self.log("❌ Error: Invalid directory selected.")
            return

        self.log(f"📂 Scanning: {folder_path}...")
        
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        except Exception as e:
            self.log(f"❌ Error accessing directory: {e}")
            return

        total_files = len(files)
        if total_files == 0:
            self.log("⚠️ No files found to clean.")
            self.progress(1.0) # Complete
            return

        self.log(f"ℹ️ Found {total_files} files. Starting organization...")
        
        moved_count = 0
        errors = 0

        for i, file in enumerate(files):
            if not self.running:
                self.log("🛑 Operation stopped by user.")
                break

            full_path = os.path.join(folder_path, file)
            _, ext = os.path.splitext(file)
            category = self.get_category(ext.lower())

            category_path = os.path.join(folder_path, category)
            
            try:
                os.makedirs(category_path, exist_ok=True)
                
                # Handle duplicate names safely
                new_filename = self.get_unique_filename(category_path, file)
                new_full_path = os.path.join(category_path, new_filename)
                
                shutil.move(full_path, new_full_path)
                
                # Logging
                if file != new_filename:
                    self.log(f"✅ Moved (renamed): {file} → {category}/{new_filename}")
                else:
                    self.log(f"✅ Moved: {file} → {category}")
                    
                moved_count += 1
                
            except Exception as e:
                self.log(f"❌ Error moving {file}: {e}")
                errors += 1

            # Update progress
            progress_val = (i + 1) / total_files
            self.progress(progress_val)
            
            # Small delay for visual smoothness (optional, can be removed for speed)
            # time.sleep(0.02) 

        self.log("-" * 40)
        self.log(f"🎉 Completed! Moved: {moved_count}, Errors: {errors}")
        self.running = False


# ---------------- GUI CLASS ---------------- #

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Folder Cleaner")
        self.geometry("700x550")
        self.resizable(False, False)

        self.organizer = None
        self.thread = None

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # 1. Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Smart Folder Cleaner", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(pady=20)

        # 2. Folder Selection
        self.select_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.select_frame.pack(fill="x", padx=20, pady=10)

        self.folder_path_var = ctk.StringVar()
        self.folder_entry = ctk.CTkEntry(
            self.select_frame, 
            textvariable=self.folder_path_var, 
            width=450,
            placeholder_text="Select a folder to clean..."
        )
        self.folder_entry.pack(side="left", padx=(0, 10))

        self.browse_btn = ctk.CTkButton(
            self.select_frame, 
            text="Browse", 
            command=self.browse_folder,
            width=100
        )
        self.browse_btn.pack(side="left")

        # 3. Action Area
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=20, pady=10)

        self.clean_btn = ctk.CTkButton(
            self.action_frame, 
            text="Start Cleaning", 
            command=self.start_thread,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            fg_color="#2CC985", 
            hover_color="#229A65"
        )
        self.clean_btn.pack(fill="x")

        # 4. Progress Bar
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(fill="x", padx=20, pady=(10, 5))
        self.progress_bar.set(0)

        # 5. Log Area
        self.log_label = ctk.CTkLabel(self, text="Activity Log:", anchor="w")
        self.log_label.pack(fill="x", padx=25, pady=(5, 0))

        self.log_box = ctk.CTkTextbox(self, height=200, activate_scrollbars=True)
        self.log_box.pack(fill="both", padx=20, pady=(5, 20), expand=True)
        self.log_box.configure(state="disabled")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path_var.set(folder)

    def log_message(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def update_progress(self, value):
        self.progress_bar.set(value)

    def start_thread(self):
        path = self.folder_path_var.get()
        if not path:
            self.log_message("⚠️ Please select a folder first.")
            return

        # Disable button while running
        self.clean_btn.configure(state="disabled", text="Cleaning...")
        self.progress_bar.set(0)
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        
        self.organizer = FileOrganizer(self.log_message, self.update_progress)
        
        # Start background thread
        self.thread = threading.Thread(target=self.run_cleaning, args=(path,))
        self.thread.daemon = True
        self.thread.start()

    def run_cleaning(self, path):
        self.organizer.start_cleaning(path)
        # Re-enable button on main thread (ctk usually handles this okay, or use after)
        self.after(100, self.cleaning_finished)

    def cleaning_finished(self):
        self.clean_btn.configure(state="normal", text="Start Cleaning")
        messagebox.showinfo("Done", "Folder cleaning completed successfully!")

if __name__ == "__main__":
    app = App()
    app.mainloop()
