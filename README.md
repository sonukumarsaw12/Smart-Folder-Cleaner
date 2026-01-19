# Smart Folder Cleaner

## 1. The Problem
In our daily digital lives, download folders and desktops often become cluttered with a chaotic mix of file types—images, documents, installers, and archives. Organizing these manually is tedious, time-consuming, and repetitive. This clutter makes it difficult to find important files and reduces productivity. **Smart Folder Cleaner** automates this process, instantly restoring order to any chosen directory.

## 2. How to Run

### Prerequisites
- Python 3.x installed
- `pip` package manager

### Installation
1.  Open your terminal or command prompt.
2.  Navigate to the project directory:
    ```bash
    cd "path/to/Smart Folder Cleaner"
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application
1.  Execute the main script:
    ```bash
    python folder_cleaner_gui.py
    ```
2.  The graphical interface will appear.
3.  Click **Browse** to select the chaotic folder you wish to clean.
4.  Click **Start Cleaning** and watch the logs as your files are instantly organized into categories (Images, Documents, etc.).

## 3. Design Decisions

### **User Interface (GUI)**
I chose **CustomTkinter** for the interface to provide a modern, clean, and user-friendly experience (dark/light mode support) compared to the standard Tkinter look. The layout is simple: Top-down flow from selection to action to feedback.

### **Categorization Logic**
The core logic uses a dictionary mapping file extensions to categories. This is scalable; adding a new file type is as simple as adding an entry to the `FILE_CATEGORIES` dictionary.

### **File Safety**
To prevent data loss, I implemented a `get_unique_filename` method. If a file with the same name already exists in the destination folder, the program automatically appends a counter (e.g., `file_1.txt`) instead of overwriting the existing file.

### **Concurrency**
The cleaning process runs on a separate **Daemon Thread**. This ensures that the GUI remains responsive (does not freeze) while the file operations are being performed, adhering to best practices for desktop applications.
