<img width="2879" height="1799" alt="Screenshot 2026-01-20 145807" src="https://github.com/user-attachments/assets/e77e84f9-6c33-434f-b31a-5c11b76e986f" /># Smart Folder Cleaner

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

## **First User Interface**
<img width="1399" height="1154" alt="Screenshot 2026-01-20 145110" src="https://github.com/user-attachments/assets/ac15bf41-29de-42c6-a047-2e963a073082" />

## **Before Organise Files**
<img width="1795" height="1164" alt="Screenshot 2026-01-20 145441" src="https://github.com/user-attachments/assets/51004de5-c422-4730-9b08-bb33048032e4" />

## **Select Folder**
<img width="1395" height="484" alt="Screenshot 2026-01-20 145519" src="https://github.com/user-attachments/assets/3fcc3491-b4f2-4adb-9703-e4e6e27d4c33" />

## **Successful Complete**
<img width="1386" height="1103" alt="Screenshot 2026-01-20 145533" src="https://github.com/user-attachments/assets/371d70af-6277-404a-a6b5-df559dae638f" />

<img width="1382" height="1135" alt="Screenshot 2026-01-20 145548" src="https://github.com/user-attachments/assets/96f4c04a-f453-4e1f-b806-e14488810ec8" />

## **After Organise Files**
<img width="1943" height="1226" alt="Screenshot 2026-01-20 145611" src="https://github.com/user-attachments/assets/147fe053-6999-4efd-aedb-659a1b52d289" />

## **Code**
<img width="2879" height="1799" alt="Screenshot 2026-01-20 145807" src="https://github.com/user-attachments/assets/e770c2a0-2c7d-462f-8a35-f959d3be1f38" />




