import cv2
import numpy as np
import os
import pytesseract
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *


# Get the current working directory
current_folder = os.getcwd()

# Set Tesseract path explicitly
os.environ['TESSDATA_PREFIX'] = os.path.join(current_folder, "Tesseract-OCR", "tessdata")

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = os.path.join(current_folder, "Tesseract-OCR", "tesseract.exe")

def check_tesseract_installation():
    try:
        pytesseract.get_tesseract_version()
    except pytesseract.TesseractNotFoundError:
        messagebox.showinfo("Error", "Tesseract is not installed. Please check the readme file for installation instructions.")
        return False
    return True


# Function to create 'data_collection' folder if it doesn't exist
def create_data_collection_folder():
    if not os.path.exists('data_collection'):
        os.makedirs('data_collection')
        
# Function to open the 'data_collection' folder
def open_data_folder():
    folder_path = 'data_collection'
    if os.path.exists(folder_path):
        os.system(f'explorer {os.path.realpath(folder_path)}')
    else:
        print("The 'data_collection' folder doesn't exist.")

# Function to perform OCR on selected image
def perform_ocr():
    if not check_tesseract_installation():
        return
    try :
        create_data_collection_folder()
        file_path = filedialog.askopenfilename()
        
        # Check if the selected file exists in the 'data_collection' folder
        if os.path.exists(os.path.join('data_collection', os.path.basename(file_path))):
            messagebox.showinfo("Image Exists", "The image exists in the data folder. You need to delete data before uploading again.")
            return
            
        if file_path:
            
            # Save the image to the 'data_collection' folder
            save_path = os.path.join('data_collection', os.path.basename(file_path))
            image = cv2.imread(file_path)
            cv2.imwrite(save_path, image)
    
            # Perform OCR on the saved image(s)
            extracted_text = extract_text_from_images()
            
            # Display the extracted text in the text box
            text_box.delete(1.0, END)
            text_box.insert(END, extracted_text)
    
            # Display the folder weight
            folder_weight_label.config(text=f"Folder Weight: {get_folder_weight('data_collection')} MB")
    except:
        messagebox.showinfo("Error", "Failed to load the image. Please select a valid image file. Ensure that the file exists and try changing the image name.")

# Function to extract text from images in 'data_collection' folder
def extract_text_from_images():
    if not check_tesseract_installation():
        return
    text = ''
    data_collection_path = 'data_collection'
    for file_name in os.listdir(data_collection_path):
        file_path = os.path.join(data_collection_path, file_name)
        img = cv2.imread(file_path)
        text += pytesseract.image_to_string(img, lang='eng') + '\n'
    return text

# Function to get the folder weight in MB
def get_folder_weight(folder_path):
    create_data_collection_folder()
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return round(total_size / (1024 * 1024), 2)  # Convert bytes to MB

# Function to clear the extracted text
def clear_extracted_text():
    text_box.delete(1.0, "end")  # Clear text from the Text widget

# Function to delete all contents in the 'data_collection' folder
def delete_data_collection():
    folder_path = 'data_collection'
    create_data_collection_folder()
    for file_name in os.listdir('data_collection'):
        file_path = os.path.join('data_collection', file_name)
        os.remove(file_path)
    folder_weight_label.config(text="Folder Weight: 0 MB")
    # Clear extracted text
    clear_extracted_text()

# Create the GUI
root = Tk()
root.title("Image OCR by Atef")
icon_path=os.path.join(current_folder, 'icon.ico')
root.iconbitmap(icon_path)
root.configure(bg="#e9f5f9")

# Configure colors and fonts
button_color = "#2596be"
button_text_color = "white"
button_font = ("Arial", 12)

label_font = ("Arial", 10)

# Upload button
upload_button = Button(root, text="Upload Image", command=perform_ocr, bg=button_color, fg=button_text_color, font=button_font)
upload_button.pack(pady=10)

# Create a frame to contain Text
text_frame = Frame(root)
text_frame.pack(expand=True, fill='both')
text_frame.configure(bg="#2596be")


# Text box for displaying extracted text
text_box = Text(text_frame, font=("Arial", 12), wrap='word', height=20, width=50, relief='solid', highlightbackground="#cfe2f3")
text_box.pack(expand=True, fill='both', padx=10, pady=10)

# Folder weight label
folder_weight_label = Label(root, text=f"Folder Weight: {get_folder_weight('data_collection')} MB", font=label_font,background="#cfe2f3")
folder_weight_label.pack()

# Delete button
delete_button = Button(root, text="Delete Data", command=delete_data_collection, bg=button_color, fg=button_text_color, font=button_font)
delete_button.pack(pady=10)

# Open folder button
open_folder_button = Button(root, text="Open Data Folder", command=open_data_folder, bg=button_color, fg=button_text_color, font=button_font)
open_folder_button.pack(pady=10)

root.mainloop()