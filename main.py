#!/usr/bin/python

import sqlite3
import os.path
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from datetime import date
from tkinter import filedialog
import tempfile, webbrowser

version = "Version 0.0.1"
version1 = "0.0.1"
versiondate = "2025.07.02"
license = "test"
date = date.today().strftime("%Y-%m-%d")
userrolle = "reader"
username   = "none"


# Funktion zum Erstellen der Datenbank
def database_device():
    # Ensure the 'db' directory exists
    if not os.path.exists('db'):
        os.makedirs('db')

    if not os.path.exists('db/device.db'):
        conn = sqlite3.connect('db/device.db')
        conn.execute('''CREATE TABLE device
         (ID INTEGER PRIMARY KEY NOT NULL,
         name TEXT NOT NULL,
         description TEXT NOT NULL,           
         manufacturer TEXT NOT NULL,
         serialnumber INT NOT NULL,
         typ TEXT NOT NULL,
         yearofmanufacture INT NOT NULL,
         [connected load] TEXT NOT NULL,
         internID INT NOT NULL,
         status TEXT NOT NULL,
         location TEXT NOT NULL,
         department TEXT NOT NULL,
         circuitdiagramm BLOB,
         technivaldrawing BLOB,
         manual BLOB,
         note TEXT NOT NULL,
         link TEXT NOT NULL
         )
        ''')
        messagebox.showinfo("Datenbank", "Die Datenbank 'device.db' wurde erstellt.")
        conn.close()
    else:   
        messagebox  .showinfo("Datenbank", "Die Datenbank 'device.db' existiert bereits.")  
def database_preventivemaintenance():
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
def database_user1():     
    if not os.path.exists('db/user.db'):
        conn = sqlite3.connect('db/user.db')
        conn.execute('''CREATE TABLE user
            (ID INTEGER PRIMARY KEY NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP                      
            )
    ''')
        messagebox.showinfo("Datenbank", "Die Datenbank 'user.db' wurde erstellt.")
        conn.close()
    else:
            messagebox.showinfo("Datenbank", "Die Datenbank 'user.db' existiert bereits.")
    #root-user erstellen
    conn = sqlite3.connect('db/user.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO user (username, password, role, email, phone) 
                          VALUES (?, ?, ?, ?, ?)''', 
                       ("root", "root", "admin", "root@example.com", "0000000000"))
    conn.commit()
    conn.close()

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

# Login-Funktion
def login():
    clear_content()
    #aktuelle Rolle des Benutzers
    user_info_frame = tk.Frame(content_frame)
    user_info_frame.pack(fill="x")
    tk.Label(user_info_frame, text=f"Benutzer: {username} | Rolle: {userrolle}", font=("Arial", 10), anchor="e").pack(side="right", padx=10, pady=5)

    tk.Label(content_frame, text="Login", font=("Arial", 25)).pack(pady=10)
    tk.Label(content_frame, text="Benutzername", font=("Arial", 12)).pack(pady=5)
    username_entry = tk.Entry(content_frame, width=30)
    username_entry.pack(pady=5)
    tk.Label(content_frame, text="Passwort", font=("Arial", 12)).pack(pady=5)
    password_entry = tk.Entry(content_frame, show='*', width=30)
    password_entry.pack(pady=5) 
    # Funktion zum Überprüfen der Anmeldedaten
    # Diese Funktion wird aufgerufen, wenn der "Anmelden"-Button geklickt wird
    def check_login():
        entered_username = username_entry.get()
        password = password_entry.get()

        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect('db/user.db')
        cursor = conn.cursor()

        # Benutzer in der Datenbank suchen
        cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (entered_username, password))
        user = cursor.fetchone()
        
        conn.close()

        if user:
            global userrolle, username
            userrolle = user[3]  # Rolle des Benutzers abrufen
            username = user[1]   # Username auf den angemeldeten Namen setzen
            messagebox.showinfo("Login", "Willkommen, " + username + "! Sie sind als " + userrolle + " angemeldet.")
            start()  # Startfenster anzeigen
        else:
            messagebox.showerror("Login", "Ungültiger Benutzername oder Passwort. Bitte versuchen Sie es erneut.")  
    # Button zum Überprüfen der Anmeldedaten
    login_button = tk.Button(content_frame, text="Anmelden", command=check_login, width=20, height=2, bg='blue', fg='white')
    login_button.pack(pady=10)  

# Startfenster
def start():
    clear_content()
    # User + Rolle oben rechts anzeigen
    user_info_frame = tk.Frame(content_frame)
    user_info_frame.pack(fill="x")
    tk.Label(user_info_frame, text=f"Benutzer: {username} | Rolle: {userrolle}", font=("Arial", 10), anchor="e").pack(side="right", padx=10, pady=5)

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
    clear_content()
    tk.Label(content_frame, text="INSTANDO - Instandhaltungsdatenbank", font=("Arial", 25)).pack(pady=10)
    tk.Label(content_frame, text="Version: " + version, font=("Arial", 12)).pack(pady=5)
    tk.Label(content_frame, text="Lizenz: " + license, font=("Arial", 12)).pack(pady=5)
    tk.Label(content_frame, text="Erstellt durch RWES -- https://github.com/rwesforall/INSTANDO", font=("Arial", 12)).pack(pady=5)
    tk.Label(content_frame, text="powered by Python und SQlite ", font=("Arial", 12)).pack(pady=5)
    # Logo anzeigen (optional, nicht im Messagebox möglich, daher im content_frame)
    image = Image.open("img/sqlite.png")
    image = image.resize((150, 150))
    img = ImageTk.PhotoImage(image)
    label_img = tk.Label(content_frame, image=img)
    label_img.image = img
    label_img.pack(pady=10)
    image = Image.open("img/python.png")
    image = image.resize((150, 150))
    img = ImageTk.PhotoImage(image)
    label_img = tk.Label(content_frame, image=img)
    label_img.image = img
    label_img.pack(pady=10)
                                
#usermenü
def user():
    if userrolle == "admin":
        clear_content()
        tk.Label(content_frame, text="Benutzerverwaltung", font=("Arial", 25)).pack(pady=10)
        # Benutzer hinzufügen
        tk.Label(content_frame, text="Benutzer hinzufügen", font=("Arial", 15)).pack(pady=10)
        tk.Label(content_frame, text="Benutzername", font=("Arial", 12)).pack(pady=5)
        username_entry = tk.Entry(content_frame, width=30)
        username_entry.pack(pady=5)
        tk.Label(content_frame, text="Passwort", font=("Arial", 12)).pack(pady=5)
        password_entry = tk.Entry(content_frame, show='*', width=30)
        password_entry.pack(pady=5)
        roles = ["admin", "user", "reader"]
        role_combobox = ttk.Combobox(content_frame, values=roles, width=27)
        role_combobox.set("Wählen Sie eine Rolle")
        role_combobox.pack(pady=5)
        tk.Label(content_frame, text="E-Mail", font=("Arial", 12)).pack(pady=5)
        email_entry = tk.Entry(content_frame, width=30)
        email_entry.pack(pady=5)
        tk.Label(content_frame, text="Telefon", font=("Arial", 12)).pack(pady=5)
        phone_entry = tk.Entry(content_frame, width=30)
        phone_entry.pack(pady=5)

        # Buttons oben platzieren
        button_frame = tk.Frame(content_frame)
        button_frame.pack(pady=10)
        add_user_button = tk.Button(button_frame, text="Benutzer hinzufügen", width=20, height=2, bg='green', fg='white')
        add_user_button.pack(side="left", padx=5)
        delete_user_button = tk.Button(button_frame, text="Benutzer löschen", width=20, height=2, bg='red', fg='white')
        delete_user_button.pack(side="left", padx=5)

        # Übersicht der Benutzer
        tk.Label(content_frame, text="Benutzerübersicht", font=("Arial", 25)).pack(pady=10)

        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect('db/user.db')
        cursor = conn.cursor()

        # Alle Benutzer aus der Datenbank abfragen
        cursor.execute("SELECT ID, username, role, email, phone, created_at, updated_at, last_login FROM user")
        users = cursor.fetchall()

        # Überschriften für die Tabelle (ohne Passwort)
        headers = ["ID", "Benutzername", "Rolle", "E-Mail", "Telefon", "Erstellt am", "Aktualisiert am", "Letzte Anmeldung"]

        # Baumansicht erstellen
        tree = ttk.Treeview(content_frame, columns=headers, show='headings')
        tree.pack(fill='both', expand=True)

        # Spaltenüberschriften hinzufügen
        for header in headers:
            tree.heading(header, text=header)
            tree.column(header, anchor='center')

        # Daten in die Baumansicht einfügen
        for user_row in users:
            tree.insert('', 'end', values=user_row)

        conn.close()

        # Funktion zum Hinzufügen eines Benutzers
        def add_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_combobox.get()
            email = email_entry.get()
            phone = phone_entry.get()

            if not username or not password or not role or not email or not phone:
                messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus.")
                return

            # Verbindung zur Datenbank herstellen
            conn = sqlite3.connect('db/user.db')
            cursor = conn.cursor()

            # Benutzer in die Datenbank einfügen
            cursor.execute('''INSERT INTO user (username, password, role, email, phone) 
                          VALUES (?, ?, ?, ?, ?)''',
                       (username, password, role, email, phone))
            conn.commit()
            conn.close()
            messagebox.showinfo("Benutzer hinzufügen", "Der Benutzer " + username + " wurde erfolgreich hinzugefügt.")

        # Funktion zum Löschen eines Benutzers
        def delete_user():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showerror("Fehler", "Bitte wählen Sie einen Benutzer aus der Liste aus.")
                return
            user_values = tree.item(selected_item, "values")
            user_id = user_values[0]
            if user_id == "1":
                messagebox.showerror("Fehler", "Der root-Benutzer kann nicht gelöscht werden.")
                return
            confirm = messagebox.askyesno("Benutzer löschen", f"Sind Sie sicher, dass Sie den Benutzer '{user_values[1]}' löschen möchten?")
            if confirm:
                conn = sqlite3.connect('db/user.db')
                cursor = conn.cursor()
                cursor.execute("DELETE FROM user WHERE ID=?", (user_id,))
                conn.commit()
                conn.close()
                tree.delete(selected_item)
                messagebox.showinfo("Benutzer gelöscht", f"Der Benutzer '{user_values[1]}' wurde gelöscht.")

        # Button-Commands zuweisen
        add_user_button.config(command=add_user)
        delete_user_button.config(command=delete_user)
    else:
        clear_content()
        tk.Label(content_frame, text="keine Berechtigung", font=("Arial", 25)).pack(pady=10)
    
#setting
def setting():
    if userrolle == "admin":
        print("setting")
    else:
        clear_content()
        user_info_frame = tk.Frame(content_frame)
        user_info_frame.pack(fill="x")
        tk.Label(user_info_frame, text=f"Benutzer: {username} | Rolle: {userrolle}", font=("Arial", 10), anchor="e").pack(side="right", padx=10, pady=5)
        tk.Label(content_frame, text="keine Berechtigung", font=("Arial", 25)).pack(pady=10)

        # Button zum Login-Fenster
        login_button_main = tk.Button(content_frame, text="Login", command=login, width=20, height=2, bg='blue', fg='white')
        login_button_main.pack(pady=10)
#backup
def backup():
    if userrolle == "admin":
        print("backup")
    else:
        clear_content()
        user_info_frame = tk.Frame(content_frame)
        user_info_frame.pack(fill="x")
        tk.Label(user_info_frame, text=f"Benutzer: {username} | Rolle: {userrolle}", font=("Arial", 10), anchor="e").pack(side="right", padx=10, pady=5)
        tk.Label(content_frame, text="keine Berechtigung", font=("Arial", 25)).pack(pady=10)

        # Button zum Login-Fenster
        login_button_main = tk.Button(content_frame, text="Login", command=login, width=20, height=2, bg='blue', fg='white')
        login_button_main.pack(pady=10)

#help
def help():
    clear_content()
    user_info_frame = tk.Frame(content_frame)
    user_info_frame.pack(fill="x")
    tk.Label(
        user_info_frame,
        text=f"Benutzer: {username} | Rolle: {userrolle}",
        font=("Arial", 10),
        anchor="e"
    ).pack(side="right", padx=10, pady=5)

    tk.Label(content_frame, text="Benutzerrollen Übersicht", font=("Arial", 22, "bold")).pack(pady=(20, 10))

    roles = [
        ("reader", "Darf nur lesen."),
        ("user", "Darf Wartungen anlegen, Wartungsaufträge bearbeiten, Störmeldungen bearbeiten, Tools nutzen."),
        ("admin", "Hat alle Rechte, inkl. Benutzer- und Datenbankverwaltung.")
    ]

    for role, desc in roles:
        frame = tk.Frame(content_frame, bg="#f0f0f0", bd=1, relief="solid")
        frame.pack(fill="x", padx=60, pady=8)
        tk.Label(frame, text=role.upper(), font=("Arial", 16, "bold"), width=10, anchor="w", bg="#f0f0f0").pack(side="left", padx=10, pady=10)
        tk.Label(frame, text=desc, font=("Arial", 14), anchor="w", bg="#f0f0f0").pack(side="left", padx=10, pady=10)

# Datenbank erstellen
def database():
    if userrolle == "admin":
        clear_content()
        tk.Label(content_frame, text="Datenbank verwaltung", font=("Arial", 25)).pack(pady=10)
    
        # Frame für die Buttons nebeneinander
        create_frame = tk.Frame(content_frame)
        create_frame.pack(pady=20)

        # Buttons zum Erstellen der Datenbanken
        create_button = tk.Button(create_frame, text="Anlagen Datenbank erstellen", command=database_device, width=25, height=2, bg='purple', fg='white')
        create_button.grid(row=0, column=0, padx=10)
        create_button1 = tk.Button(create_frame, text="Wartung Datenbank erstellen", command=database_preventivemaintenance, width=25, height=2, bg='purple', fg='white')
        create_button1.grid(row=0, column=1, padx=10)
        create_button2 = tk.Button(create_frame, text="Benutzer Datenbank erstellen", command=database_user1, width=25, height=2, bg='purple', fg='white')
        create_button2.grid(row=0, column=2, padx=10)

        # Frame für die Lösch-Buttons nebeneinander
        delete_frame = tk.Frame(content_frame)
        delete_frame.pack(pady=20)

        # Datenbank device.db löschen
        def delete_database():
            if os.path.exists('db/device.db'):
                os.remove('db/device.db')
                messagebox.showinfo("Datenbank löschen", "Die Datenbank 'device.db' wurde gelöscht.")
            else:
                messagebox.showerror("Fehler", "Die Datenbank 'device.db' existiert nicht.")

        # Datenbank preventivemaintenance.db löschen
        def delete_database1():
            if os.path.exists('db/preventivemaintenance.db'):
                os.remove('db/preventivemaintenance.db')
                messagebox.showinfo("Datenbank löschen", "Die Datenbank 'preventivemaintenance.db' wurde gelöscht.")
            else:
                messagebox.showerror("Fehler", "Die Datenbank 'preventivemaintenance.db' existiert nicht.")

        # Datenbank user.db löschen
        def delete_database2():
            if os.path.exists('db/user.db'):
                os.remove('db/user.db')
                messagebox.showinfo("Datenbank löschen", "Die Datenbank 'user.db' wurde gelöscht.")
            else:
                messagebox.showerror("Fehler", "Die Datenbank 'user.db' existiert nicht.")

        # Buttons zum Löschen der Datenbanken
        delete_button = tk.Button(delete_frame, text="Anlagen Datenbank löschen", command=delete_database, width=25, height=2, bg='red', fg='white')
        delete_button.grid(row=0, column=0, padx=10)
        delete_button1 = tk.Button(delete_frame, text="Wartung Datenbank löschen", command=delete_database1, width=25, height=2, bg='red', fg='white')
        delete_button1.grid(row=0, column=1, padx=10)
        delete_button2 = tk.Button(delete_frame, text="Benutzer Datenbank löschen", command=delete_database2, width=25, height=2, bg='red', fg='white')
        delete_button2.grid(row=0, column=2, padx=10)
    else:
        clear_content()
        tk.Label(content_frame, text="keine Berechtigung", font=("Arial", 25)).pack(pady=10)
    
# Anlagen hinzufügen
def add_device():
    if userrolle == "admin":
        clear_content()
        tk.Label(content_frame, text="Anlage hinzufügen", font=("Arial", 25, "bold")).pack(pady=15)

        # Haupt-Frame für Felder
        main_fields_frame = tk.Frame(content_frame)
        main_fields_frame.pack(pady=10, fill="both", expand=True)

        # Linke Spalte
        left_frame = tk.LabelFrame(main_fields_frame, text="Anlagendaten", padx=15, pady=10, font=("Arial", 11, "bold"))
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        fields_left = [
            ("Name", 30), ("Beschreibung", 30), ("Hersteller", 30), ("Seriennummer", 30),
            ("Typ/Model", 30), ("Baujahr", 30), ("Anschlussleistung", 30), ("Interne ID", 30)
        ]
        entries_left = []
        for label, width in fields_left:
            tk.Label(left_frame, text=label, font=("Arial", 12)).pack(pady=(7, 0), anchor="w")
            entry = tk.Entry(left_frame, width=width, font=("Arial", 11))
            entry.pack(pady=(0, 5))
            entries_left.append(entry)
        devicename, description, manufacturer, serialnumber, typ, yearofmanufacture, connectedload, internID = entries_left

        # Rechte Spalte
        right_frame = tk.LabelFrame(main_fields_frame, text="Weitere Informationen", padx=15, pady=10, font=("Arial", 11, "bold"))
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        tk.Label(right_frame, text="Status", font=("Arial", 12)).pack(pady=(7, 0), anchor="w")
        status = ttk.Combobox(right_frame, values=["vorhanden", "nicht mehr vorhanden"], width=27, font=("Arial", 11))
        status.set("Wählen Sie einen Status")
        status.pack(pady=(0, 5))

        fields_right = [
            ("Standort", 30), ("Abteilung", 30)
        ]
        entries_right = []
        for label, width in fields_right:
            tk.Label(right_frame, text=label, font=("Arial", 12)).pack(pady=(7, 0), anchor="w")
            entry = tk.Entry(right_frame, width=width, font=("Arial", 11))
            entry.pack(pady=(0, 5))
            entries_right.append(entry)
        location, department = entries_right

        # Datei-Auswahl für BLOB Felder
        circuitdiagramm_path = tk.StringVar()
        technivaldrawing_path = tk.StringVar()
        manual_path = tk.StringVar()

        def select_file(var):
            file_path = filedialog.askopenfilename()
            if file_path:
                var.set(file_path)

        for label, var in [
            ("Schaltplan", circuitdiagramm_path),
            ("Technische Zeichnung", technivaldrawing_path),
            ("Bedienungsanleitung", manual_path)
        ]:
            frame = tk.Frame(right_frame)
            frame.pack(fill="x", pady=(7, 0))
            tk.Label(frame, text=label, font=("Arial", 12)).pack(side="left")
            tk.Entry(frame, textvariable=var, width=20, state="readonly", font=("Arial", 10)).pack(side="left", padx=5)
            tk.Button(frame, text="Datei wählen", command=lambda v=var: select_file(v), font=("Arial", 10)).pack(side="left")

        # Weitere Felder
        note_label = tk.Label(right_frame, text="Notizen", font=("Arial", 12))
        note_label.pack(pady=(7, 0), anchor="w")
        note = tk.Entry(right_frame, width=30, font=("Arial", 11))
        note.pack(pady=(0, 5))
        link_label = tk.Label(right_frame, text="Link", font=("Arial", 12))
        link_label.pack(pady=(7, 0), anchor="w")
        link = tk.Entry(right_frame, width=30, font=("Arial", 11))
        link.pack(pady=(0, 5))

        main_fields_frame.grid_columnconfigure(0, weight=1)
        main_fields_frame.grid_columnconfigure(1, weight=1)

        def file_to_blob(path):
            if not path:
                return None
            try:
                with open(path, "rb") as f:
                    return f.read()
            except Exception:
                return None

        def save_device():
            name = devicename.get().strip()
            description_value = description.get().strip()
            manufacturer_value = manufacturer.get().strip()
            serialnumber_value = serialnumber.get().strip()
            typ_value = typ.get().strip()
            yearofmanufacture_value = yearofmanufacture.get().strip()
            connectedload_value = connectedload.get().strip()
            internID_value = internID.get().strip()
            status_value = status.get().strip()
            location_value = location.get().strip()
            department_value = department.get().strip()
            note_value = note.get().strip()
            link_value = link.get().strip()
            circuitdiagramm_blob = file_to_blob(circuitdiagramm_path.get())
            technivaldrawing_blob = file_to_blob(technivaldrawing_path.get())
            manual_blob = file_to_blob(manual_path.get())

            if not name or not description_value or not manufacturer_value or not serialnumber_value or not typ_value or not yearofmanufacture_value or not connectedload_value or not internID_value or not status_value or not location_value or not department_value:
                messagebox.showerror("Fehler", "Bitte füllen Sie alle Pflichtfelder aus.")
                return

            conn = sqlite3.connect('db/device.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO device (name, description, manufacturer, serialnumber, typ, yearofmanufacture, [connected load], internID, status, location, department, circuitdiagramm, technivaldrawing, manual, note, link)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (name, description_value, manufacturer_value, serialnumber_value, typ_value, yearofmanufacture_value, connectedload_value, internID_value, status_value, location_value, department_value, circuitdiagramm_blob, technivaldrawing_blob, manual_blob, note_value, link_value))
            conn.commit()
            conn.close()
            messagebox.showinfo("Anlage hinzufügen", f"Die Anlage '{name}' wurde erfolgreich hinzugefügt.")

        # Button zum Speichern
        save_button = tk.Button(content_frame, text="Gerät speichern", command=save_device, width=20, height=2, bg='green', fg='white', font=("Arial", 12, "bold"))
        save_button.pack(pady=20)
    else:
        clear_content()
        user_info_frame = tk.Frame(content_frame)
        user_info_frame.pack(fill="x")
        tk.Label(user_info_frame, text=f"Benutzer: {username} | Rolle: {userrolle}", font=("Arial", 10), anchor="e").pack(side="right", padx=10, pady=5)
        tk.Label(content_frame, text="keine Berechtigung", font=("Arial", 25)).pack(pady=10)

        # Button zum Login-Fenster
        login_button_main = tk.Button(content_frame, text="Login", command=login, width=20, height=2, bg='blue', fg='white')
        login_button_main.pack(pady=10)
# Übersicht der Anlagen
def device_overview():
    clear_content()
    tk.Label(content_frame, text="Anlagenübersicht", font=("Arial", 25)).pack(pady=10)

    main_frame = tk.Frame(content_frame)
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Linke Seite: Übersichtsliste
    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="y", expand=False, padx=(0, 20))

    tk.Label(left_frame, text="Geräte (Interne ID, Name, Typ)", font=("Arial", 13, "bold")).pack(pady=(0, 5))

    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect('db/device.db')
    cursor = conn.cursor()
    cursor.execute("SELECT ID, internID, name, typ FROM device WHERE status = ? ORDER BY internID ASC", ("vorhanden",))
    devices = cursor.fetchall()

    # Treeview für die Übersicht
    tree = ttk.Treeview(left_frame, columns=("Interne ID", "Name", "Typ"), show='headings', height=20)
    tree.pack(fill="y", expand=False)

    for col in ("Interne ID", "Name", "Typ"):
        tree.heading(col, text=col)
        tree.column(col, anchor='center', width=120)

    for device in devices:
        tree.insert('', 'end', iid=device[0], values=(device[1], device[2], device[3]))

    # Rechte Seite: Detailanzeige
    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="left", fill="both", expand=True)

    detail_labels = [
        "Interne ID", "Name", "Beschreibung", "Hersteller", "Seriennummer", "Typ/Model",
        "Baujahr", "Anschlussleistung", "Status", "Standort", "Abteilung", "Notizen", "Link"
    ]
    detail_vars = [tk.StringVar() for _ in detail_labels]

    for i, label in enumerate(detail_labels):
        tk.Label(right_frame, text=label + ":", font=("Arial", 11, "bold")).grid(row=i, column=0, sticky="e", pady=2, padx=5)
        tk.Label(right_frame, textvariable=detail_vars[i], font=("Arial", 11), anchor="w", wraplength=350, justify="left").grid(row=i, column=1, sticky="w", pady=2, padx=5)

    # Datei-Anzeige Buttons
    file_labels = [
        ("Schaltplan", "circuitdiagramm", 12),
        ("Technische Zeichnung", "technivaldrawing", 13),
        ("Bedienungsanleitung", "manual", 14)
    ]

    def save_and_open_blob(device_id, col_index, title, filetype):
        # Datei aus DB holen und temporär speichern
        conn = sqlite3.connect('db/device.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT {filetype} FROM device WHERE ID=?", (device_id,))
        blob = cursor.fetchone()
        conn.close()
        if not blob or not blob[0]:
            messagebox.showinfo("Datei anzeigen", f"Keine Datei für {title} vorhanden.")
            return
        ext = ".pdf" if filetype == "manual" else ".png"
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(blob[0])
            tmp_path = tmp.name
        try:
            webbrowser.open(tmp_path)
        except Exception as e:
            messagebox.showerror("Fehler", f"Datei konnte nicht geöffnet werden: {e}")

    button_frame = tk.Frame(right_frame)
    button_frame.grid(row=len(detail_labels), column=0, columnspan=2, pady=(10, 0))

    def get_selected_device_id():
        selected = tree.selection()
        if not selected:
            return None
        return selected[0]

    for idx, (label, col, db_col_index) in enumerate(file_labels):
        btn = tk.Button(
            button_frame,
            text=f"{label}",
            width=18,
            command=lambda c=col, i=db_col_index, l=label: (
                lambda: save_and_open_blob(get_selected_device_id(), i, l, c)
            )()
        )
        btn.grid(row=0, column=idx, padx=5)

    def show_details(event):
        selected = tree.selection()
        if not selected:
            return
        device_id = selected[0]
        conn = sqlite3.connect('db/device.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT internID, name, description, manufacturer, serialnumber, typ, yearofmanufacture, [connected load], status, location, department, note, link FROM device WHERE ID=?",
            (device_id,))
        data = cursor.fetchone()
        conn.close()
        if data:
            for var, value in zip(detail_vars, data):
                var.set(str(value) if value is not None else "")
        else:
            for var in detail_vars:
                var.set("")

    tree.bind("<<TreeviewSelect>>", show_details)

    # Optional: erstes Gerät vorselektieren und Details anzeigen
    if devices:
        tree.selection_set(devices[0][0])
        show_details(None)

# Anlagen bearbeiten
def edit_device():
    if userrolle == "admin":
        clear_content()
        tk.Label(content_frame, text="Anlagen bearbeiten", font=("Arial", 25, "bold")).pack(pady=15)

        # Auswahlfeld für Gerät
        select_frame = tk.Frame(content_frame)
        select_frame.pack(pady=10, fill="x")
        tk.Label(select_frame, text="Anlage auswählen:", font=("Arial", 13)).pack(side="left", padx=(0, 10))
        conn = sqlite3.connect('db/device.db')
        cursor = conn.cursor()
        cursor.execute("SELECT ID, internID, name FROM device")
        devices = cursor.fetchall()
        conn.close()
        device_names = [f"{device[0]} - {device[1]} - {device[2]}" for device in devices]
        device_combobox = ttk.Combobox(select_frame, values=device_names, width=60, font=("Arial", 11))
        device_combobox.set("Wählen Sie ein Gerät")
        device_combobox.pack(side="left", padx=(0, 10))

        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(pady=5)
        load_button = tk.Button(button_frame, text="Anlage laden", command=lambda: load_device_data(), width=18, height=1, bg='#1976D2', fg='white', font=("Arial", 11, "bold"))
        load_button.pack(side="left", padx=5)
        save_button = tk.Button(button_frame, text="Änderungen speichern", command=lambda: save_edited_device(), width=18, height=1, bg='#388E3C', fg='white', font=("Arial", 11, "bold"))
        save_button.pack(side="left", padx=5)

        # Felder-Layout
        main_fields_frame = tk.Frame(content_frame)
        main_fields_frame.pack(pady=15, fill="both", expand=True)

        left_frame = tk.LabelFrame(main_fields_frame, text="Anlagendaten", padx=15, pady=10, font=("Arial", 11, "bold"))
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        right_frame = tk.LabelFrame(main_fields_frame, text="Weitere Informationen", padx=15, pady=10, font=("Arial", 11, "bold"))
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        # Linke Spalte Felder
        fields_left = [
            ("Name", 30), ("Beschreibung", 30), ("Hersteller", 30), ("Seriennummer", 30), ("Typ", 30),
            ("Baujahr", 30), ("Anschlussleistung", 30), ("Interne ID", 30)
         ]
        entries_left = []
        for label, width in fields_left:
            tk.Label(left_frame, text=label, font=("Arial", 12)).pack(pady=(7, 0), anchor="w")
            entry = tk.Entry(left_frame, width=width, font=("Arial", 11))
            entry.pack(pady=(0, 5))
            entries_left.append(entry)
        devicename, description, manufacturer, serialnumber, typ, yearofmanufacture, connectedload, internID_entry = entries_left

        # Rechte Spalte Felder
        tk.Label(right_frame, text="Status", font=("Arial", 12)).pack(pady=(7, 0), anchor="w")
        status = ttk.Combobox(right_frame, values=["vorhanden", "nicht mehr vorhanden"], width=27, font=("Arial", 11))
        status.set("Wählen Sie einen Status")
        status.pack(pady=(0, 5))
        fields_right = [
            ("Standort", 30), ("Abteilung", 30)
        ]
        entries_right = []
        for label, width in fields_right:
            tk.Label(right_frame, text=label, font=("Arial", 12)).pack(pady=(7, 0), anchor="w")
            entry = tk.Entry(right_frame, width=width, font=("Arial", 11))
            entry.pack(pady=(0, 5))
            entries_right.append(entry)
        location, department = entries_right

        # Datei-Auswahl für BLOB Felder
        blob_files = {
            "circuitdiagramm": {"label": "Schaltplan", "path": tk.StringVar()},
            "technivaldrawing": {"label": "Technische Zeichnung", "path": tk.StringVar()},
            "manual": {"label": "Bedienungsanleitung", "path": tk.StringVar()}
         }
        def select_file(blob_key):
            file_path = filedialog.askopenfilename()
            if file_path:
                blob_files[blob_key]["path"].set(file_path)

        for key in ["circuitdiagramm", "technivaldrawing", "manual"]:
            frame = tk.Frame(right_frame)
            frame.pack(fill="x", pady=(7, 0))
            tk.Label(frame, text=blob_files[key]["label"], font=("Arial", 12)).pack(side="left")
            tk.Entry(frame, textvariable=blob_files[key]["path"], width=20, state="readonly", font=("Arial", 10)).pack(side="left", padx=5)
            tk.Button(frame, text="Datei wählen", command=lambda k=key: select_file(k), font=("Arial", 10)).pack(side="left")

        # Weitere Felder
        note_label = tk.Label(right_frame, text="Notizen", font=("Arial", 12))
        note_label.pack(pady=(7, 0), anchor="w")
        note = tk.Entry(right_frame, width=30, font=("Arial", 11))
        note.pack(pady=(0, 5))
        link_label = tk.Label(right_frame, text="Link", font=("Arial", 12))
        link_label.pack(pady=(7, 0), anchor="w")
        link = tk.Entry(right_frame, width=30, font=("Arial", 11))
        link.pack(pady=(0, 5))

        main_fields_frame.grid_columnconfigure(0, weight=1)
        main_fields_frame.grid_columnconfigure(1, weight=1)

        # Gerätedaten laden
        def load_device_data():
            selected_device = device_combobox.get()
            if not selected_device:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Gerät aus.")
                return
            id_value = selected_device.split(" - ")[0]
            conn = sqlite3.connect('db/device.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM device WHERE ID = ?", (id_value,))
            device_data = cursor.fetchone()
            conn.close()
            if not device_data:
                messagebox.showerror("Fehler", "Gerät nicht gefunden.")
                return
            devicename.delete(0, tk.END)
            devicename.insert(0, device_data[1])
            description.delete(0, tk.END)
            description.insert(0, device_data[2])
            manufacturer.delete(0, tk.END)
            manufacturer.insert(0, device_data[3])
            serialnumber.delete(0, tk.END)
            serialnumber.insert(0, device_data[4])
            typ.delete(0, tk.END)
            typ.insert(0, device_data[5])
            yearofmanufacture.delete(0, tk.END)
            yearofmanufacture.insert(0, device_data[6])
            connectedload.delete(0, tk.END)
            connectedload.insert(0, device_data[7])
            internID_entry.delete(0, tk.END)
            internID_entry.insert(0, device_data[8])
            status.set(device_data[9])
            location.delete(0, tk.END)
            location.insert(0, device_data[10])
            department.delete(0, tk.END)
            department.insert(0, device_data[11])
            for idx, key in zip([12, 13, 14], ["circuitdiagramm", "technivaldrawing", "manual"]):
                blob_files[key]["path"].set("")
            note.delete(0, tk.END)
            note.insert(0, device_data[15])
            link.delete(0, tk.END)
            link.insert(0, device_data[16])

        # Datei zu BLOB
        def file_to_blob(path):
            if not path:
                return None
            try:
                with open(path, "rb") as f:
                    return f.read()
            except Exception:
                return None

        # Gerät speichern
        def save_edited_device():
            selected_device = device_combobox.get()
            if not selected_device:
                messagebox.showerror("Fehler", "Bitte wählen Sie ein Gerät aus.")
                return
            id_value = selected_device.split(" - ")[0]
            name = devicename.get().strip()
            description_value = description.get().strip()
            manufacturer_value = manufacturer.get().strip()
            serialnumber_value = serialnumber.get().strip()
            typ_value = typ.get().strip()
            yearofmanufacture_value = yearofmanufacture.get().strip()
            connectedload_value = connectedload.get().strip()
            internID_value = internID_entry.get().strip()
            status_value = status.get().strip()
            location_value = location.get().strip()
            department_value = department.get().strip()
            note_value = note.get().strip()
            link_value = link.get().strip()
            circuitdiagramm_blob = file_to_blob(blob_files["circuitdiagramm"]["path"].get())
            technivaldrawing_blob = file_to_blob(blob_files["technivaldrawing"]["path"].get())
            manual_blob = file_to_blob(blob_files["manual"]["path"].get())

            if not name or not internID_value:
                messagebox.showerror("Fehler", "Name und Interne ID dürfen nicht leer sein.")
                return

            conn = sqlite3.connect('db/device.db')
            cursor = conn.cursor()
            cursor.execute("SELECT circuitdiagramm, technivaldrawing, manual FROM device WHERE ID=?", (id_value,))
            old_blobs = cursor.fetchone()
            if circuitdiagramm_blob is None:
                circuitdiagramm_blob = old_blobs[0]
            if technivaldrawing_blob is None:
                technivaldrawing_blob = old_blobs[1]
            if manual_blob is None:
                manual_blob = old_blobs[2]

            cursor.execute('''UPDATE device SET name=?, description=?, manufacturer=?, serialnumber=?, typ=?, yearofmanufacture=?, [connected load]=?, internID=?, status=?, location=?, department=?, circuitdiagramm=?, technivaldrawing=?, manual=?, note=?, link=?
                            WHERE ID=?''',
                        (name, description_value, manufacturer_value, serialnumber_value, typ_value, yearofmanufacture_value, connectedload_value, internID_value, status_value, location_value, department_value, circuitdiagramm_blob, technivaldrawing_blob, manual_blob, note_value, link_value, id_value))
            conn.commit()
            conn.close()
            messagebox.showinfo("Gerät bearbeiten", f"Die Änderungen für das Gerät '{name}' wurden erfolgreich gespeichert.")
    else:
        clear_content()
        user_info_frame = tk.Frame(content_frame)
        user_info_frame.pack(fill="x")
        tk.Label(user_info_frame, text=f"Benutzer: {username} | Rolle: {userrolle}", font=("Arial", 10), anchor="e").pack(side="right", padx=10, pady=5)
        tk.Label(content_frame, text="keine Berechtigung", font=("Arial", 25)).pack(pady=10)

        # Button zum Login-Fenster
        login_button_main = tk.Button(content_frame, text="Login", command=login, width=20, height=2, bg='blue', fg='white')
        login_button_main.pack(pady=10)


#auswahlmennü
menu_bar = tk.Menu(root)

# INSTANDO Menü
def do_something():
    print("Aktion ausgeführt!")

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Startmenü", command=start)
file_menu.add_command(label="Login", command=login)
file_menu.add_command(label="Datenbank" ,command=database)
file_menu.add_command(label="USER", command=user)
file_menu.add_command(label="SETTING", command=setting)
file_menu.add_command(label="BACKUP", command=backup)
file_menu.add_command(label="HELP",command=help)
file_menu.add_separator()
file_menu.add_command(label="Beenden", command=root.quit)
file_menu.add_command(label="INFO", command=info)
menu_bar.add_cascade(label="INSTANDO", menu=file_menu)

# ANLAGEN Menü
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Übersicht", command=device_overview)
edit_menu.add_command(label="Anlagen bearbeiten", command=edit_device)
edit_menu.add_command(label="Einfügen", command=add_device)
menu_bar.add_cascade(label="ANLAGEN", menu=edit_menu)

# Wartung/Instandsetzung Menü   
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Wartung bearbeiten", command=do_something)
edit_menu.add_command(label="Instandsetzung", command=do_something)
menu_bar.add_cascade(label="WARTUNG/INSTANDSETZUNG", menu=edit_menu)

# Störaufträge Menü
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Störaufträge hinzufügen", command=do_something)
edit_menu.add_command(label="Störaufträge bearbeiten", command=do_something)
menu_bar.add_cascade(label="STÖRAUFTRÄGE", menu=edit_menu)  

# Tools Menü
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Prüfprotokoll", command=do_something)
edit_menu.add_command(label="Adressbuch", command=do_something)
edit_menu.add_command(label="Werkzeugliste", command=do_something)
menu_bar.add_cascade(label="TOOLS", menu=edit_menu)
root.config(menu=menu_bar)


start()

root.mainloop()
