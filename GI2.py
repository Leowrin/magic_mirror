#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 15:48:15 2024

@author: oozi
"""

# %% import
import tkinter as tk
from PIL import Image, ImageTk
import os
import request_transport as rt
import datetime 
import time
import schedule


scriptdir = os.path.dirname(__file__)


# %% 
def refresh_window():
    # Redraw the windows
    trains = rt.request_trains(rt.trainstation_request())
    buses = rt.request_buses(rt.busstop_request())
    create_train_grid(root, trains)
    create_bus_grid(bus_window, buses)
    root.update_idletasks()
    bus_window.update_idletasks()


# Function to create a grid for trains
def create_train_grid(root, trains):
    now = datetime.datetime.now().strftime('%H:%M')
    for r, row in enumerate(trains):
        for c, item in enumerate(row):
            if r==0 and (c==2 or c==4) :
                continue
            
            if isinstance(item, str):
                if item.startswith("img/"):
                    image_path = item
                    img = Image.open(os.path.join(scriptdir, image_path))
                    img = img.resize((118, 40))  # Resize the image to fit the cell
                    img = ImageTk.PhotoImage(img)

                    # Create a label for the image
                    label = tk.Label(root, image=img, bg="#2d327d", borderwidth=0, relief="solid")
                    label.image = img  # Keep a reference to the image to prevent garbage collection
                    label.grid(row=r, column=c, sticky="nsew")
                    
                elif item.startswith("IC1") :
                    image_path = "img/ic1.png"
                    img = Image.open(os.path.join(scriptdir, image_path))
                    img = img.resize((118, 40))  # Resize the image to fit the cell
                    img = ImageTk.PhotoImage(img)

                    # Create a label for the image
                    label = tk.Label(root, image=img, bg="#2d327d", borderwidth=1, relief="solid")
                    label.image = img  # Keep a reference to the image to prevent garbage collection
                    label.grid(row=r, column=c, sticky="nsew")
                
                elif item.startswith("IC5") :
                    image_path = "img/ic5.png"
                    img = Image.open(os.path.join(scriptdir, image_path))
                    img = img.resize((118, 40))  # Resize the image to fit the cell
                    img = ImageTk.PhotoImage(img)

                    # Create a label for the image
                    label = tk.Label(root, image=img, bg="#2d327d", borderwidth=1, relief="solid")
                    label.image = img  # Keep a reference to the image to prevent garbage collection
                    label.grid(row=r, column=c, sticky="nsew")
                
                elif item.startswith("IR90") :
                    image_path = "img/ir90.png"
                    img = Image.open(os.path.join(scriptdir, image_path))
                    img = img.resize((118, 40))  # Resize the image to fit the cell
                    img = ImageTk.PhotoImage(img)

                    # Create a label for the image
                    label = tk.Label(root, image=img, bg="#2d327d", borderwidth=1, relief="solid")
                    label.image = img  # Keep a reference to the image to prevent garbage collection
                    label.grid(row=r, column=c, sticky="nsew")
                    
                elif item.startswith("IR15") :
                    image_path = "img/ir15.png"
                    img = Image.open(os.path.join(scriptdir, image_path))
                    img = img.resize((118, 40))  # Resize the image to fit the cell
                    img = ImageTk.PhotoImage(img)

                    # Create a label for the image
                    label = tk.Label(root, image=img, bg="#2d327d", borderwidth=1, relief="solid")
                    label.image = img  # Keep a reference to the image to prevent garbage collection
                    label.grid(row=r, column=c, sticky="nsew")
                    
                elif item.startswith("SN") :
                    image_path = "img/sn.png"
                    img = Image.open(os.path.join(scriptdir, image_path))
                    img = img.resize((118, 40))  # Resize the image to fit the cell
                    img = ImageTk.PhotoImage(img)

                    # Create a label for the image
                    label = tk.Label(root, image=img, bg="#2d327d", borderwidth=1, relief="solid")
                    label.image = img  # Keep a reference to the image to prevent garbage collection
                    label.grid(row=r, column=c, sticky="nsew")
                    
                
                elif r == 0 and c == 1 :
                    font = ("Helvetica", 20, "bold")
                    fg_color = "white"
                    label = tk.Label(root, text="Lausanne - Départs", font=font, fg=fg_color, bg="#2d327d", borderwidth=0, relief="solid")
                    label.grid(row=r, column=c, columnspan=2, sticky="nsew")
                    
                elif r == 0 and c == 3 :
                    font = ("Helvetica", 20, "bold")
                    fg_color = "white"
                    label = tk.Label(root, text=now, font=font, fg=fg_color, bg="#2d327d", borderwidth=0, relief="solid")
                    label.grid(row=r, column=c, columnspan=2, sticky="nsew")
                    
                    
           
                else :
                    if r == 0:
                        font = ("Helvetica", 20, "bold")
                        fg_color = "white"
                    else:
                        font = ("Helvetica", 16)
                        fg_color = "white"

                        if item.startswith("IR") or item.startswith("IC"):
                            fg_color = "#EB0000"  
                            font = ("Helvetica", 18)
                        else:
                            font = ("Helvetica", 16)
                            fg_color = "white"

                    if c == 4 and r != 0:
                        fg_color = "#FFD32C"
                    
                    if c == 2 :
                        label = tk.Label(root, text=" "+item, font=font, fg=fg_color, bg="#2d327d", borderwidth=1, relief="solid", anchor="w")
                        label.grid(row=r, column=c, sticky="nsew")

                    else :
                        label = tk.Label(root, text=item, font=font, fg=fg_color, bg="#2d327d", borderwidth=1, relief="solid")
                        label.grid(row=r, column=c, sticky="nsew")

                

    # Configure rows and columns to expand
    for r in range(len(trains)):
        root.grid_rowconfigure(r, weight=1)
    for c in range(len(trains[0])):
        root.grid_columnconfigure(c, weight=1)




def create_bus_grid(window, buses):
    now = datetime.datetime.now().strftime('%H:%M')
    for r, row in enumerate(buses):
        for c, item in enumerate(row):
            
            if isinstance(item, str):
                font = ("Helvetica", 16)
                fg_color = "#2596be"  # Blue color code for bus text

                label = tk.Label(window, text=item, font=font, fg=fg_color, bg="white", borderwidth=1, relief="solid")
                label.grid(row=r, column=c, sticky="nsew")

    # Configure rows and columns to expand
    for r in range(len(buses)):
        window.grid_rowconfigure(r, weight=1)
    for c in range(len(buses[0])):
        window.grid_columnconfigure(c, weight=1)




# Initialize the main window for trains
root = tk.Tk()
root.title("Lausanne - Departs")
ws = root.winfo_screenwidth()  # width of the screen
hs = root.winfo_screenheight()  # height of the screen

root.geometry(str(f"{ws//3}x{hs}+0+0"))  # Set window size to one-third of the screen width and full height

# Initialize the second window for buses
bus_window = tk.Toplevel(root)
bus_window.title("Georgette")
bus_window.geometry(str(f"{ws//3}x{hs}+{ws//3}+0"))  # Set window size to one-third of the screen width and start from one-third

# Create frames for trains and buses


# Sample trains and buses: mix of text and image paths
trains = rt.request_trains(rt.trainstation_request())
buses = rt.request_buses(rt.busstop_request())

# Create grids
create_train_grid(root, trains)
create_bus_grid(bus_window, buses)
root.update_idletasks()
bus_window.update_idletasks()

# Run the application
schedule.every().minute.at(":01").do(refresh_window)

while True:
    schedule.run_pending()
    time.sleep(1)
