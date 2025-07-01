#!/usr/bin/python

import sqlite3
import os.path
import tkinter as tk
from tkinter import Tk, ttk 


# prüfen ob die Datenbank existiert, wenn nicht, dann wird sie erstellt

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
    print ("Tabelle Device erstellt")
    conn.close()

else:
    print ("Datenbank Ordner vorhanden")

if not os.path.exists('db/preventivemaintenance.db'):
    conn = sqlite3.connect('db/preventivemaintenance.db')
    

    conn.execute('''CREATE TABLE preventivemaintenance
         (ID INTEGER PRIMARY KEY NOT NULL,
         deviceID INTEGER NOT NULL,
         description TEXT NOT NULL,
         regulation TEXT NOT NULL,     
         planneddate DATE NOT NULL,
         completeddate DATE,
         status TEXT planned, completed, overdue NOT NULL,
         interval INTEGER NOT NULL,
         maintenancemanual BLOB NOT NULL,
         maintenancestatusreport BLOB NOT NULL
         )  )  
         ''')
    print ("Wartungsdatenbank erstellt + Tabelle  erstellt")
    conn.close()

else:
    print ("Datenbank Ordner vorhanden")

 
# GUI erstellen
# Hier wird das GUI mit Tkinter erstellt
root = tk.Tk()
root.title("INSTANDO - Instandhaltungsdatenbank")
root.geometry("1200x800")  # Fenstergröße anpassen

tk.Label(root, text="Anlage hinzufügen", font=("Arial", 25)).grid(row=0, column=0, sticky='n', pady=10)
tk.Label(root, text="Name", font=("Arial", 12)).grid(row=1, column=0, sticky='w', pady=10)
tk.Label(root, text="Hersteller", font=("Arial", 12)).grid(row=2, column=0, sticky='w', pady=10)
tk.Label(root, text="Seriennummer", font=("Arial", 12)).grid(row=3, column=0, sticky='w', pady=10)
tk.Label(root, text="Typ/Model", font=("Arial", 12)).grid(row=4, column=0, sticky='w', pady=10)
tk.Label(root, text="Baujahr", font=("Arial", 12)).grid(row=5, column=0, sticky='w', pady=10)
tk.Label(root, text="Interne ID", font=("Arial", 12)).grid(row=6, column=0, sticky='w', pady=10)
tk.Label(root, text="Status", font=("Arial", 12)).grid(row=1, column=4, sticky='s', pady=10)
tk.Label(root, text="Standort", font=("Arial", 12)).grid(row=2, column=4, sticky='', pady=10)
tk.Label(root, text="Schaltplan", font=("Arial", 12)).grid(row=3, column=4, sticky='', pady=10)
tk.Label(root, text="Technische Zeichnung", font=("Arial", 12)).grid(row=4, column=4, sticky='', pady=10)
tk.Label(root, text="Bedienungsanleitung", font=("Arial", 12)).grid(row=5, column=4, sticky='', pady=10)
tk.Label(root, text="Notizen", font=("Arial", 12)).grid(row=6, column=4, sticky='', pady=10)
tk.Label(root, text="Serviceadresse", font=("Arial", 12)).grid(row=7, column=0, sticky='W', pady=10)
tk.Label(root, text="Herstelleradresse", font=("Arial", 12)).grid(row=8, column=0, sticky='W', pady=10)  

# Eingabefelder erstellen
# Hier werden die Eingabefelder für die Datenbankeinträge erstellt  
devicename = tk.Entry(root, width=30)
devicename.grid(row=1, column=1, pady=10, sticky='w')
manufacturer = tk.Entry(root, width=30)
manufacturer.grid(row=2, column=1, pady=20, sticky='w')
serialnumber = tk.Entry(root, width=30)
serialnumber.grid(row=3, column=1, pady=20, sticky='w')
typ = tk.Entry(root, width=30)
typ.grid(row=4, column=1, pady=20, sticky='w')
yearofmanufacture = tk.Entry(root, width=30)
yearofmanufacture.grid(row=5, column=1, pady=20, sticky='w')
internID = tk.Entry(root, width=30)
internID.grid(row=6, column=1, pady=20, sticky='w')
status = ttk.Combobox(root, values=["vorhanden", "nicht mehr vorhanden"], width=27)
status.grid(row=1, column=5, pady=20, sticky='w')
location = tk.Entry(root, width=30)
location.grid(row=2, column=5, pady=20, sticky='w')
circuitdiagramm = tk.Entry(root, width=30)
circuitdiagramm.grid(row=3, column=5, pady=20, sticky=' w')
technivaldrawing = tk.Entry(root, width=30)                             
technivaldrawing.grid(row=4, column=5, pady=20, sticky='w')
manual = tk.Entry(root, width=30)
manual.grid(row=5, column=5, pady=20, sticky='w')
note = tk.Entry(root, width=30)
note.grid(row=6, column=5, pady=20, sticky='w')
addressservice = tk.Entry(root, width=50)
addressservice.grid(row=7, column=1, pady=20, sticky='w')
addressmanufacture = tk.Entry(root, width=50)
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
 
# Button zum Speichern der Daten
# Hier wird der Button zum Speichern der Daten erstellt
save_button = tk.Button(root, text="Gerät speichern", command=save_device, width=20, height=2, bg='green', fg='white')
save_button.grid(row=9, column=1, columnspan=2, pady=20, sticky='w')   
# Button zum Beenden der Anwendung
exit_button = tk.Button(root, text="Beenden", command=root.quit, width=20, height=2, bg='red', fg='white')
exit_button.grid(row=9, column=5, columnspan=2, pady=20, sticky='w')    


root.mainloop()
