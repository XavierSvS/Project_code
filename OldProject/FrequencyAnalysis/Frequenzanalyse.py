#Import Bibliotheken
import math
import openpyxl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl.drawing.image import Image
from io import BytesIO

#Input-Datei einlesen und Darstellung Output vorbereiten
# Passe den Dateipfad entsprechend deiner Datei an
dateipfad = "Dateninput.xlsx" # Die Excel Datei muss sich im gleichen Ordner befinden wie die Jupyter Datei

# Einlesen der Excel-Datei
daten = pd.read_excel(dateipfad)

# Anzeigen der Dimension der eingelesenen Daten
#print("Dimensionen der Daten:", daten.shape)
anzahl_spalten = daten.shape[1]
#print("Anzahl der Spalten:", anzahl_spalten)

#Resultat in eine Excel Datei schreiben
from openpyxl import Workbook
# Create a new workbook
workbook = Workbook()

#"active worksheet" auswählen
sheet = workbook.active
sheet.title = "Resultate"

#Titel in Zelle B4 schreiben
sheet['B2'] = "Ergebnisse Frequenzanalyse"
sheet.append([])

#Input-Parameter einlesen
#Welche Form hat der Mast? 1 = konisch (Hohlkreis), 2 = konisch (Achteck), 3 = zylindrisch (Hohlkreis)
form_excel = daten.iloc[1,1]
#print("Form Excel:" , form_excel)
if form_excel == "konisch (Hohlkreis)":
    form = 1
elif form_excel == "konisch (Achteck)":
    form = 2
elif form_excel == "zylindrisch (Hohlkreis)":
    form = 3
#Aus welchem Material ist der Mast? 1 = Stahl S235, 2 = Stahl S275, 3 = Stahl S355, 4 = Aluminium 6061
material_excel = daten.iloc[3,1]
#print("Material Excel:" , material_excel)
if material_excel == "Stahl S235":
    material = 1
elif material_excel == "Stahl S275":
    material = 2
elif material_excel == "Stahl S355":
    material = 3
elif material_excel == "Aluminium 6061":
    material = 4
#Wie hoch ist der Mast [m]?
hoehe_excel = daten.iloc[6,1]
#print("Höhe Excel:" , hoehe_excel)
hoehe = hoehe_excel

#für konische Form werden nur 2 Durchmesser/Seitenlängen benötigt. Für zylindrische Form so viele wie man will.
#für zylindrischer Querschnitt: d = Aussendurchmesser [m], für achteckiger Querschnitt: d = Seitenlänge Achteck (aussen) [m]
#In den folgenden Listen kann der Aussendurchmesser/Seitenlänge [m] sowie die Höhe dieses Querschnitts [m] angegeben werden.
d_list_eingabe = []
z_list = []
if form == 1 or form == 2:
    d_list_eingabe_excel1 = daten.iloc[8,1]
    z_list_excel1 = daten.iloc[10,1]
    d_list_eingabe.append(d_list_eingabe_excel1)
    z_list.append(z_list_excel1)
    d_list_eingabe_excel2 = daten.iloc[8,2]
    z_list_excel2 = daten.iloc[10,2]
    d_list_eingabe.append(d_list_eingabe_excel2)
    z_list.append(z_list_excel2)
elif form == 3:
    d_list_eingabe_excel = daten.iloc[8,1]
    anzahl_D = 0
    while pd.notnull(d_list_eingabe_excel):
        z_list_excel = daten.iloc[10,1+anzahl_D]
        anzahl_D += 1
        d_list_eingabe.append(d_list_eingabe_excel)
        z_list.append(z_list_excel)
        if anzahl_D >= anzahl_spalten-1:
            break
        d_list_eingabe_excel = daten.iloc[8,1+anzahl_D]
#print("d_list_eingabe")
#print(d_list_eingabe)
#print("z_list")
#print(z_list)

#Dicke der Mastwand [m]:
t_excel = daten.iloc[12,1]
#print("t:" , t_excel)
t = t_excel

#input für die Leuchte
#die Höhe der Leuchte ist momentan automatisch die Masthöhe und es gibt nur eine Leuchte
#Fläche der Leuchte [m^2]:
A_x_leuchte_excel = daten.iloc[15,1]
#print("A_x Leuchte:" , A_x_leuchte_excel)
A_x_leuchte = A_x_leuchte_excel
A_y_leuchte_excel = daten.iloc[15,2]
#print("A_y Leuchte:" , A_y_leuchte_excel)
A_y_leuchte = A_y_leuchte_excel
#Masse der Leuchte [kg]:
m_leuchte_excel = daten.iloc[15,3]
#print("m Leuchte:" , m_leuchte_excel)
m_leuchte = m_leuchte_excel

#input für die Zusatzmassen
#Im Folgenden können Sie die Höhe [m], die Masse [kg] und die projizierte Fläche [m^2] von Zusatzmassen in die Listen eingeben.
#Die Einträge an der gleichen Stelle der jeweiligen Listen sollten dabei der gleichen Zusatzmasse entsprechen.
z_zusatzmasse_list = []
A_x_zusatzmasse_list = []
A_y_zusatzmasse_list = []
m_zusatzmasse_list = []
z_zusatzmasse_excel = daten.iloc[19,2]
anzahl_zusatzmassen = 0
while pd.notnull(z_zusatzmasse_excel):
    A_x_zusatzmasse_excel = daten.iloc[20,2+anzahl_zusatzmassen]
    A_y_zusatzmasse_excel = daten.iloc[21,2+anzahl_zusatzmassen]
    m_zusatzmasse_excel = daten.iloc[22,2+anzahl_zusatzmassen]
    anzahl_zusatzmassen += 1
    z_zusatzmasse_list.append(z_zusatzmasse_excel)
    A_x_zusatzmasse_list.append(A_x_zusatzmasse_excel)
    A_y_zusatzmasse_list.append(A_y_zusatzmasse_excel)
    m_zusatzmasse_list.append(m_zusatzmasse_excel)
    if anzahl_zusatzmassen >= anzahl_spalten-2:
        break
    z_zusatzmasse_excel = daten.iloc[19,2+anzahl_zusatzmassen]
#print("z_zusatzmasse_list")
#print(z_zusatzmasse_list)
#print("A_x_zusatzmasse_list")
#print(A_x_zusatzmasse_list)
#print("A_y_zusatzmasse_list")
#print(A_y_zusatzmasse_list)
#print("m_zusatzmasse_list")
#print(m_zusatzmasse_list)

#input für die Abmessungen von Türen/Öffnungen im Mast
tuer_excel = daten.iloc[27,2]
tuer = "Nein" #damit der code auch ohne Öffnung funktioniert
hoehe_tuere_list = []
laenge_tuere_list = []
breite_tuere_list = []
eckradius_tuere_list = []
dicke_verstaerkung_list = []
breite_verstaerkung_list = []
ausrichtung_tuere_list = []
anzahl_tueren = 0
while tuer_excel != "Nein":
    tuer = "Ja"
    hoehe_tuere_excel = daten.iloc[28,2+anzahl_tueren]
    hoehe_tuere_list.append(hoehe_tuere_excel)
    laenge_tuere_excel = daten.iloc[29,2+anzahl_tueren]
    laenge_tuere_list.append(laenge_tuere_excel)
    breite_tuere_excel = daten.iloc[30,2+anzahl_tueren]
    breite_tuere_list.append(breite_tuere_excel)
    eckradius_tuere_excel = daten.iloc[33,2+anzahl_tueren]
    if pd.isnull(eckradius_tuere_excel):
        eckradius_tuere_excel = 0
    eckradius_tuere_list.append(eckradius_tuere_excel)
    if tuer_excel == "Ja (verstärkt Typ 4)":
        dicke_verstaerkung_excel = daten.iloc[31,2+anzahl_tueren]
        breite_verstaerkung_excel = daten.iloc[32,2+anzahl_tueren]
    elif tuer_excel == "Ja (unverstärkt)":
        dicke_verstaerkung_excel = 0
        breite_verstaerkung_excel = 0
    dicke_verstaerkung_list.append(dicke_verstaerkung_excel)
    breite_verstaerkung_list.append(breite_verstaerkung_excel)
    ausrichtung_tuere_excel = daten.iloc[34,2+anzahl_tueren]
    ausrichtung_tuere_list.append(ausrichtung_tuere_excel)
    anzahl_tueren += 1
    if anzahl_tueren >= anzahl_spalten-2:
        break
    tuer_excel = daten.iloc[27,2+anzahl_tueren]
#print("hoehe_tuere_list")
#print(hoehe_tuere_list)
#print("laenge_tuere_list")
#print(laenge_tuere_list)
#print("breite_tuere_list")
#print(breite_tuere_list)
#print("eckradius_tuere_list")
#print(eckradius_tuere_list)
#print("dicke_verstaerkung_list")
#print(dicke_verstaerkung_list)
#print("breite_verstaerkung_list")
#print(breite_verstaerkung_list)
#print("ausrichtung_tuere_list")
#print(ausrichtung_tuere_list)

#Windzone gemäss SIA 261-Anhang E: Geben Sie 1,2,3,4,5,6 oder 7 ein.
#1 : q_p0 = 0.9 kN/m2, 'Allgemein';2 : q_p0 = 1.1 kN/m2, 'Allgemein';3 : q_p0 = 1.3 kN/m2, 'Allgemein';
#4 : q_p0 = 2.4 kN/m2, 'Jura';5 : q_p0 = 2.7 kN/m2, 'Alpen', konservativ;
#6 : q_p0 = 3.3 kN/m2, 'Alpen', konservativ;7 : q_p0 = 3.3 kN/m2, 'Alpen'
windzone_excel = daten.iloc[37, 1]
#print("Windzone:" , windzone_excel)
if windzone_excel == "1 : q_p0 = 0.9 kN/m2, 'Allgemein'":
    windzone = 1
elif windzone_excel == "2 : q_p0 = 1.1 kN/m2, 'Allgemein'":
    windzone = 2
elif windzone_excel == "3 : q_p0 = 1.3 kN/m2, 'Allgemein'":
    windzone = 3
elif windzone_excel == "4 : q_p0 = 2.4 kN/m2, 'Jura'":
    windzone = 4
elif windzone_excel == "5 : q_p0 = 2.7 kN/m2, 'Alpen'":
    windzone = 5
elif windzone_excel == "6 : q_p0 = 3.3 kN/m2, 'Alpen'":
    windzone = 6
elif windzone_excel == "7 : q_p0 = 3.3 kN/m2, 'Alpen'":
    windzone = 7
#print("Windzone:" , windzone)

#Geländekategorie gemäss SIA 261, 6.2.1.2, Tabelle 4: Geben Sie 2, 2a, 3 oder 4 ein.
#2  = Seeufer; 2a = grosse Ebene; 3  = Ortschaften,freies Feld; 4  = grossflächige Stadtgebiete
gelaendekategorie_excel = daten.iloc[40, 1]
if gelaendekategorie_excel == "2  = Seeufer":
    gelaendekategorie = "2"
elif gelaendekategorie_excel == "2a = grosse Ebene":
    gelaendekategorie = "2a"
elif gelaendekategorie_excel == "3  = Ortschaften,freies Feld":
    gelaendekategorie = "3"
elif gelaendekategorie_excel == "4  = grossflächige Stadtgebiete":
    gelaendekategorie = "4"
#print("gelaendekategorie")
#print(gelaendekategorie)

#Klasse der horizontalen Verformungen gemäss SN-EN 40-3-3, 6.5.1, Tabelle 4 : Geben Sie 1,2 oder 3 ein. 1 = 4%, 2 = 6%, 3 = 10%
#Annanhme: w vernachlässigbar
klasse_verschiebung_excel = daten.iloc[46, 1]
if klasse_verschiebung_excel == "Klasse 1 (4%)":
    klasse_verschiebung = 1
elif klasse_verschiebung_excel == "Klasse 2 (6%)":
    klasse_verschiebung = 2
elif klasse_verschiebung_excel == "Klasse 3 (10%)":
    klasse_verschiebung = 3
#print("klasse_verschiebung")
#print(klasse_verschiebung)

#In wie viele Elemente soll der Mast zur Berechnung unterteilt werden: [ganze Zahl]
anzahl_elemente_excel = daten.iloc[49, 1]
anzahl_elemente = anzahl_elemente_excel
#print("anzahl_elemente")
#print(anzahl_elemente)

#gemessene Eigenfrequenzen
f_1_gemessen_x = daten.iloc[52,1]
f_1_gemessen_y = daten.iloc[52,2]
#print("1. Eigenfrequenz gemessen x:" , f_1_gemessen_x)
#print("1. Eigenfrequenz gemessen y:" , f_1_gemessen_y)
erfüllt = False
if f_1_gemessen_x != 0:
    entscheidungsachse = "x"
elif f_1_gemessen_x == 0 and f_1_gemessen_y != 0:
    entscheidungsachse = "y"
else:
    erfüllt = True
    entscheidungsachse = "Keine"
#print("Entscheidungsachse:" , entscheidungsachse)
#print("erfüllt:" , erfüllt)

#Berechnung inputabhängiger Variablen
#Berechnungen, jeweils in der Mitte eines Elements zwischen zwei "nodes" berechnet.
#Durchmesser wenn achteckiger Querschnitt
d_flanke = [0] * (len(d_list_eingabe))
d_aussen = [0] * (len(d_list_eingabe))
if form == 2:
    for i in range (len(d_list_eingabe)):
        #d_flanke bezeichnet den Flankendurchmesser bei achteckigen Querschnitten
        d_flanke[i] = d_list_eingabe[i]/math.tan(math.pi/8)
        #print("Flankendurchmesser:" , d_flanke[i])
        #d_aussen bezeichnet den Aussendurchmesser bei achteckigen Querschnitten
        d_aussen[i] = d_list_eingabe[i]/(math.sin(math.pi/8))
        #print("Aussendurchmesser" , d_aussen[i])
else: #bei kreisförmigen Querschnitten sind d_flanke und d_aussen gleich
    d_flanke = d_list_eingabe.copy()
    d_aussen = d_list_eingabe.copy()

#Materialkennwerte
if material == 1:
    E = 210000*1000000 #in N/m^2
    rho = 7850 #in kg/m^3
elif material == 2:
    E = 210000*1000000 #in N/m^2
    rho = 7850 #in kg/m^3
elif material == 3:
    E = 210000*1000000 #in N/m^2
    rho = 7850 #in kg/m^3 
elif material == 4:
    E = 70000*1000000 #in N/m^2
    rho = 2700 #in kg/m^3

#Gemäss BA2023 wird T konservativ auf 3.5s geschätzt.
#beta, Beiwert für das dynamische Verhalten von Lichtmasten, gemäss SN-EN 40-3-1, 5.2.4
T = 3.5 
beta = 1.0024 - 0.005*T**4 + 0.05144*T**3 - 0.22793*T**2 + 0.67262*T
#print("beta:" , beta) #Kontrollausgabe ohne Funktion

#delta, Beiwert für die Mastgrösse, gemäss SN-EN 40-3-1, 5.2.3
delta = 1-0.01*hoehe
#print("delta:" , delta) #Kontrollausgabe ohne Funktion

#f, Topographiebeiwert, gemäss SN-EN 40-3-1, 5.2.5, f=1, ausser signifikante Topograpie
f = 1
#print("f:" , f) #Kontrollausgabe ohne Funktion

#wirksame Länge definieren
wirksame_laenge_tuere_list = []
for elem1, elem2 in zip(laenge_tuere_list, eckradius_tuere_list):
    differenz = elem1 - 0.43*elem2
    wirksame_laenge_tuere_list.append(differenz)
#if len(wirksame_laenge_tuere_list) > 0:
    #print("wirksame Länge Tür 1:" , wirksame_laenge_tuere_list[0])

#windzone
if windzone == 1:
    q_p0 = 0.9
elif windzone == 2:
    q_p0 = 1.1
elif windzone == 3:
    q_p0 = 1.3
elif windzone == 4:
    q_p0 = 2.4
elif windzone == 5:
    q_p0 = 2.7
elif windzone == 6 or windzone == 7:
    q_p0 = 3.3
rho_luft = 1.2 #Luftdiche (unter 1600m gemäss BA2023)
c_s = math.sqrt(0.91)
#print("q_p0:" , q_p0) #Kontrollausgabe ohne Funktion
#v_ref, berechnet gemöss BA2023, S.9
v_ref = math.sqrt( (2*q_p0*1000*1.6*((10/300)**0.16+0.375)**2)/((1+0.375*(450/10)**0.23)**2*rho_luft))
#print("v_ref:" , v_ref) #Kontrollausgabe ohne Funktion
#q_10, berechnet gemäss SN-En 40-3-1, 5.2.2
q_10 = 0.5*rho_luft*c_s**2*(v_ref)**2
#print("q_10:" , q_10) #Kontrollausgabe ohne Funktion
#gelaendekategorie
if gelaendekategorie == "2":
    z_g = 300
    alpha_r = 0.16
elif gelaendekategorie == "2a":
    z_g = 380
    alpha_r = 0.19
elif gelaendekategorie == "3":
    z_g = 450
    alpha_r = 0.23
elif gelaendekategorie == "4":
    z_g = 526
    alpha_r = 0.30
#Klasse Verschiebungen
if klasse_verschiebung == 1:
    verschiebung_zugelassen = 0.04
elif klasse_verschiebung == 2:
    verschiebung_zugelassen = 0.06
elif klasse_verschiebung == 3:
    verschiebung_zugelassen = 0.1

#Inputkontrolle
inputkontrolle = True
#if hoehe > 20:
#    inputkontrolle = False
#    sheet.append(["Die verwendete Norm SN-EN-40-3-1 gilt nur bis zu einer Höhe von 20 m."])
for i in range (len(z_list)):
    if z_list[i] > hoehe:
        inputkontrolle = False
        sheet.append(["Der Durchmesser bzw. die Seitenlänge wurde für eine zu grosse Höhe eingegeben."])
    if d_list_eingabe[i] < 0.01 or d_list_eingabe[i] > 0.8:
        inputkontrolle = False
        sheet.append(["Der Durchmesser bzw. die Seitenlänge liegt nicht im Bereich 1-80 cm."])
for i in range (len(z_list)-1):
    if d_list_eingabe[i] < d_list_eingabe[i+1]:
        inputkontrolle = False
        sheet.append(["Der Durchmesser des Mastes nimmt nach oben zu anstatt ab."])
if t < 0.001:
    inputkontrolle = False
    sheet.append(["Die Wandstärke liegt unter 1 mm."])
if t > 0.02:
    sheet.append(["Die Wandstärke liegt über 20 mm. Bitte überprüfen Sie, dass kein Fehler vorliegt."])
if anzahl_elemente > 1000:
    inputkontrolle = False
    sheet.append(["Bitte beschränken Sie die Anzahl Elemente auf maximal 1'000."])
for i in range (len(laenge_tuere_list)):
    if laenge_tuere_list[i] > 1 or laenge_tuere_list[i] < 0:
        inputkontrolle = False
        sheet.append(["Die Länge einer Tür liegt nicht im Bereich 0-1 m."])
    if eckradius_tuere_list[i] > 0.5*breite_tuere_list[i] or eckradius_tuere_list[i] < 0:
        inputkontrolle = False
        sheet.append(["Der Eckradius einer Tür liegt nicht im Bereich 0 bis halbe Türbreite."])
    if (dicke_verstaerkung_list[i] < 0.001 or dicke_verstaerkung_list[i] > 0.03) and dicke_verstaerkung_list[i] != 0:
        inputkontrolle = False
        sheet.append(["Die Dicke der Verstärkung einer Tür liegt nicht im Bereich 1-30 mm."])
    if (breite_verstaerkung_list[i] < 0.001 or breite_verstaerkung_list[i] > 0.1) and breite_verstaerkung_list[i] != 0:
        inputkontrolle = False
        sheet.append(["Die Breite der Verstärkung einer Tür liegt nicht im Bereich 1-100 mm."])
if A_x_leuchte < 0 or A_x_leuchte > 1 or A_y_leuchte < 0 or A_y_leuchte > 1:
    inputkontrolle = False
    sheet.append(["Die Fläche der Leuchte liegt nicht im Bereich 0-1 m^2."])
if m_leuchte < 0 or m_leuchte > 300:
    inputkontrolle = False
    sheet.append(["Die Masse der Leuchte liegt nicht im Bereich 0-300 kg."])
for i in range (len(z_zusatzmasse_list)):
    if A_x_zusatzmasse_list[i] < 0 or A_x_zusatzmasse_list[i] > 1 or A_y_zusatzmasse_list[i] < 0 or A_y_zusatzmasse_list[i] > 1:
        inputkontrolle = False
        sheet.append(["Die Fläche einer Zusatzmasse liegt nicht im Bereich 0-1 m^2."])
    if m_zusatzmasse_list[i] < 0 or m_zusatzmasse_list[i] > 300:
        inputkontrolle = False
        sheet.append(["Die Masse einer Zusatzmasse liegt nicht im Bereich 0-300 kg."])
    if z_zusatzmasse_list[i] > hoehe:
        inputkontrolle = False
        sheet.append(["Bei der Berechnung können nur Zusatzmassen berücksichtigt werden, die sich nicht über der Mastspitze befinden."])

#Beginn Berechnungnen
if inputkontrolle == True:
    #z_node enthält die Höhe [m] des Nodes
    z_node = [None] * (anzahl_elemente+1)
    #c_h, Profilbeiwert c_h von jedem Node(gemäss Höhe des Nodes) gemäss SIA 261, 6.2.1.2
    c_h_node = [None] * (anzahl_elemente+1)
    #c_e, Standortbeiwert, gemäss BA2023, S.10
    c_e_node = [None] * (anzahl_elemente+1)
    #q_p [N/m^2], Staudruck gemäss SIA 261, 6.2.1.1
    q_p_node = [None] * (anzahl_elemente+1)
    #q_z [N/m^2], charakteristischer Winddruck gemäss SN-EN 40-3-1, 5.2.1
    q_z_node = [None] * (anzahl_elemente+1)
    #d_node_flanke, Flankendurchmesser, bei kreisförmigen Querschnitten gleich d_node_aussen
    d_node_flanke = [None] * (anzahl_elemente+1)
    #d_node_aussen, Aussendurchmesser, bei kreisförmigen Querschnitten gleich d_node_flanke
    d_node_aussen = [None] * (anzahl_elemente+1)
    #delta_h
    delta_h_node = [None] * (anzahl_elemente+1)
    #v_Wind [m/s], Windgeschwindigkeit, gemäss SN_EN 40-3-1, 5.3.2, Koeffizienten gemäss BA2023, S.
    v_wind_node = [None] * (anzahl_elemente+1)
    #re, Reynoldszahl gemäss SN-EN 40-3-1, 5.3.2, mit Flankendurchmesser berechnet (achteckige Querschnitte)
    reynoldszahl_node = [None] * (anzahl_elemente+1)
    #r_achteck, Eckradius, Es wird davon ausgegegangen, dass r_achteckt unbekannt ist. Deshalb wird es konservatvi zu 0 gesetzt.
    r_achteck_node = [None] * (anzahl_elemente+1)
    #r/d =r_achteck/d_node_flanke gemäss SN_EN 40-3-1, 5.3.2, zur Verwendung von Bild 3
    r_durch_d_node = [None] * (anzahl_elemente+1)
    #c formbeiwert gemäss SN-EN 40-3-1, 5.3.2, Bild 3
    c_formbeiwert_node = [None] * (anzahl_elemente+1)
    #Fläche Mast, die Fläche des einem Node zugeordneten Mastabschnitts (Windangriffsfläche) [m^2]
    flaeche_mast_node = [None] * (anzahl_elemente+1)
    #Fläche Zusatzmassen und Leuchten pro Node, in x-Richtung [m^2]
    flaeche_zm_node_x = [0] * (anzahl_elemente+1)
    #Fläche Zusatzmassen und Leuchten pro Node, in y-Richtung [m^2]
    flaeche_zm_node_y = [0] * (anzahl_elemente+1)
    #Fläche total in x-Richtung, Addition der Flächen von Mast, Leuchte, Zusatzmasse pro Element [m^2]
    flaeche_tot_node_x = [None] * (anzahl_elemente+1)
    #Fläche total in y-Richtung, Addition der Flächen von Mast, Leuchte, Zusatzmasse pro Element [m^2]
    flaeche_tot_node_y = [None] * (anzahl_elemente+1)
    #Masse Mast, Masse des Mastelements, das zum Node zugeordnet wird [kg]
    masse_mast_node = [None] * (anzahl_elemente+1)
    #Masse Zusatzmassen und Leuchten pro Node [kg]
    masse_zm_node = [0] * (anzahl_elemente+1)
    #F_d_node, Windkraft [N] in x-Richtung auf charakteristischem Niveau pro Node
    f_d_node_x = [None] * (anzahl_elemente+1)
    #F_d_node, Windkraft [N] in y-Richtung auf charakteristischem Niveau pro Node
    f_d_node_y = [None] * (anzahl_elemente+1)

    for i in range (anzahl_elemente+1):
        #print(i) #Kontrollausgabe ohne Funktion
        z_node[i] = (hoehe/anzahl_elemente)*(i)
        #print("z_node:" , z_node[i]) #Kontrollausgabe ohne Funktion
        if gelaendekategorie in ["2","2a","3"]:
            if z_node[i] <= 5:
                z_temp = 5
            else:
                z_temp = z_node[i]
        if gelaendekategorie == "4":
            if z_node[i] <= 10:
                z_temp = 10
            elif z_node[i] > 30:
                z_g = 450
                alpha_r = 0.23
                z_temp == z_node[i]
            else:
                z_temp == z_node[i]
        c_h_node[i] = 1.6*((z_temp/z_g)**alpha_r+0.375)**2
        c_e_node[i] = c_h_node[i]/(1.6*( (10/300)**0.16+0.375)**2)*(1+0.375*(300/10)**0.16)**2
        q_z_node[i] = delta*beta*f*c_e_node[i]*q_10
        #print("q_z_node:" , q_z_node[i]) #Kontrollausgabe ohne Funktion
        if form == 3: # form = zylindrisch, d_node_flanke bzw. d_node_aussen werden entsprechend der Höhe bestimmt
            for j in range (len(z_list)):
                if z_list[j] <= z_node[i]:
                    d_node_flanke[i] = d_flanke[j]
                    d_node_aussen[i] = d_aussen[j]
                else:
                    break
        if form == 1 or form == 2: # form = konisch, lineare Interpolation
            d_node_flanke[i] = d_flanke[0] - ((d_flanke[0]-d_flanke[1])/(z_list[1]-z_list[0]))*(z_node[i]-z_list[0])
            d_node_aussen[i] = d_aussen[0] - ((d_aussen[0]-d_aussen[1])/(z_list[1]-z_list[0]))*(z_node[i]-z_list[0])
        if i == 0 or i == anzahl_elemente:
            delta_h_node[i] = 0.5*hoehe/anzahl_elemente
        else:
            delta_h_node[i] =  hoehe/anzahl_elemente
        v_wind_node[i] = 1/c_s*math.sqrt(q_z_node[i]/(rho_luft*beta*delta*0.5))
        reynoldszahl_node[i] = d_node_flanke[i]*v_wind_node[i]/(15.1*10**(-6))*10**(-5)
        if form == 2:
            r_achteck_node[i] = 0 #Eckradien sind nicht bekannt, werden konservativ so angenommen, dass r/D < 0.075
            r_durch_d_node[i] = r_achteck_node[i]/d_node_flanke[i]
            if r_durch_d_node[i] < 0.075: #Kurve 1, Bild 3, SN-EN 40-3-1
                if reynoldszahl_node[i] >= 3:
                    c_formbeiwert_node[i] = 1.3
                elif reynoldszahl_node[i] < 2.3:
                    c_formbeiwert_node[i] = 1.45
                else:
                    c_formbeiwert_node[i] = 1.45-(0.15/0.7)*(reynoldszahl_node[i]-2.3)
            else: # Kurve 2, Bild 3, SN-EN 40-3-1, in der aktuellen Version des codes wird nie Kurve 2 verwendet
                if reynoldszahl_node[i] >= 7:
                    c_formbeiwert_node[i] = 1.1
                elif reynoldszahl_node[i] < 2:
                    c_formbeiwert_node[i] = 1.29
                else:
                    c_formbeiwert_node[i] = 1.29-(0.19/5)*(reynoldszahl_node[i]-2)
        elif form == 1 or form == 3:
            r_achteck_node[i] = 0
            r_durch_d_node[i] = 0
            if reynoldszahl_node[i] > 4:
                c_formbeiwert_node[i] = 0.5 + (1/60)*(reynoldszahl_node[i]-4)
            elif reynoldszahl_node[i] > 2 and reynoldszahl_node[i] <= 4:
                c_formbeiwert_node[i] = 1.2 - 0.35*(reynoldszahl_node[i]-2)
            else:
                c_formbeiwert_node[i] = 1.2
        flaeche_mast_node[i] = delta_h_node[i]*d_node_aussen[i]*c_formbeiwert_node[i]
        #print("Fläche Mastabschnitt:" , flaeche_mast_node[i]) #Kontrollausgabe ohne Funktion
        for k in range (len(z_zusatzmasse_list)): #Falls eine Zusatzmasse gerade in der Mitte zwischen zwei Nodes liegt, wird sie gleichmässig auf die beiden Nodes aufgeteilt.
            if i == 0 and z_zusatzmasse_list[k] < delta_h_node[i]:
                flaeche_zm_node_x[i] += A_x_zusatzmasse_list[k]
                flaeche_zm_node_y[i] += A_y_zusatzmasse_list[k]
            elif i == 0 and z_zusatzmasse_list[k] == delta_h_node[i]:
                flaeche_zm_node_x[i] += 0.5*A_x_zusatzmasse_list[k]
                flaeche_zm_node_y[i] += 0.5*A_y_zusatzmasse_list[k]
            elif i == anzahl_elemente and z_zusatzmasse_list[k] <= hoehe and  z_zusatzmasse_list[k] > (hoehe-delta_h_node[i]):
                flaeche_zm_node_x[i] += A_x_zusatzmasse_list[k]
                flaeche_zm_node_y[i] += A_y_zusatzmasse_list[k]
            elif i == anzahl_elemente and z_zusatzmasse_list[k] == (hoehe-delta_h_node[i]):
                flaeche_zm_node_x[i] += 0.5*A_x_zusatzmasse_list[k]
                flaeche_zm_node_y[i] += 0.5*A_y_zusatzmasse_list[k]
            elif z_node[i]-(delta_h_node[i]/2) < z_zusatzmasse_list[k] and z_node[i]+(delta_h_node[i]/2) > z_zusatzmasse_list[k]:
                flaeche_zm_node_x[i] += A_x_zusatzmasse_list[k]
                flaeche_zm_node_y[i] += A_y_zusatzmasse_list[k]
            elif z_node[i]-(delta_h_node[i]/2) == z_zusatzmasse_list[k] or z_node[i]+(delta_h_node[i]/2) == z_zusatzmasse_list[k]:
                flaeche_zm_node_x[i] += 0.5*A_x_zusatzmasse_list[k]
                flaeche_zm_node_y[i] += 0.5*A_y_zusatzmasse_list[k]
        #Leuchte dazurechnen
        if i == anzahl_elemente:
            flaeche_zm_node_x[i] += A_x_leuchte
            flaeche_zm_node_y[i] += A_y_leuchte
        flaeche_tot_node_x[i] = flaeche_mast_node[i] + flaeche_zm_node_x[i]
        flaeche_tot_node_y[i] = flaeche_mast_node[i] + flaeche_zm_node_y[i]
        #print("Fläche total, x-Richtung:" , flaeche_tot_node_x[i])
        #print("Fläche total, y-Richtung:" , flaeche_tot_node_y[i])
        #Windkraft pro Node, auf charakteristischem Niveau (für Verformungen):
        f_d_node_x[i] = flaeche_tot_node_x[i]*q_z_node[i]
        f_d_node_y[i] = flaeche_tot_node_y[i]*q_z_node[i]
        #print("f_d_node_x:" , f_d_node_x[i]) #Kontrollausgabe ohne Funktion
        #print("f_d_node_y:" , f_d_node_y[i]) #Kontrollausgabe ohne Funktion
        
    #print()
#Berechnungen Schleife 2
    #z_m enthält die Höhe [m] des Mittelpunktes von jedem Element
    z_m = [0] * (anzahl_elemente)
    #d_m_flanke, Flankendurchmesser, bei kreisförmigen Querschnitten gleich d_m_aussen
    d_m_flanke = [0] * (anzahl_elemente)
    #d_m_aussen, Aussendurchmesser, bei kreisförmigen Querschnitten gleich d_m_flanke
    d_m_aussen = [0] * (anzahl_elemente)
    #d_seite_elementmitte, Seitenlänge aussen in der Mitte des Elements, wird nur für achteckige Querschnitte verwendet
    d_seite_elementmitte = [0] * (anzahl_elemente)
    #A, Querschnittsfläche in der Mitte eines Elements
    A = [0] * (anzahl_elemente)
    #L, Länge eines Elements
    L = hoehe/anzahl_elemente
    #teilt die Zusatzmassen dem nächsten node zu, falls die Zusatzmasse genau in der Mitte liegt, wird sie aufgeteilt
    masse_node_liste = [0] * (anzahl_elemente+1)
    #r_m_elementmitte, mittlerer Radius des Querschnitts in der Elementmitte
    r_m_elementmitte = [0] * (anzahl_elemente)
    #theta, halber Türöffnungswinkel gemäss SN-EN 40-3-3
    theta = [0] * (anzahl_elemente)
    #m_x, Abstand von der x-Achse zur Mastwandmitte, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_x = [0] * (anzahl_elemente)
    #m_0x, Abstand von der x-Achse zum Schwerpunkt der Türverstärkung, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_0x = [0] * (anzahl_elemente)
    #m_y, Abstand von dere y-Achse zur Mastwandmitte, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_y = [0] * (anzahl_elemente)
    #m_0y, Abstand von der y-Achse zum Schwerpunkt der Türverstärkung, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_0y = [0] * (anzahl_elemente)
    #z_offen, enthält die Höhen der Elemente, an welchen sich eine Tür befindet, ansonsten 0.
    z_offen = [0] * (anzahl_elemente)
    #breite_tuere_elementmitte, enthält die Breite der Tür, falls keine Tür, dann 0
    breite_tuere_elementmitte = [0] * (anzahl_elemente)
    #Breite der Verstärkung
    breite_verstaerkung_elementmitte = [0] * (anzahl_elemente)
    #Dicke der Verstärkung
    dicke_verstaerkung_elementmitte = [0] * (anzahl_elemente)
    #Ausrichtung, ist immmer x, ausser auf der Höhe einer Türöffnung mit Ausrichtung in y-Richtung, wird für die Berechnung von I verwendet.
    #ausrichtung_tuere_list enthält nur so viele Elemente wie Anzahl Türen, ausrichtung_tuere enthält für jedes Berechnungselement einen Wert
    ausrichtung_tuere = ["x"] * (anzahl_elemente)
    
    #I_x, Flächenträgheitsmoment des entsprechenden Querschnitts, um die x-Achse, gemäss SN-EN-40-3-3
    I_x = [0] * (anzahl_elemente)
    #I_y, Flächenträgheitsmoment des entsprechenden Querschnitts, um die y-Achse, gemäss SN-EN-40-3-3
    I_y = [0] * (anzahl_elemente)
    #Fläche in der Elementmitte für den kompletten Querschnitt, nur für Acheckquerschnitte verwendet
    flaeche_ganz_elementmitte = [0] * (anzahl_elemente)
    #Schwerpunktverschiebung des Querschnitts durch das Loch, nur für Achteckquerschnitte verwendet, darf nur bei unverstärkten QS in späteren Berechnungen angewendet werden!
    schwerpunktverschiebung_elementmitte = [0] * (anzahl_elemente)
    
    #Nun wird für jedes Element die oben definierten Werte ausgerechnet.
    for i in range (anzahl_elemente):
        #print(i) #Kontrollausgabe ohne Funktion
        z_m[i] = (hoehe/anzahl_elemente)*(i+0.5)
        z_m[i] = round(z_m[i],4)
        #print("z_m:" , z_m[i]) #Kontrollausgabe ohne Funktion
        if form == 3: # form = zylindrisch, d_m_flanke bzw. d_m_aussen werden entsprechend der Höhe bestimmt
            for j in range (len(z_list)):
                if z_list[j] <= z_m[i]:
                    d_m_flanke[i] = d_flanke[j]
                    d_m_aussen[i] = d_aussen[j]
        if form == 1 or form == 2: # form = konisch, lineare Interpolation
            d_m_flanke[i] = d_flanke[0] - ((d_flanke[0]-d_flanke[1])/(z_list[1]-z_list[0]))*(z_m[i]-z_list[0])
            d_m_aussen[i] = d_aussen[0] - ((d_aussen[0]-d_aussen[1])/(z_list[1]-z_list[0]))*(z_m[i]-z_list[0])
            d_seite_elementmitte[i] = d_list_eingabe[0] - ((d_list_eingabe[0]-d_list_eingabe[1])/(z_list[1]-z_list[0]))*(z_m[i]-z_list[0])
        #print("d_m_aussen[i]:", d_m_aussen[i])
        r_m_elementmitte[i] = (d_m_flanke[i]-t)/2
        if form == 1 or form == 3:
            A[i] = (d_m_aussen[i]**2-(d_m_aussen[i]-2*t)**2)*math.pi/4
        elif form == 2:
            A[i] = 8*t*(d_seite_elementmitte[i]-t/math.tan(3*math.pi/8))
        #print("Fläche:" , A[i])
    
        for k in range (len(z_zusatzmasse_list)): #Falls eine Zusatzmasse gerade in der Mitte eines Elements liegt, wird sie gleichmässig auf die beiden nodes aufgeteilt.
            if i == 0 and z_zusatzmasse_list[k] == 0:
                masse_node_liste[i] += m_zusatzmasse_list[k]
            elif i == anzahl_elemente and z_zusatzmasse_list[k] == hoehe: #damit Zusatzmassen an der Spitze sicher auch berücksichtigt werden
                masse_node_liste[i+1] += m_zusatzmasse_list[k]
            elif z_m[i]-L < z_zusatzmasse_list[k] and z_m[i] > z_zusatzmasse_list[k]:
                masse_node_liste[i] += m_zusatzmasse_list[k]
            elif z_m[i]-L == z_zusatzmasse_list[k] or z_m[i] == z_zusatzmasse_list[k]:
                masse_node_liste[i] += 0.5*m_zusatzmasse_list[k]
                if i == anzahl_elemente: #für den Fall, dass eine Masse auf die beiden obersten nodes aufgeteilt werden muss
                    masse_node_liste[i+1] += 0.5*m_zusatzmasse_list[k]
                
        #theta
        if tuer == "Ja" or tuer == "ja":
            for a in range (anzahl_tueren):
                if z_m[i] >= hoehe_tuere_list[a] and z_m[i] <= hoehe_tuere_list[a]+laenge_tuere_list[a]:
                    z_offen[i] = z_m[i]
                    #print("Hier ist eine Tür:" , z_offen[i])
                    breite_tuere_elementmitte[i] = breite_tuere_list[a]
                    ausrichtung_tuere[i] = ausrichtung_tuere_list[a]
                    if breite_tuere_list[a]/d_m_flanke[i] > 0.8:
                        #print("die Tür ist zu breit.")
                        inputkontrolle = False
                        sheet.append(["Die Breite einer Tür übersteigt 80% des Durchmessers auf dieser Höhe."])
                        break
                    if form == 1 or form == 3:
                        theta[i] = math.asin(breite_tuere_list[a]/d_m_flanke[i])          
                    elif form == 2:
                        #theta für Achteck:
                        if breite_tuere_list[a] <= d_seite_elementmitte[i]:
                            r_klein = 0.5*d_seite_elementmitte[i]*(1+math.sqrt(2))
                        elif breite_tuere_list[a] > d_seite_elementmitte[i]:
                            r_klein = 0.5*d_seite_elementmitte[i]*(1+math.sqrt(2)) - 0.5*(breite_tuere_list[a]-d_seite_elementmitte[i])
                        theta[i] = math.atan(breite_tuere_list[a]/2/r_klein)
                    if dicke_verstaerkung_list[a] != 0:  #überprüft ob es eine verstaerkung hat
                        breite_verstaerkung_elementmitte[i] = breite_verstaerkung_list[a]
                        dicke_verstaerkung_elementmitte[i] = dicke_verstaerkung_list[a]
                        if form == 2:
                            if breite_tuere_list[a] <= d_seite_elementmitte[i]:
                                m_x[i] = 0.5*d_seite_elementmitte[i]*(1+math.sqrt(2)) - 0.5*t
                                m_y[i] = 0.5*breite_tuere_list[a]
                            elif breite_tuere_list[a] > d_seite_elementmitte[i]:
                                m_x[i] = 0.5*d_seite_elementmitte[i]*(1+math.sqrt(2)) - 0.5*(breite_tuere_list[a]-d_seite_elementmitte[i]) - math.sqrt(2)/4*t
                                m_y[i] = 0.5*breite_tuere_list[a] - math.sqrt(2)/4*t
                            if breite_tuere_list[a] + 2*breite_verstaerkung_list[a] <= d_seite_elementmitte[i]:
                                m_0x[i] = 0.5*d_seite_elementmitte[i]*(1+math.sqrt(2)) - t - 0.5*dicke_verstaerkung_list[a]
                                m_0y[i] = m_y[i] + 0.5*breite_verstaerkung_list[a]
                            elif breite_tuere_list[a] <= d_seite_elementmitte[i]:
                                m_0x[i] = 0.5*d_seite_elementmitte[i]*(1+math.sqrt(2)) - (t+0.5*dicke_verstaerkung_list[a]+0.5*breite_verstaerkung_list[a])*math.sqrt(2)/2
                                m_0y[i] = 0.5*d_seite_elementmitte[i] - (t+0.5*dicke_verstaerkung_list[a])*math.sqrt(2)/2 + breite_verstaerkung_list[a]*math.sqrt(2)/4
                            elif breite_tuere_list[a] > d_seite_elementmitte[i]:
                                m_0x[i] = 0.5*d_seite_elementmitte[i]*(1+math.sqrt(2)) - 0.5*(breite_tuere_list[a]-d_seite_elementmitte[i]) - (t+0.5*dicke_verstaerkung_list[a]+0.5*breite_verstaerkung_list[a])*math.sqrt(2)/2
                                m_0y[i] = 0.5*breite_tuere_list[a] - (t+0.5*dicke_verstaerkung_list[a])*math.sqrt(2)/2 + breite_verstaerkung_list[a]*math.sqrt(2)/4
                        if form == 1 or form == 3:
                            m_x[i] = r_m_elementmitte[i]*math.cos(theta[i])
                            m_y[i] = r_m_elementmitte[i]*math.sin(theta[i])
                            m_0x[i] = m_x[i] - 0.5*breite_verstaerkung_list[a]*math.sin(theta[i]) - 0.5*(t+dicke_verstaerkung_list[a])*math.cos(theta[i])
                            m_0y[i] = m_y[i] - 0.5*(t+dicke_verstaerkung_list[a])*math.sin(theta[i]) + 0.5*breite_verstaerkung_list[a]*math.cos(theta[i])
                
            #print("Theta:" , theta[i])
            #print("Theta in Grad:", theta[i]*180/math.pi)
            #print("m_x:" , m_x[i])
            #print("m_0x:" , m_0x[i])
            #print("m_y:" , m_y[i])
            #print("m_0y:" , m_0y[i])
                 
        #Flächenträgheitsmoment berechnen
        if form == 2: #Achteck
            if theta[i] == 0:
                I_x[i] = (11+8*math.sqrt(2))/12 * ( (d_seite_elementmitte[i])**4 - (d_seite_elementmitte[i] - 2*t*math.tan(math.pi/8))**4)
                I_y[i] = I_x[i]
                #print("D:" , d_seite_elementmitte[i])
            elif theta[i] != 0:
                flaechentraegheitsmoment_ohne_loch = (11+8*math.sqrt(2))/12 * ( (d_seite_elementmitte[i])**4 - (d_seite_elementmitte[i] - 2*t*math.tan(math.pi/8))**4)
                flaeche_ganz_elementmitte[i] = 8*t*(d_seite_elementmitte[i]-t/math.tan(3*math.pi/8))
                if breite_tuere_elementmitte[i] <= d_seite_elementmitte[i]:
                    schwerpunktverschiebung_elementmitte[i] = -breite_tuere_elementmitte[i]*t*(d_seite_elementmitte[0]/(2*math.tan(math.pi/8)))/(flaeche_ganz_elementmitte[i] - breite_tuere_elementmitte[i]*t)
                    I_x[i] = flaechentraegheitsmoment_ohne_loch + flaeche_ganz_elementmitte[i]*schwerpunktverschiebung_elementmitte[i]**2 - 1/12*breite_tuere_elementmitte[i]*t**3 - breite_tuere_elementmitte[i]*t*( (d_seite_elementmitte[i]/(2*math.tan(math.pi/8))) -0-5*t - schwerpunktverschiebung_elementmitte[i] )**2
                    I_y[i] = flaechentraegheitsmoment_ohne_loch - 1/12*t*breite_tuere_elementmitte[i]**3
                    if breite_verstaerkung_elementmitte[i] != 0:  #überprüft ob es eine verstaerkung hat
                        flaeche_verstaerkung = breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]
                        schwerpunktverschiebung_neu = (-breite_tuere_elementmitte[i]*t*(d_seite_elementmitte[0]/(2*math.tan(math.pi/8))) + 2*flaeche_verstaerkung*m_0x[i])/(flaeche_ganz_elementmitte[i] - breite_tuere_elementmitte[i]*t + 2*flaeche_verstaerkung)
                        if breite_tuere_elementmitte[i] + 2*breite_verstaerkung_elementmitte[i] <= d_seite_elementmitte[i]:
                            beitrag1 = 2*(1/12*breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]**3 + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_neu)**2)
                            I_x[i] += (flaeche_ganz_elementmitte[i]-breite_tuere_elementmitte[i]*t)*(schwerpunktverschiebung_elementmitte[i]-schwerpunktverschiebung_neu)**2 + beitrag1
                            I_y[i] += 2*breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]*m_0y[i]**2 + 1/6*dicke_verstaerkung_elementmitte[i]*breite_verstaerkung_elementmitte[i]**3
                        elif breite_tuere_elementmitte[i] + 2*breite_verstaerkung_elementmitte[i] > d_seite_elementmitte[i]:
                            beitrag1 = 2*( 0.5*1/12*breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]**3 + 0.5*1/12*dicke_verstaerkung_elementmitte[i]*breite_verstaerkung_elementmitte[i]**2 + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_neu)**2 )
                            I_x[i] += (flaeche_ganz_elementmitte[i]-breite_tuere_elementmitte[i]*t)*(schwerpunktverschiebung_elementmitte[i]-schwerpunktverschiebung_neu)**2 + beitrag1
                            I_y[i] += 2*breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]*m_0y[i]**2 + 1/12*( breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]**3 + dicke_verstaerkung_elementmitte[i]*breite_verstaerkung_elementmitte[i]**3 )
                elif breite_tuere_elementmitte[i] > d_seite_elementmitte[i]:
                    #die Berechnung enthält leichte Vereinfachungen: der Schwerpunkt der Stirnfläche, welche nun aufgrund der Öffnung nicht mehr im Querschnitt enthalten ist, wurde in der Mitte der Dicke angenommen, die seitlichen Komponenten, welche nun nicht mehr vorhanden sind, wurden als Rechteck behandelt.
                    r_klein = d_seite_elementmitte[i]/(2*math.tan(math.pi/8))
                    breite_tuer = breite_tuere_elementmitte[i]
                    flaechenabzug1 = t*(d_seite_elementmitte[i]-t/(math.tan(3*math.pi/8)))
                    flaechenabzug2 = math.sqrt(2)/2*(breite_tuere_elementmitte[i]-d_seite_elementmitte[i])*t
                    flaechenabzug = flaechenabzug1 + 2*flaechenabzug2
                    schwerpunktverschiebung_elementmitte[i] = (-flaechenabzug1*(r_klein-0.5*t)-2*flaechenabzug2*(r_klein-0.5*t-0.5*0.5*(breite_tuer-d_seite_elementmitte[i])))/(flaeche_ganz_elementmitte[i]-flaechenabzug)
                    beitrag1 = 1/12*d_seite_elementmitte[i]*t**3 + flaechenabzug1*(r_klein-0.5*t-schwerpunktverschiebung_elementmitte[i])**2
                    beitrag2 = 2*( 0.5*1/12*math.sqrt(2)/2*(breite_tuer-d_seite_elementmitte[i]) *t**3 + 0.5*1/12*t * (math.sqrt(2)/2*(breite_tuer-d_seite_elementmitte[i]))**3 + flaechenabzug2*( r_klein-0.5*t-0.5*0.5*(breite_tuer-d_seite_elementmitte[i])-schwerpunktverschiebung_elementmitte[i])**2 )
                    I_x[i] = flaechentraegheitsmoment_ohne_loch + flaeche_ganz_elementmitte[i]*schwerpunktverschiebung_elementmitte[i]**2 - beitrag1 - beitrag2
                    beitrag_y_1 = -1/12*t*(d_seite_elementmitte[i] - t/(math.tan(3*math.pi/8)))**3 - math.sqrt(2)*t*(breite_tuer-d_seite_elementmitte[i]) * (d_seite_elementmitte[i]/4 + breite_tuer/4 - math.sqrt(2)/4*t)**2
                    beitrag_y_2 = -math.sqrt(2)/24*t**3*(breite_tuer-d_seite_elementmitte[i]) - math.sqrt(2)/48*t*(breite_tuer-d_seite_elementmitte[i])**3
                    I_y[i] = flaechentraegheitsmoment_ohne_loch + beitrag_y_1 + beitrag_y_2
                    if breite_verstaerkung_elementmitte[i] != 0:  #überprüft ob es eine verstaerkung hat
                        flaeche_verstaerkung = breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]
                        schwerpunktverschiebung_neu = (-flaechenabzug1*(r_klein-0.5*t)-2*flaechenabzug2*(r_klein-0.5*t-0.5*0.5*(breite_tuer-d_seite_elementmitte[i])) + 2*flaeche_verstaerkung*m_0x[i])/( flaeche_ganz_elementmitte[i]-flaechenabzug+2*flaeche_verstaerkung )
                        beitrag1 = 2*( 0.5*1/12*breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]**3 + 0.5*1/12*dicke_verstaerkung_elementmitte[i]*breite_verstaerkung_elementmitte[i]**2 + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_neu)**2 )
                        I_x[i] += (flaeche_ganz_elementmitte[i]-flaechenabzug)*(schwerpunktverschiebung_elementmitte[i]-schwerpunktverschiebung_neu)**2 + beitrag1
                        I_y[i] += 2*breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]*m_0y[i]**2 + 1/12*( breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]**3 + dicke_verstaerkung_elementmitte[i]*breite_verstaerkung_elementmitte[i]**3 )
        elif form == 1 or form == 3: #kreisförmiger Querschnitt
            if theta[i] == 0:
                I_x[i] = math.pi/4* ( (r_m_elementmitte[i]+(t/2))**4 - (r_m_elementmitte[i]-(t/2))**4 )
                I_y[i] = I_x[i]
            elif theta[i] != 0:
                r_aussen = r_m_elementmitte[i]+(t/2)
                r_innen = r_m_elementmitte[i]-(t/2)
                I_x[i] = 1/4*(r_aussen**4-r_innen**4)*(math.pi - theta[i] - math.sin(theta[i])*math.cos(theta[i]) ) + 4/9*(r_aussen**3 - r_innen**3)**2 * math.sin(theta[i])*math.sin(theta[i])* 1/( (r_aussen**2 - r_innen**2)*(math.pi-theta[i])  )
                I_y[i] = 1/4*(r_aussen**4-r_innen**4) * (math.pi - theta[i] + math.sin(theta[i])*math.cos(theta[i]))
                if breite_verstaerkung_elementmitte[i] != 0: #überprüft ob es eine verstaerkung hat
                    flaeche_verstaerkung = breite_verstaerkung_elementmitte[i]*dicke_verstaerkung_elementmitte[i]
                    #die folgende Verschiebung berechnet den Abstand vom Schwerpunkt zur x-Achse und nicht die reine Verschiebung des Schwerpunkts durch die Verstärkung.
                    schwerpunktverschiebung_elementmitte[i] = (2*flaeche_verstaerkung*m_0x[i] - (2/3*(r_aussen**3 - r_innen**3) * math.sin(theta[i])) ) /(2*flaeche_verstaerkung + (r_aussen**2 - r_innen**2)*(math.pi-theta[i]) )
                    beitrag1 = 2*( 1/12*dicke_verstaerkung_elementmitte[i]**3 *breite_verstaerkung_elementmitte[i] *math.cos(theta[i])*math.cos(theta[i]) + 1/12*breite_verstaerkung_elementmitte[i]**3 *dicke_verstaerkung_elementmitte[i] *math.sin(theta[i])*math.sin(theta[i]) + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_elementmitte[i])**2)
                    beitrag2 = (math.pi-theta[i])*(r_aussen**2 - r_innen**2)* (-2/3*(r_aussen**3 - r_innen**3)*math.sin(theta[i])/((r_aussen**2 - r_innen**2)*(math.pi-theta[i]))   + schwerpunktverschiebung_elementmitte[i] )**2
                    I_x[i] += beitrag2 - beitrag1
                    I_y[i] += 2*flaeche_verstaerkung*m_0y[i]**2 + 1/6*( breite_verstaerkung_elementmitte[i]**3 *dicke_verstaerkung_elementmitte[i] *math.cos(theta[i])**2 + dicke_verstaerkung_elementmitte[i]**3 *breite_verstaerkung_elementmitte[i] *math.sin(theta[i])**2 )
        if ausrichtung_tuere[i] == "y":
            I_x[i], I_y[i] = I_y[i], I_x[i]
        #print("Flächenträgheitsmoment I_x:" , I_x[i])
        #print("Flächenträgheitsmoment I_y:" , I_y[i])
        #print()

#Mastmodellierung
    #die folgende Berechnung wird 2 mal durchgeführt: zuerst um die x-Achse, danach um die y-Achse
    for achse in range (2):
        #I, Flächenträgheitsmoment um die x-Achse oder um die y-Achse, je nach Berechnungsrichtung
        I = [0] * (anzahl_elemente)
        for i in range (anzahl_elemente):
            if achse == 0:
                I[i] = I_x[i]
            if achse == 1:
                I[i] = I_y[i]
        anzahl_nodes = anzahl_elemente + 1
        anzahl_dof = 3*anzahl_nodes
        k_matrix_1 = np.zeros( (anzahl_dof,anzahl_dof) )
        m_matrix_1 = np.zeros( (anzahl_dof,anzahl_dof) )
        for i in range (anzahl_elemente):
            k_1a = np.array( [ [E*A[i]/L, 0, 0],
                             [0, 12*E*I[i]/(L**3), 6*E*I[i]/(L**2)],
                             [0, 6*E*I[i]/(L**2), 4*E*I[i]/L] ] )
            k_1b = np.array( [ [-E*A[i]/L, 0, 0],
                             [0, -12*E*I[i]/(L**3), 6*E*I[i]/(L**2)],
                             [0, -6*E*I[i]/(L**2), 2*E*I[i]/L] ] )
            k_1c = np.array( [ [-E*A[i]/L, 0, 0],
                             [0, -12*E*I[i]/(L**3), -6*E*I[i]/(L**2)],
                             [0, 6*E*I[i]/(L**2), 2*E*I[i]/L] ] )
            k_1d = np.array( [ [E*A[i]/L, 0, 0],
                             [0, 12*E*I[i]/(L**3), -6*E*I[i]/(L**2)],
                             [0, -6*E*I[i]/(L**2), 4*E*I[i]/L] ] )
            
            k_matrix_3_dof = np.array( [ [k_1a[0][0], k_1a[0][1], k_1a[0][2], k_1b[0][0], k_1b[0][1], k_1b[0][2] ],
                                         [k_1a[1][0], k_1a[1][1], k_1a[1][2], k_1b[1][0], k_1b[1][1], k_1b[1][2] ],
                                         [k_1a[2][0], k_1a[2][1], k_1a[2][2], k_1b[2][0], k_1b[2][1], k_1b[2][2] ],
                                         [k_1c[0][0], k_1c[0][1], k_1c[0][2], k_1d[0][0], k_1d[0][1], k_1d[0][2] ],
                                         [k_1c[1][0], k_1c[1][1], k_1c[1][2], k_1d[1][0], k_1d[1][1], k_1d[1][2] ],
                                         [k_1c[2][0], k_1c[2][1], k_1c[2][2], k_1d[2][0], k_1d[2][1], k_1d[2][2] ] ] )
            
            m_1a = np.array( [ [1/3*rho*A[i]*L, 0, 0],
                             [0, 13/35*rho*A[i]*L, 11*L/210*rho*A[i]*L],
                             [0, 11*L/210*rho*A[i]*L, L**2/105*rho*A[i]*L] ] )
            m_1b = np.array( [ [1/6*rho*A[i]*L, 0, 0],
                             [0, 9/70*rho*A[i]*L, -13*L/420*rho*A[i]*L],
                             [0, 13*L/420*rho*A[i]*L, -L**2/140*rho*A[i]*L] ] )
            m_1c = np.array( [ [1/6*rho*A[i]*L, 0, 0],
                             [0, 9/70*rho*A[i]*L, 13*L/420*rho*A[i]*L],
                             [0, -13*L/420*rho*A[i]*L, -L**2/140*rho*A[i]*L] ] )
            m_1d = np.array( [ [1/3*rho*A[i]*L, 0, 0],
                             [0, 13/35*rho*A[i]*L, -11*L/210*rho*A[i]*L],
                             [0, -11*L/210*rho*A[i]*L, L**2/105*rho*A[i]*L] ] )
        
            m_matrix_3_dof = np.array( [ [m_1a[0][0], m_1a[0][1], m_1a[0][2], m_1b[0][0], m_1b[0][1], m_1b[0][2] ],
                                         [m_1a[1][0], m_1a[1][1], m_1a[1][2], m_1b[1][0], m_1b[1][1], m_1b[1][2] ],
                                         [m_1a[2][0], m_1a[2][1], m_1a[2][2], m_1b[2][0], m_1b[2][1], m_1b[2][2] ],
                                         [m_1c[0][0], m_1c[0][1], m_1c[0][2], m_1d[0][0], m_1d[0][1], m_1d[0][2] ],
                                         [m_1c[1][0], m_1c[1][1], m_1c[1][2], m_1d[1][0], m_1d[1][1], m_1d[1][2] ],
                                         [m_1c[2][0], m_1c[2][1], m_1c[2][2], m_1d[2][0], m_1d[2][1], m_1d[2][2] ] ] )
            
            for j in range (6):
                for q in range (6):
                    k_matrix_1[3*i+j][3*i+q] += k_matrix_3_dof[j][q]
                    m_matrix_1[3*i+j][3*i+q] += m_matrix_3_dof[j][q]
        #print("k matrix_1 ohne Randbedingungen:")
        #print(k_matrix_1)
        #print("m matrix_1 ohne Randbedingungen:")
        #print(m_matrix_1)
        
        #Zusatzmassen und Leuchte an der Spitze hinzufügen
        #Zusatzmassen
        #print("Extramassen:" , masse_node_liste)
        for i in range (anzahl_nodes):
            m_matrix_1[3*i][3*i] += masse_node_liste[i]
            m_matrix_1[3*i+1][3*i+1] += masse_node_liste[i]
        #Leuchte
        m_matrix_1[anzahl_dof-3][anzahl_dof-3] += m_leuchte
        m_matrix_1[anzahl_dof-2][anzahl_dof-2] += m_leuchte

        #Kraftvektor (nur Windkraft) erstellen
        f_vektor_1 = np.zeros(anzahl_dof)
        for i in range (anzahl_nodes):
            if achse == 0:
                f_vektor_1[3*i+1] = f_d_node_x[i]
            if achse == 1:
                f_vektor_1[3*i+1] = f_d_node_y[i]
        #print("Kraftvektor F ohne Randbedingungen:" , f_vektor_1)
        
        #dofs, die durch einspannung gehalten werden, löschen
        dof_gehalten = [0,1,2] #mit 2: biegesteif eingespannt
        anzahl_dof_gehalten = len(dof_gehalten)
        m_matrix = np.zeros( (anzahl_dof-anzahl_dof_gehalten,anzahl_dof-anzahl_dof_gehalten) )
        k_matrix = np.zeros( (anzahl_dof-anzahl_dof_gehalten,anzahl_dof-anzahl_dof_gehalten) )
        f_vektor = np.zeros(anzahl_dof-anzahl_dof_gehalten)
        a = 0
        for i in range (anzahl_dof):
            b = 0
            if i not in dof_gehalten:
                f_vektor[a] = f_vektor_1[i]
                for j in range (anzahl_dof):
                    if j not in dof_gehalten:
                        m_matrix[a][b]  = m_matrix_1[i][j]
                        k_matrix[a][b]  = k_matrix_1[i][j]
                        b += 1
                a += 1
        #print("k_matrix mit Randbedingungen:")
        #print(k_matrix)
        #print("m_matrix mit Randbedingungen:")
        #print(m_matrix)
        #print("f_vektor mit Randbedingungen:")
        #print(f_vektor)

#statische Deformation berechnen
        u_statisch = np.zeros(anzahl_dof-anzahl_dof_gehalten)
        k_matrix_invers = np.linalg.inv(k_matrix)
        u_statisch = np.dot(k_matrix_invers,f_vektor)
        #print("u_statisch:" , u_statisch)
        u_gross = np.zeros(anzahl_dof)
        c = 0
        for i in range (anzahl_dof):
            if i in dof_gehalten:
                u_gross[i] = 0
                c += 1
            else:
                u_gross[i] = u_statisch[i-c]
        #print("u_gross:" , u_gross)
        u_horizontal = np.zeros(anzahl_nodes)
        for i in range (anzahl_nodes):
            u_horizontal[i] = u_gross[3*i+1]
        #print("u_horizontal:" , u_horizontal)
        if achse == 0:
            #print("zulässige horizontale Verschiebung:" , round(verschiebung_zugelassen*hoehe*1000,2) , "mm")
            #print("Die horizontale Verschiebung der Mastspitze in x-Richtung ist:" , round(u_horizontal[anzahl_nodes-1]*1000,2) , "mm")
            sheet.append(["zulässige horizontale Verschiebung [mm]:" , round(verschiebung_zugelassen*hoehe*1000,2) ])
            sheet.append(["horizontale Verschiebung, x-Richtung [mm]:" , round(u_horizontal[anzahl_nodes-1]*1000,2) ])
        if achse == 1:
            #print("zulässige horizontale Verschiebung:" , round(verschiebung_zugelassen*hoehe*1000,2) , "mm")
            #print("Die horizontale Verschiebung der Mastspitze in y-Richtung ist:" , round(u_horizontal[anzahl_nodes-1]*1000,2) , "mm")
            sheet.append(["zulässige horizontale Verschiebung [mm]:" , round(verschiebung_zugelassen*hoehe*1000,2) ])
            sheet.append(["horizontale Verschiebung, y-Richtung [mm]:" , round(u_horizontal[anzahl_nodes-1]*1000,2) ])
        if u_horizontal[anzahl_nodes-1] <= verschiebung_zugelassen*hoehe:
            #print("horizontale Verformungen i.O.")
            sheet.append(["horizontale Verformungen i.O."])
        else:
            #print("horizontale Verformungen zu gross.")
            sheet.append(["horizontale Verformungen zu gross."])
        #Deformation plotten
        Masthoehe = []
        for i in range(anzahl_nodes):
            Masthoehe.append(L*i)
        plt.plot(u_horizontal,Masthoehe)
        plt.xlabel('horizontale Verschiebung [m]')
        plt.ylabel('Masthöhe')
        if achse == 0:
            plt.title('Deformation x-Richtung ohne Berücksichtigung der Einspannung')
        if achse == 1:
            plt.title('Deformation y-Richtung ohne Berücksichtigung der Einspannung')
        plt.grid(True)  #Raster hinzufügen
        if u_horizontal[anzahl_nodes-1] < 1.1:
            plt.xlim(-1.2, 1.2) #darzustellenden Abschnitt der x-Achse fixieren
        else:
            plt.xlim(-u_horizontal[anzahl_nodes-1]+0.2,u_horizontal[anzahl_nodes-1]+0.2)
        #plot in excel darstellen
        anker_zelle_spalte = chr(ord('E') + 10*achse)
        if erfüllt == True:
            anker_zelle = f'{anker_zelle_spalte}23'
        else:
            anker_zelle = f'{anker_zelle_spalte}44'
        #print("ankerzelle" , anker_zelle)
        plot_image = BytesIO()
        plt.savefig(plot_image, format='png')
        plot_image.seek(0)
        img = Image(plot_image)
        img.anchor = anker_zelle
        sheet.add_image(img)
        #
        #plt.show()
        plt.clf()
        
#Eigenfrequenzen und -modi berechnen
        D, V = np.linalg.eig(np.dot(np.linalg.inv(m_matrix), k_matrix))
        #D = eigenwerte, V = eigenvektoren
        #print("D:" , D)
        #print("V:" , V) #eigenmodi sind Spalten in der V-matrix
        sortiert_D = sorted(D)
        #print("sortiert_D:")
        #print(sortiert_D)
        transponiert_V = np.transpose(V) #jetzt sind die eigenmodi Zeilen in der transponierten V-matrix
        #print("transponiert_V:")
        #print(transponiert_V)
        sortiert_V = np.zeros( (len(D),len(D)) )
        for i in range (len(D)):
            for j in range (len(D)):
                if sortiert_D[i] == D[j]:
                    sortiert_V[i] = transponiert_V[j]
        #print("sortiert_V:")
        #print(sortiert_V)
        normalisiert_V = np.zeros( (len(D),len(D)) )
        for i in range (len(D)):
            max_verschiebung = max(sortiert_V[i], key=abs)
            if max_verschiebung != 0:
                ratio = 1/max_verschiebung
                ratio = abs(ratio)
                normalisiert_V[i] = [x*ratio for x in sortiert_V[i]]
            else:
                normalisiert_V[i] = sortiert_V[i]
        #print("normalisiert_V:")
        #print(normalisiert_V)
        eigenfrequenzen = sortiert_D
        eigenfrequenzen = [math.sqrt(x)/(2*math.pi) for x in eigenfrequenzen]
        #print("Eigenfrequenzen:")
        #print(eigenfrequenzen)
        
        #die gehaltenen dof zu den Eigenmodi hinzufügen
        normalisiert_V_gross = np.zeros( (len(D),anzahl_dof) )
        for i in range (len(D)):
            a = 0
            for j in range (anzahl_dof):
                if j in dof_gehalten:
                    normalisiert_V_gross[i][j] = 0
                    a += 1
                else:
                    normalisiert_V_gross[i][j] = normalisiert_V[i][j-a]
    
        if inputkontrolle == True:
            #Eigenmodi plotten
            Masthoehe = []
            for i in range(anzahl_nodes):
                Masthoehe.append(L*i)
            auslenkung = np.zeros( (len(D),anzahl_nodes) )
            for i in range (len(D)):
                for j in range (anzahl_nodes):
                    auslenkung[i][j] = normalisiert_V_gross[i][3*j+1]
            #print("auslenkung")
            #print(auslenkung)
            if achse == 0:
                sheet.append(["Eigenfrequenzen in x-Richtung:"])
            if achse == 1:
                sheet.append(["Eigenfrequenzen in y-Richtung:"])
            
            ##for i in range (len(D)):
            anker_zelle_spalte_liste = ['E','O','Y','AI','AS']
            for i in range(5): #Jetzt werden nur die ersten 5 geplottet.
                plt.plot(auslenkung[i],Masthoehe)
                plt.xlabel('Auslenkung [m]')
                plt.ylabel('Masthöhe [m]')
                str_i = str(i+1)
                str_eigenfrequenzen = str(round(eigenfrequenzen[i],4))
                if achse == 0:
                    plt.title('Eigenmodus ' + str_i + ' (x-Richtung), f = ' + str_eigenfrequenzen + ' Hz (ohne Bodenfeder)')
                if achse == 1:
                    plt.title('Eigenmodus ' + str_i + ' (y-Richtung), f = ' + str_eigenfrequenzen + ' Hz (ohne Bodenfeder)')
                plt.grid(True)  #Raster hinzufügen
                plt.xlim(-1.2, 1.2) #darzustellenden Abschnitt der x-Achse fixieren
                #plot in excel darstellen
                anker_zelle_spalte = anker_zelle_spalte_liste[i]
                if erfüllt == True:
                    anker_zelle_zeile = 49 + achse*26
                else:
                    anker_zelle_zeile = 70 + achse*26
                anker_zelle = f'{anker_zelle_spalte}{anker_zelle_zeile}'
                #print("ankerzelle" , anker_zelle)
                plot_image = BytesIO()
                plt.savefig(plot_image, format='png')
                plot_image.seek(0)
                img = Image(plot_image)
                img.anchor = anker_zelle
                sheet.add_image(img)
                #
                #plt.show()
                plt.clf()
                sheet.append(["Eigenfrequenz" , i+1 , str_eigenfrequenzen, "Hz" ])
        
#iterative Berechnung der Steifigkeit der Einspannung
    if erfüllt == False:
        k_bodenfeder = 10000 #in [Nm/rad]
        anzahl_iterationen = 0
        if entscheidungsachse == "x":
            achse = 0
            f_1_gemessen = f_1_gemessen_x
        else:
            achse = 1
            f_1_gemessen = f_1_gemessen_y
        #print("Entscheidungsachse:" , entscheidungsachse)
        #print("erfüllt:" , erfüllt)
        veraenderung = 1000000 #um so viel [Nm/rad] wird der Wert für k_bodenfeder verändert, später halbiert sich die Grösse der Veränderungen.
        groesser = True #gibt an, in welche Richtung der Wert von k_bodenfeder im vorherigen Schritt verändert wurde
        for q in range (50):
            #print("Iteration wird durchgeführt.")
            anzahl_iterationen += 1
            #print("Achse: " , achse)
            for i in range (anzahl_elemente):
                if achse == 0:
                    I[i] = I_x[i]
                if achse == 1:
                    I[i] = I_y[i]
            anzahl_nodes = anzahl_elemente + 1
            anzahl_dof = 3*anzahl_nodes
            k_matrix_1 = np.zeros( (anzahl_dof,anzahl_dof) )
            m_matrix_1 = np.zeros( (anzahl_dof,anzahl_dof) )
            for i in range (anzahl_elemente):
                k_1a = np.array( [ [E*A[i]/L, 0, 0],
                                 [0, 12*E*I[i]/(L**3), 6*E*I[i]/(L**2)],
                                 [0, 6*E*I[i]/(L**2), 4*E*I[i]/L] ] )
                k_1b = np.array( [ [-E*A[i]/L, 0, 0],
                                 [0, -12*E*I[i]/(L**3), 6*E*I[i]/(L**2)],
                                 [0, -6*E*I[i]/(L**2), 2*E*I[i]/L] ] )
                k_1c = np.array( [ [-E*A[i]/L, 0, 0],
                                 [0, -12*E*I[i]/(L**3), -6*E*I[i]/(L**2)],
                                 [0, 6*E*I[i]/(L**2), 2*E*I[i]/L] ] )
                k_1d = np.array( [ [E*A[i]/L, 0, 0],
                                 [0, 12*E*I[i]/(L**3), -6*E*I[i]/(L**2)],
                                 [0, -6*E*I[i]/(L**2), 4*E*I[i]/L] ] )
                
                k_matrix_3_dof = np.array( [ [k_1a[0][0], k_1a[0][1], k_1a[0][2], k_1b[0][0], k_1b[0][1], k_1b[0][2] ],
                                             [k_1a[1][0], k_1a[1][1], k_1a[1][2], k_1b[1][0], k_1b[1][1], k_1b[1][2] ],
                                             [k_1a[2][0], k_1a[2][1], k_1a[2][2], k_1b[2][0], k_1b[2][1], k_1b[2][2] ],
                                             [k_1c[0][0], k_1c[0][1], k_1c[0][2], k_1d[0][0], k_1d[0][1], k_1d[0][2] ],
                                             [k_1c[1][0], k_1c[1][1], k_1c[1][2], k_1d[1][0], k_1d[1][1], k_1d[1][2] ],
                                             [k_1c[2][0], k_1c[2][1], k_1c[2][2], k_1d[2][0], k_1d[2][1], k_1d[2][2] ] ] )
                
                m_1a = np.array( [ [1/3*rho*A[i]*L, 0, 0],
                                 [0, 13/35*rho*A[i]*L, 11*L/210*rho*A[i]*L],
                                 [0, 11*L/210*rho*A[i]*L, L**2/105*rho*A[i]*L] ] )
                m_1b = np.array( [ [1/6*rho*A[i]*L, 0, 0],
                                 [0, 9/70*rho*A[i]*L, -13*L/420*rho*A[i]*L],
                                 [0, 13*L/420*rho*A[i]*L, -L**2/140*rho*A[i]*L] ] )
                m_1c = np.array( [ [1/6*rho*A[i]*L, 0, 0],
                                 [0, 9/70*rho*A[i]*L, 13*L/420*rho*A[i]*L],
                                 [0, -13*L/420*rho*A[i]*L, -L**2/140*rho*A[i]*L] ] )
                m_1d = np.array( [ [1/3*rho*A[i]*L, 0, 0],
                                 [0, 13/35*rho*A[i]*L, -11*L/210*rho*A[i]*L],
                                 [0, -11*L/210*rho*A[i]*L, L**2/105*rho*A[i]*L] ] )
            
                m_matrix_3_dof = np.array( [ [m_1a[0][0], m_1a[0][1], m_1a[0][2], m_1b[0][0], m_1b[0][1], m_1b[0][2] ],
                                             [m_1a[1][0], m_1a[1][1], m_1a[1][2], m_1b[1][0], m_1b[1][1], m_1b[1][2] ],
                                             [m_1a[2][0], m_1a[2][1], m_1a[2][2], m_1b[2][0], m_1b[2][1], m_1b[2][2] ],
                                             [m_1c[0][0], m_1c[0][1], m_1c[0][2], m_1d[0][0], m_1d[0][1], m_1d[0][2] ],
                                             [m_1c[1][0], m_1c[1][1], m_1c[1][2], m_1d[1][0], m_1d[1][1], m_1d[1][2] ],
                                             [m_1c[2][0], m_1c[2][1], m_1c[2][2], m_1d[2][0], m_1d[2][1], m_1d[2][2] ] ] )
                
                for j in range (6):
                    for q in range (6):
                        k_matrix_1[3*i+j][3*i+q] += k_matrix_3_dof[j][q]
                        m_matrix_1[3*i+j][3*i+q] += m_matrix_3_dof[j][q]
            
            #Zusatzmassen und Leuchte an der Spitze hinzufügen
            #Zusatzmassen
            for i in range (anzahl_nodes):
                m_matrix_1[3*i][3*i] += masse_node_liste[i]
                m_matrix_1[3*i+1][3*i+1] += masse_node_liste[i]
            #Leuchte
            m_matrix_1[anzahl_dof-3][anzahl_dof-3] += m_leuchte
            m_matrix_1[anzahl_dof-2][anzahl_dof-2] += m_leuchte
            
            k_matrix_1[2][2] += k_bodenfeder
            
            #dofs, die durch Einspannung gehalten werden, löschen
            dof_gehalten = [0,1] #mit 2: biegesteif eingespannt
            anzahl_dof_gehalten = len(dof_gehalten)
            m_matrix = np.zeros( (anzahl_dof-anzahl_dof_gehalten,anzahl_dof-anzahl_dof_gehalten) )
            k_matrix = np.zeros( (anzahl_dof-anzahl_dof_gehalten,anzahl_dof-anzahl_dof_gehalten) )
            f_vektor = np.zeros(anzahl_dof-anzahl_dof_gehalten)
            a = 0
            for i in range (anzahl_dof):
                b = 0
                if i not in dof_gehalten:
                    f_vektor[a] = f_vektor_1[i]
                    for j in range (anzahl_dof):
                        if j not in dof_gehalten:
                            m_matrix[a][b]  = m_matrix_1[i][j]
                            k_matrix[a][b]  = k_matrix_1[i][j]
                            b += 1
                    a += 1
            
            #Eigenfrequenzen und -modi berechnen
            D, V = np.linalg.eig(np.dot(np.linalg.inv(m_matrix), k_matrix))
            #D = eigenwerte, V = eigenvektoren
            sortiert_D = sorted(D)
            transponiert_V = np.transpose(V) #jetzt sind die eigenmodi Zeilen in der transponierten V-matrix
            sortiert_V = np.zeros( (len(D),len(D)) )
            for i in range (len(D)):
                for j in range (len(D)):
                    if sortiert_D[i] == D[j]:
                        sortiert_V[i] = transponiert_V[j]
            normalisiert_V = np.zeros( (len(D),len(D)) )
            for i in range (len(D)):
                max_verschiebung = max(sortiert_V[i], key=abs)
                if max_verschiebung != 0:
                    ratio = 1/max_verschiebung
                    ratio = abs(ratio)
                    normalisiert_V[i] = [x*ratio for x in sortiert_V[i]]
                else:
                    normalisiert_V[i] = sortiert_V[i]
            eigenfrequenzen = sortiert_D
            eigenfrequenzen = [math.sqrt(x)/(2*math.pi) for x in eigenfrequenzen]
            #print("Anzahl Iterationen:" , anzahl_iterationen)
            #print("Eigenfrequenz:" , eigenfrequenzen[0])
            #print("K Bodenfeder:" , k_bodenfeder)
            if eigenfrequenzen[0] < f_1_gemessen + 0.001 and eigenfrequenzen[0] > f_1_gemessen - 0.001:
                #print("geschafft")
                break
            if eigenfrequenzen[0] < f_1_gemessen:
                if groesser == False:
                    veraenderung = veraenderung/2
                k_bodenfeder += veraenderung
                groesser = True
            if eigenfrequenzen[0] > f_1_gemessen:
                if groesser == True:
                    veraenderung = veraenderung/2
                    #print("asdfadsf")
                k_bodenfeder -= veraenderung
                groesser = False

#statische Deformation, Eigenfrequenzen und -modi mit der berechneten Steifigkeit berechnen
        #jetzt wurde k_bodenfeder bestimmt: Die gesamte berechnung wird noch einmal mit k_Bodenfeder durchgeführt und ausgegeben
        #print("Resultate unter Berücksichtigung der Einspannung im Boden:")
        #print("Federsteifigkeit der Einspannung [kNm/rad]:" , k_bodenfeder/1000)
        sheet.append([])
        sheet.append(["Resultate unter Berücksichtigung der Einspannung im Boden:"])
        sheet.append(["Federsteifigkeit der Einspannung [kNm/rad]:" , k_bodenfeder/1000])
        #die folgende Berechnung wird 2 mal durchgeführt: zuerst um die x-Achse, danach um die y-Achse
        for achse in range (2):
            #I, Flächenträgheitsmoment um die x-Achse oder um die y-Achse, je nach Berechnungsrichtung
            I = [0] * (anzahl_elemente)
            for i in range (anzahl_elemente):
                if achse == 0:
                    I[i] = I_x[i]
                if achse == 1:
                    I[i] = I_y[i]
            anzahl_nodes = anzahl_elemente + 1
            anzahl_dof = 3*anzahl_nodes
            k_matrix_1 = np.zeros( (anzahl_dof,anzahl_dof) )
            m_matrix_1 = np.zeros( (anzahl_dof,anzahl_dof) )
            for i in range (anzahl_elemente):
                k_1a = np.array( [ [E*A[i]/L, 0, 0],
                                 [0, 12*E*I[i]/(L**3), 6*E*I[i]/(L**2)],
                                 [0, 6*E*I[i]/(L**2), 4*E*I[i]/L] ] )
                k_1b = np.array( [ [-E*A[i]/L, 0, 0],
                                 [0, -12*E*I[i]/(L**3), 6*E*I[i]/(L**2)],
                                 [0, -6*E*I[i]/(L**2), 2*E*I[i]/L] ] )
                k_1c = np.array( [ [-E*A[i]/L, 0, 0],
                                 [0, -12*E*I[i]/(L**3), -6*E*I[i]/(L**2)],
                                 [0, 6*E*I[i]/(L**2), 2*E*I[i]/L] ] )
                k_1d = np.array( [ [E*A[i]/L, 0, 0],
                                 [0, 12*E*I[i]/(L**3), -6*E*I[i]/(L**2)],
                                 [0, -6*E*I[i]/(L**2), 4*E*I[i]/L] ] )
                
                k_matrix_3_dof = np.array( [ [k_1a[0][0], k_1a[0][1], k_1a[0][2], k_1b[0][0], k_1b[0][1], k_1b[0][2] ],
                                             [k_1a[1][0], k_1a[1][1], k_1a[1][2], k_1b[1][0], k_1b[1][1], k_1b[1][2] ],
                                             [k_1a[2][0], k_1a[2][1], k_1a[2][2], k_1b[2][0], k_1b[2][1], k_1b[2][2] ],
                                             [k_1c[0][0], k_1c[0][1], k_1c[0][2], k_1d[0][0], k_1d[0][1], k_1d[0][2] ],
                                             [k_1c[1][0], k_1c[1][1], k_1c[1][2], k_1d[1][0], k_1d[1][1], k_1d[1][2] ],
                                             [k_1c[2][0], k_1c[2][1], k_1c[2][2], k_1d[2][0], k_1d[2][1], k_1d[2][2] ] ] )
                
                m_1a = np.array( [ [1/3*rho*A[i]*L, 0, 0],
                                 [0, 13/35*rho*A[i]*L, 11*L/210*rho*A[i]*L],
                                 [0, 11*L/210*rho*A[i]*L, L**2/105*rho*A[i]*L] ] )
                m_1b = np.array( [ [1/6*rho*A[i]*L, 0, 0],
                                 [0, 9/70*rho*A[i]*L, -13*L/420*rho*A[i]*L],
                                 [0, 13*L/420*rho*A[i]*L, -L**2/140*rho*A[i]*L] ] )
                m_1c = np.array( [ [1/6*rho*A[i]*L, 0, 0],
                                 [0, 9/70*rho*A[i]*L, 13*L/420*rho*A[i]*L],
                                 [0, -13*L/420*rho*A[i]*L, -L**2/140*rho*A[i]*L] ] )
                m_1d = np.array( [ [1/3*rho*A[i]*L, 0, 0],
                                 [0, 13/35*rho*A[i]*L, -11*L/210*rho*A[i]*L],
                                 [0, -11*L/210*rho*A[i]*L, L**2/105*rho*A[i]*L] ] )
            
                m_matrix_3_dof = np.array( [ [m_1a[0][0], m_1a[0][1], m_1a[0][2], m_1b[0][0], m_1b[0][1], m_1b[0][2] ],
                                             [m_1a[1][0], m_1a[1][1], m_1a[1][2], m_1b[1][0], m_1b[1][1], m_1b[1][2] ],
                                             [m_1a[2][0], m_1a[2][1], m_1a[2][2], m_1b[2][0], m_1b[2][1], m_1b[2][2] ],
                                             [m_1c[0][0], m_1c[0][1], m_1c[0][2], m_1d[0][0], m_1d[0][1], m_1d[0][2] ],
                                             [m_1c[1][0], m_1c[1][1], m_1c[1][2], m_1d[1][0], m_1d[1][1], m_1d[1][2] ],
                                             [m_1c[2][0], m_1c[2][1], m_1c[2][2], m_1d[2][0], m_1d[2][1], m_1d[2][2] ] ] )
                
                for j in range (6):
                    for q in range (6):
                        k_matrix_1[3*i+j][3*i+q] += k_matrix_3_dof[j][q]
                        m_matrix_1[3*i+j][3*i+q] += m_matrix_3_dof[j][q]
            
            #Zusatzmassen und Leuchte an der Spitze hinzufügen
            #Zusatzmassen
            #print("Extramassen:" , masse_node_liste)
            for i in range (anzahl_nodes):
                m_matrix_1[3*i][3*i] += masse_node_liste[i]
                m_matrix_1[3*i+1][3*i+1] += masse_node_liste[i]
            #Leuchte
            m_matrix_1[anzahl_dof-3][anzahl_dof-3] += m_leuchte
            m_matrix_1[anzahl_dof-2][anzahl_dof-2] += m_leuchte
            
            #Rotationssteifigkeit der "Einspannung" im Boden modellieren
            #im Moment muss der entsprechende Wert hier eingegeben werden
            k_matrix_1[2][2] += k_bodenfeder
            #print("K Bodenfeder:" , k_bodenfeder)
    
            #Kraftvektor (nur Windkraft) erstellen
            f_vektor_1 = np.zeros(anzahl_dof)
            for i in range (anzahl_nodes):
                if achse == 0:
                    f_vektor_1[3*i+1] = f_d_node_x[i]
                if achse == 1:
                    f_vektor_1[3*i+1] = f_d_node_y[i]
            
            #dofs, die durch einspannung gehalten werden, löschen
            dof_gehalten = [0,1] #mit 2: biegesteif eingespannt
            anzahl_dof_gehalten = len(dof_gehalten)
            m_matrix = np.zeros( (anzahl_dof-anzahl_dof_gehalten,anzahl_dof-anzahl_dof_gehalten) )
            k_matrix = np.zeros( (anzahl_dof-anzahl_dof_gehalten,anzahl_dof-anzahl_dof_gehalten) )
            f_vektor = np.zeros(anzahl_dof-anzahl_dof_gehalten)
            a = 0
            for i in range (anzahl_dof):
                b = 0
                if i not in dof_gehalten:
                    f_vektor[a] = f_vektor_1[i]
                    for j in range (anzahl_dof):
                        if j not in dof_gehalten:
                            m_matrix[a][b]  = m_matrix_1[i][j]
                            k_matrix[a][b]  = k_matrix_1[i][j]
                            b += 1
                    a += 1
    
            #statische Deformation berechnen
            u_statisch = np.zeros(anzahl_dof-anzahl_dof_gehalten)
            k_matrix_invers = np.linalg.inv(k_matrix)
            u_statisch = np.dot(k_matrix_invers,f_vektor)
            u_gross = np.zeros(anzahl_dof)
            c = 0
            for i in range (anzahl_dof):
                if i in dof_gehalten:
                    u_gross[i] = 0
                    c += 1
                else:
                    u_gross[i] = u_statisch[i-c]
            u_horizontal = np.zeros(anzahl_nodes)
            for i in range (anzahl_nodes):
                u_horizontal[i] = u_gross[3*i+1]
            if achse == 0:
                #print("zulässige horizontale Verschiebung:" , round(verschiebung_zugelassen*hoehe*1000,2) , "mm")
                #print("Die horizontale Verschiebung der Mastspitze in x-Richtung ist:" , round(u_horizontal[anzahl_nodes-1]*1000,2) , "mm")
                sheet.append(["zulässige horizontale Verschiebung [mm]:" , round(verschiebung_zugelassen*hoehe*1000,2) ])
                sheet.append(["horizontale Verschiebung, x-Richtung [mm]:" , round(u_horizontal[anzahl_nodes-1]*1000,2) ])
            if achse == 1:
                #print("zulässige horizontale Verschiebung:" , round(verschiebung_zugelassen*hoehe*1000,2) , "mm")
                #print("Die horizontale Verschiebung der Mastspitze in y-Richtung ist:" , round(u_horizontal[anzahl_nodes-1]*1000,2) , "mm")
                sheet.append(["zulässige horizontale Verschiebung [mm]:" , round(verschiebung_zugelassen*hoehe*1000,2) ])
                sheet.append(["horizontale Verschiebung, y-Richtung [mm]:" , round(u_horizontal[anzahl_nodes-1]*1000,2) ])
            if u_horizontal[anzahl_nodes-1] <= verschiebung_zugelassen*hoehe:
                #print("horizontale Verformungen i.O.")
                sheet.append(["horizontale Verformungen i.O."])
            else:
                #print("horizontale Verformungen zu gross.")
                sheet.append(["horizontale Verformungen zu gross."])
            #Deformation plotten
            Masthoehe = []
            for i in range(anzahl_nodes):
                Masthoehe.append(L*i)
            plt.plot(u_horizontal,Masthoehe)
            plt.xlabel('horizontale Verschiebung [m]')
            plt.ylabel('Masthöhe [m]')
            if achse == 0:
                plt.title('Deformation x-Richtung mit Berücksichtigung der Einspannung')
            if achse == 1:
                plt.title('Deformation y-Richtung mit Berücksichtigung der Einspannung')
            plt.grid(True)  #Raster hinzufügen
            if u_horizontal[anzahl_nodes-1] < 1.1:
                plt.xlim(-1.2, 1.2) #darzustellenden Abschnitt der x-Achse fixieren
            else:
                plt.xlim(-u_horizontal[anzahl_nodes-1]+0.2,u_horizontal[anzahl_nodes-1]+0.2)
            #plot in excel darstellen
            anker_zelle_spalte = chr(ord('E') + 10*achse)
            anker_zelle = f'{anker_zelle_spalte}122'
            plot_image = BytesIO()
            plt.savefig(plot_image, format='png')
            plot_image.seek(0)
            img = Image(plot_image)
            img.anchor = anker_zelle
            sheet.add_image(img)
            #
            #plt.show()
            plt.clf()
    
            
            #Eigenfrequenzen und -modi berechnen
            D, V = np.linalg.eig(np.dot(np.linalg.inv(m_matrix), k_matrix))
            #D = eigenwerte, V = eigenvektoren, eigenmodi sind Spalten in der V-matrix
            sortiert_D = sorted(D)
            transponiert_V = np.transpose(V) #jetzt sind die eigenmodi Zeilen in der transponierten V-matrix
            sortiert_V = np.zeros( (len(D),len(D)) )
            for i in range (len(D)):
                for j in range (len(D)):
                    if sortiert_D[i] == D[j]:
                        sortiert_V[i] = transponiert_V[j]
            normalisiert_V = np.zeros( (len(D),len(D)) )
            for i in range (len(D)):
                max_verschiebung = max(sortiert_V[i], key=abs)
                if max_verschiebung != 0:
                    ratio = 1/max_verschiebung
                    ratio = abs(ratio)
                    normalisiert_V[i] = [x*ratio for x in sortiert_V[i]]
                else:
                    normalisiert_V[i] = sortiert_V[i]
            eigenfrequenzen = sortiert_D
            eigenfrequenzen = [math.sqrt(x)/(2*math.pi) for x in eigenfrequenzen]
            #print("Eigenfrequenzen:")
            #print(eigenfrequenzen)
            
            #die gehaltenen dof zu den Eigenmodi hinzufügen
            normalisiert_V_gross = np.zeros( (len(D),anzahl_dof) )
            for i in range (len(D)):
                a = 0
                for j in range (anzahl_dof):
                    if j in dof_gehalten:
                        normalisiert_V_gross[i][j] = 0
                        a += 1
                    else:
                        normalisiert_V_gross[i][j] = normalisiert_V[i][j-a]
        
            if inputkontrolle == True:
                #Eigenmodi plotten
                Masthoehe = []
                for i in range(anzahl_nodes):
                    Masthoehe.append(L*i)
                auslenkung = np.zeros( (len(D),anzahl_nodes) )
                for i in range (len(D)):
                    for j in range (anzahl_nodes):
                        auslenkung[i][j] = normalisiert_V_gross[i][3*j+1]
                if achse == 0:
                    sheet.append(["Eigenfrequenzen in x-Richtung:"])
                if achse == 1:
                    sheet.append(["Eigenfrequenzen in y-Richtung:"])
                
                ##for i in range (len(D)):
                for i in range(5): #Jetzt werden nur die ersten 5 geplottet.
                    plt.plot(auslenkung[i],Masthoehe)
                    plt.xlabel('Auslenkung [m]')
                    plt.ylabel('Masthöhe [m]')
                    str_i = str(i+1)
                    str_eigenfrequenzen = str(round(eigenfrequenzen[i],4))
                    if achse == 0:
                        plt.title('Eigenmodus ' + str_i + ' (x-Richtung), f = ' + str_eigenfrequenzen + ' Hz (mit Bodenfeder)')
                    if achse == 1:
                        plt.title('Eigenmodus ' + str_i + ' (y-Richtung), f = ' + str_eigenfrequenzen + ' Hz (mit Bodenfeder)')
                    plt.grid(True)  #Raster hinzufügen
                    plt.xlim(-1.2, 1.2) #darzustellenden Abschnitt der x-Achse fixieren
                    #plot in excel darstellen
                    anker_zelle_spalte = anker_zelle_spalte_liste[i]
                    anker_zelle_zeile = 148 + achse*26
                    anker_zelle = f'{anker_zelle_spalte}{anker_zelle_zeile}'
                    #print("ankerzelle" , anker_zelle)
                    plot_image = BytesIO()
                    plt.savefig(plot_image, format='png')
                    plot_image.seek(0)
                    img = Image(plot_image)
                    img.anchor = anker_zelle
                    sheet.add_image(img)
                    #
                    #plt.show()
                    plt.clf()
                    sheet.append(["Eigenfrequenz" , i+1 , str_eigenfrequenzen, "Hz" ])
                    
#Titel für plots schreiben
    for i in range (13):
        sheet.append([])
    sheet.append(["statische Deformationen in y- und x-Richtung"])
    sheet.append(["ohne Berücksichtigung der Einspannung:"])
    for i in range (24):
        sheet.append([])
    sheet.append(["Eigenmodi 1-5 in x-Richtung"])
    sheet.append(["ohne Berücksichtigung der Einspannung:"])
    for i in range (24):
        sheet.append([])
    sheet.append(["Eigenmodi 1-5 in y-Richtung"])
    sheet.append(["ohne Berücksichtigung der Einspannung:"])

      
    if erfüllt == False:
        for i in range (24):
            sheet.append([])
        sheet.append(["statische Deformationen in y- und x-Richtung"])
        sheet.append(["mit Berücksichtigung der Einspannung:"])
        for i in range (24):
            sheet.append([])
        sheet.append(["Eigenmodi 1-5 in x-Richtung"])
        sheet.append(["mit Berücksichtigung der Einspannung:"])
        for i in range (24):
            sheet.append([])
        sheet.append(["Eigenmodi 1-5 in y-Richtung"])
        sheet.append(["mit Berücksichtigung der Einspannung:"])
                
#Inputkontrolle 2
elif inputkontrolle == False:
    #print("Input ist falsch.")
    sheet.append(["Bitte überprüfen sie den Input."])

#workbook speichern
workbook.save('Resultate_Frequenzanalyse.xlsx') #Die  neue Excel Datei wird im gleichen Ordner gespeichert wie die Jupyter Datei