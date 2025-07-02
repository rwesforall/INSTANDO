#!/usr/bin/python

import sqlite3
import os.path
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk

version = "Version 0.0.1"
version1 = "0.0.1"
versiondate = "2025.07.02"
license = "test"

# Funktion zum Erstellen der Datenbank
# Diese Funktion überprüft, ob die Datenbankverzeichnisse und -dateien existieren
# Wenn nicht, werden sie erstellt und die entsprechenden Tabellen angelegt
def database():
    # Ensure the 'db' directory exists
    if not os.path.exists('db'):
        os.makedirs('db')

    if not os.path.exists('db/device.db'):
        conn = sqlite3.connect('db/device.db')
        conn.execute('''CREATE TABLE device
         (ID INTEGER PRIMARY KEY NOT NULL,
         name TEXT NOT NULL,
         manufacturer TEXT NOT NULL,
         serialnumber INT NOT NULL,
         typ TEXT NOT NULL,
         yearofmanufacture INT NOT NULL,
         internID INT NOT NULL,
         status TEXT NOT NULL,
         location TEXT NOT NULL,
         circuitdiagramm TEXT NOT NULL,
         technivaldrawing TEXT NOT NULL,
         manual TEXT NOT NULL,
         note TEXT NOT NULL,
         addressservice TEXT NOT NULL,
         addressmanufacture TEXT NOT NULL
         )
        ''')
        messagebox.showinfo("Datenbank", "Die Datenbank 'device.db' wurde erstellt.")
        conn.close()
    else:   
        messagebox  .showinfo("Datenbank", "Die Datenbank 'device.db' existiert bereits.")  

    if not os.path.exists('db/preventivemaintenance.db'):
        conn = sqlite3.connect('db/preventivemaintenance.db')
        conn.execute('''CREATE TABLE preventivemaintenance
            (ID INTEGER PRIMARY KEY NOT NULL,
            deviceID INTEGER NOT NULL,
            description TEXT NOT NULL,
            regulation TEXT NOT NULL,     
            planneddate DATE NOT NULL,
            completeddate DATE,
            status TEXT NOT NULL,
            interval INTEGER NOT NULL,
            maintenancemanual BLOB NOT NULL,
            maintenancestatusreport BLOB NOT NULL
            )
    ''')
        messagebox.showinfo("Datenbank", "Die Datenbank 'preventivemaintenance.db' wurde erstellt.")
        conn.close()
    else:
            messagebox.showinfo("Datenbank", "Die Datenbank 'preventivemaintenance.db' existiert bereits.") 
    


# GUI erstellen
# Hier wird das GUI mit Tkinter erstellt
root = tk.Tk()
root.title("INSTANDO - Instandhaltungsdatenbank")
root.geometry("1200x800")  # Fenstergröße anpassen
content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True)

# Funktion zum Löschen des Inhalts des Frames
# Diese Funktion wird verwendet, um den Inhalt des Frames zu löschen, wenn ein neues Fenster geöffnet wird  
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()



# Startfenster
# Hier wird das Startfenster erstellt, das beim Starten der Anwendung angezeigt wird
def start():
    clear_content()
    tk.Label(content_frame, text="Willkommen bei INSTANDO", font=("Arial", 25)).pack(pady=10)
    tk.Label(content_frame, text=version, font=("Arial", 12)).pack(pady=10)
    image = Image.open("img/logo.png")
    image = image.resize((150, 150))
    img = ImageTk.PhotoImage(image)
    label_img = tk.Label(content_frame, image=img)
    label_img.image = img
    label_img.pack(pady=10)
 



#info Fenster INSTANDO
def info():
    messagebox.showinfo("INSTANDO", "INSTANDO - Instandhaltungsdatenbank\n\n"
                                    "Erstellt von RWES\n\n"
                                    "Kontakt: https://github.com/rwesforall"
                                    "\n\n" + version + " vom "
                                    + versiondate + "\n"
                                    "Lizenz: " + license + "\n\n")




# Anlagen hinzufügen
def add_device():
 clear_content()
 tk.Label(content_frame, text="Anlage hinzufügen", font=("Arial", 25)).grid(row=0, column=0, sticky='n', pady=10)
 tk.Label(content_frame, text="Name", font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=10)
 tk.Label(content_frame, text="Hersteller", font=("Arial", 12)).grid(row=2, column=0, sticky='w', pady=10)
 tk.Label(content_frame, text="Seriennummer", font=("Arial", 12)).grid(row=3, column=0, sticky='w', pady=10)
 tk.Label(content_frame, text="Typ/Model", font=("Arial", 12)).grid(row=4, column=0, sticky='w', pady=10)
 tk.Label(content_frame, text="Baujahr", font=("Arial", 12)).grid(row=5, column=0, sticky='w', pady=10)
 tk.Label(content_frame, text="Interne ID", font=("Arial", 12)).grid(row=6, column=0, sticky='w', pady=10)
 tk.Label(content_frame, text="Status", font=("Arial", 12)).grid(row=1, column=4, sticky='s', pady=10)
 tk.Label(content_frame, text="Standort", font=("Arial", 12)).grid(row=2, column=4, sticky='', pady=10)
 tk.Label(content_frame, text="Schaltplan", font=("Arial", 12)).grid(row=3, column=4, sticky='', pady=10)
 tk.Label(content_frame, text="Technische Zeichnung", font=("Arial", 12)).grid(row=4, column=4, sticky='', pady=10)
 tk.Label(content_frame, text="Bedienungsanleitung", font=("Arial", 12)).grid(row=5, column=4, sticky='', pady=10)
 tk.Label(content_frame, text="Notizen", font=("Arial", 12)).grid(row=6, column=4, sticky='', pady=10)
 tk.Label(content_frame, text="Serviceadresse", font=("Arial", 12)).grid(row=7, column=0, sticky='W', pady=10)
 tk.Label(content_frame, text="Herstelleradresse", font=("Arial", 12)).grid(row=8, column=0, sticky='W', pady=10)  

 # Eingabefelder erstellen
 # Hier werden die Eingabefelder für die Datenbankeinträge erstellt  
 devicename = tk.Entry(content_frame, width=30)
 devicename.grid(row=1, column=1, pady=10, sticky='w')
 manufacturer = tk.Entry(content_frame, width=30)
 manufacturer.grid(row=2, column=1, pady=20, sticky='w')
 serialnumber = tk.Entry(content_frame, width=30)
 serialnumber.grid(row=3, column=1, pady=20, sticky='w')
 typ = tk.Entry(content_frame, width=30)
 typ.grid(row=4, column=1, pady=20, sticky='w')
 yearofmanufacture = tk.Entry(content_frame, width=30)
 yearofmanufacture.grid(row=5, column=1, pady=20, sticky='w')
 internID = tk.Entry(content_frame, width=30)
 internID.grid(row=6, column=1, pady=20, sticky='w')
 status = ttk.Combobox(content_frame, values=["vorhanden", "nicht mehr vorhanden"], width=27)
 status.grid(row=1, column=5, pady=20, sticky='w')
 location = tk.Entry(content_frame, width=30)
 location.grid(row=2, column=5, pady=20, sticky='w')
 circuitdiagramm = tk.Entry(content_frame, width=30)
 circuitdiagramm.grid(row=3, column=5, pady=20, sticky=' w')
 technivaldrawing = tk.Entry(content_frame, width=30)                             
 technivaldrawing.grid(row=4, column=5, pady=20, sticky='w')
 manual = tk.Entry(content_frame, width=30)
 manual.grid(row=5, column=5, pady=20, sticky='w')
 note = tk.Entry(content_frame, width=30)
 note.grid(row=6, column=5, pady=20, sticky='w')
 addressservice = tk.Entry(content_frame, width=50)
 addressservice.grid(row=7, column=1, pady=20, sticky='w')
 addressmanufacture = tk.Entry(content_frame, width=50)
 addressmanufacture.grid(row=8, column=1 , pady=20, sticky='w')   


 # Button zum Speichern der Daten
 # Funktion zum Speichern der Daten in die Datenbank
 def save_device():
    conn = sqlite3.connect('db/device.db')
    cursor = conn.cursor()
    
    # Daten aus den Eingabefeldern abrufen
    name = devicename.get()
    manufacturer_value = manufacturer.get()
    serialnumber_value = serialnumber.get()
    typ_value = typ.get()
    yearofmanufacture_value = yearofmanufacture.get()
    internID_value = internID.get()
    status_value = status.get()
    location_value = location.get()
    circuitdiagramm_value = circuitdiagramm.get()
    technivaldrawing_value = technivaldrawing.get()
    manual_value = manual.get()
    note_value = note.get()
    addressservice_value = addressservice.get()
    addressmanufacture_value = addressmanufacture.get()
    
    # SQL-Insert-Befeh
    cursor.execute('''INSERT INTO device (name, manufacturer, serialnumber, typ, yearofmanufacture, internID, status, location, circuitdiagramm, technivaldrawing, manual, note, addressservice, addressmanufacture) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (name, manufacturer_value, serialnumber_value, typ_value, yearofmanufacture_value, internID_value, status_value, location_value, circuitdiagramm_value, technivaldrawing_value, manual_value, note_value, addressservice_value, addressmanufacture_value))
    conn.commit()
    conn.close()
    print("Gerät gespeichert:", name)   
    messagebox.showinfo("Anlage hinzufügen", "Die Anlage " + name + " wurde erfolgreich hinzugefügt.") 
 # Button zum Speichern der Daten
 # Hier wird der Button zum Speichern der Daten erstellt
 save_button = tk.Button(content_frame, text="Gerät speichern", command=save_device, width=20, height=2, bg='green', fg='white')
 save_button.grid(row=9, column=1, columnspan=2, pady=20, sticky='w') 
  



#auswahlmennü
menu_bar = tk.Menu(root)

# INSTANDO Menü
def do_something():
    print("Aktion ausgeführt!")

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Startmenü", command=start)
file_menu.add_command(label="Datenbank erstellen" ,command=database)
file_menu.add_command(label="USER", command=do_something)
file_menu.add_command(label="INFO", command=info)
file_menu.add_command(label="SETTING", command=do_something)
file_menu.add_command(label="BACKUP", command=do_something)
file_menu.add_separator()
file_menu.add_command(label="Beenden", command=root.quit)
menu_bar.add_cascade(label="INSTANDO", menu=file_menu)

# ANLAGEN Menü
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Anlagen bearbeiten", command=do_something)
edit_menu.add_command(label="Einfügen", command=add_device)
menu_bar.add_cascade(label="ANLAGEN", menu=edit_menu)

#Wartung/Instandsetzung Menü   
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Wartung bearbeiten", command=do_something)
edit_menu.add_command(label="Instandsetzung", command=do_something)
menu_bar.add_cascade(label="WARTUNG/INSTANDSETZUNG", menu=edit_menu)


root.config(menu=menu_bar)
start()

root.mainloop()
