#!/usr/bin/python

import sqlite3
import os.path

# prüfen ob die Datenbank existiert, wenn nicht, dann wird sie erstellt

if not os.path.exists('db/DEVICE.db'):
    conn = sqlite3.connect('db/DEVICE.db')
    print ("Datenbank erstellt")

    conn.execute('''CREATE TABLE DEVICE
         (ID INT PRIMARY KEY     NOT NULL,
         Hersteller           TEXT    NOT NULL,
         Seriennummer         INT     NOT NULL,
         Typ                    Text     NOT NULL)
         
         ''')
    print ("Tabelle  Device erstellt")
    conn.close()

else:
    print ("Datenbank Ordner vorhanden")

if not os.path.exists('db/MESSUNG.db'):
    conn = sqlite3.connect('db/MESSUNG.db')
    print ("Messungs Datenbank erstellt")

    conn.execute('''CREATE TABLE MESSUNG
         (ID INTEGER PRIMARY KEY NOT NULL,
         Hersteller           TEXT    NOT NULL,
         Seriennummer         INTEGER NOT NULL,
         Schutzkasse          INTEGER NOT NULL,
         Sichtprüfung         TEXT    NOT NULL,
         Rpe                  NUMERIC NOT NULL,
         Riso                 NUMERIC NOT NULL,
         Si                   NUMERIC NOT NULL,    
         Bi                   NUMERIC NOT NULL,
         Datum                DATE    NOT NULL, 
         Messgerät_ID         INTEGER NOT NULL)
        ''')
    print ("Tabelle  Device erstellt")
    conn.close()

else:
    print ("Datenbank Ordner vorhanden")
#Messgeräte Datenbank erstellen und Daten einfügen

print("Messgerät hinzufügen = H")
print("Messgeräte anzeigen = A")
print("Messung hinzufügen = M" )
usereingabe = input()


if usereingabe == "H":
    print("Messgerät hinzufügen")   
    ID = input("ID: ")
    Hersteller = input("Hersteller: ")
    Seriennummer = input("Seriennummer: ")
    Typ = input("Typ: ")    
    # Verbindung zur Datenbank herstellen und Daten einfügen
    conn = sqlite3.connect('db/device.db')
    cursor = conn.cursor()  
    cursor.execute("INSERT INTO DEVICE (ID, Hersteller, Seriennummer, Typ) VALUES (?, ?, ?, ?)", (ID, Hersteller, Seriennummer, Typ))
    print ("Daten in die Tabelle Device eingefügt")
    conn.commit()
    conn.close()    

if usereingabe == "A":
    print("Messgeräte anzeigen")   
    # Verbindung zur Datenbank herstellen und Daten abfragen
    conn = sqlite3.connect('db/device.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DEVICE")
    rows = cursor.fetchall()
    print ("Abfrage der Datenbank")
    for row in rows:
        print("ID:", row[0], "Hersteller:", row[1], "Seriennummer:", row[2], "Typ:", row[3]) 
    conn.close()

if usereingabe == "M":
    print("Messung hinzufügen") 
    ID = input("ID: ")
    Hersteller = input("Hersteller: ")
    Seriennummer = input("Seriennummer: ")
    Schutzkasse = input("Schutzkasse (1-3): ")
    Sichtprüfung = input("Sichtprüfung (OK or NOK): ")
    Rpe = input("Rpe: ")
    Riso = input("Riso: ")
    Si = input("Si: ")
    Bi = input("Bi: ")
    Datum = input("Datum (YYYY-MM-DD): ")
    Messgerät_ID = input("Messgerät ID: ")
    # Verbindung zur Datenbank herstellen und Daten einfügen


    conn = sqlite3.connect('db/MESSUNG.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO MESSUNG (ID, Hersteller, Seriennummer, Schutzkasse, Sichtprüfung, Rpe, Riso, Si, Bi, Datum, Messgerät_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                   (ID, Hersteller, Seriennummer, Schutzkasse, Sichtprüfung, Rpe, Riso, Si, Bi, Datum, Messgerät_ID))   
    print ("Daten in die Tabelle Messung eingefügt")

    #Daten anzeigen
    cursor.execute("SELECT * FROM MESSUNG")
    rows = cursor.fetchall()
    print ("Abfrage der Datenbank")
    for row in rows:                
        print("ID:", row[0], "Hersteller:", row[1], "Seriennummer:", row[2], "Schutzkasse:", row[3], "Sichtprüfung:", row[4], 
              "Rpe:", row[5], "Riso:", row[6], "Si:", row[7], "Bi:", row[8], "Datum:", row[9], "Messgerät_ID:", row[10])
        
    # Änderungen speichern und Verbindung schließen
    print("Daten in die Tabelle Messung eingefügt")

        
    conn.commit()
    conn.close()    







