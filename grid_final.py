#!/usr/bin/env python
# coding: utf-8

# In[4]:


import cv2
import tkinter as tk
from tkinter import filedialog, colorchooser
from PIL import Image, ImageTk
import numpy as np

# Initialize variables
rois = {}  # Dictionary to store ROI names and their respective grids
roi_colors = {}  # Dictionary to store color mappings for each ROI
image = None  # Image loaded from file
output_filename = ""  # Name of the output text file
current_roi_name = None
selected_grids = set()  # Set to store selected grids

# Grid settings
grid_size = 15
grid_color = (255, 0, 0)

# Callback function for mouse events
def start_drawing(event):
    global drawing
    drawing = True
    draw_roi(event)

def stop_drawing(event):
    global drawing
    drawing = False

def draw_roi(event):
    if current_roi_name and drawing:
        x, y = event.x, event.y
        x //= grid_size
        y //= grid_size
        if (x, y) not in selected_grids:
            rois.setdefault(current_roi_name, []).append((x, y))
            selected_grids.add((x, y))
            canvas.create_rectangle(x * grid_size, y * grid_size, (x + 1) * grid_size, (y + 1) * grid_size, fill=roi_colors.get(current_roi_name, grid_color), stipple='gray50')

def start_roi():
    global current_roi_name, selected_grids
    roi_name = roi_name_entry.get()
    if roi_name:
        current_roi_name = roi_name
        roi_name_entry.config(state=tk.DISABLED)  # Disable the Entry while defining ROIs
        color = colorchooser.askcolor()[1]  # Ask the user to choose a color for this ROI
        roi_colors[current_roi_name] = color
        selected_grids = set()

def erase_grid(event):
    if current_roi_name and drawing:
        x, y = event.x, event.y
        x //= grid_size
        y //= grid_size
        if (x, y) in selected_grids:
            selected_grids.remove((x, y))
            canvas.create_rectangle(x * grid_size, y * grid_size, (x + 1) * grid_size, (y + 1) * grid_size, fill="white")

def save_roi():
    global current_roi_name
    if current_roi_name:
        rois[current_roi_name] = rois.get(current_roi_name, [])
        roi_name_entry.config(state=tk.NORMAL)  # Re-enable the Entry for the next ROI
        roi_name_entry.delete(0, 'end')

def finish_roi():
    save_roi()  # Save the current ROI
    with open(output_filename, 'w') as file:
        file.write('{')
        for roi_name, grid_list in rois.items():
            file.write(f'"{roi_name}" : [')
            for x, y in grid_list:
                if (x, y) == grid_list[-1]:
                    file.write(f'({x}, {y})')
                else:
                    file.write(f'({x}, {y}), ')
            file.write(f'],\n')
        file.write('"end":[(9999,99999)]}')
    root.destroy()

# Create the main window
root = tk.Toplevel()
root.title("ROI Definition Tool")

# Load the image
image_path = filedialog.askopenfilename()
if image_path:
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_pil = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image_pil)

    # Create a Frame to display the image
    image_frame = tk.Frame(root)
    image_frame.grid(row=0, column=0, columnspan=2)
    canvas = tk.Canvas(image_frame, width=image.shape[1], height=image.shape[0])
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)

    # Create an Entry for ROI name
    roi_name_label = tk.Label(root, text="Enter ROI Name:")
    roi_name_entry = tk.Entry(root)
    roi_name_entry.config(state=tk.NORMAL)  # Entry starts as enabled
    start_roi_button = tk.Button(root, text="Start ROI", command=start_roi)
    save_button = tk.Button(root, text="Save ROI", command=save_roi)
    finish_button = tk.Button(root, text="Finish ROI", command=finish_roi)
    output_filename = f"{image_path.split('/')[-1].split('.')[0]}_ROI.txt"  # Generate the output filename

    # Layout management
    roi_name_label.grid(row=1, column=0, padx=10, pady=10)
    roi_name_entry.grid(row=1, column=1, padx=10, pady=10)
    start_roi_button.grid(row=2, column=0, padx=10, pady=10)
    save_button.grid(row=2, column=1, padx=10, pady=10)
    finish_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    canvas.bind("<Button-1>", start_drawing)
    canvas.bind("<B1-Motion>", draw_roi)
    canvas.bind("<Button-3>", erase_grid)
    canvas.bind("<ButtonRelease-1>", stop_drawing)
    root.mainloop()


# In[ ]:




