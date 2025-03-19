#Import Bibliotheken
import math
import openpyxl
import pandas as pd

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

#Titel in Zelle B2 schreiben
sheet['B2'] = "Ergebnisse"
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
ausmitte_x_leuchte_excel = daten.iloc[15,4]
ausmitte_x_leuchte = ausmitte_x_leuchte_excel
#print("Ausmitte_x Leuchte:" , ausmitte_x_leuchte_excel)
ausmitte_y_leuchte_excel = daten.iloc[15,5]
ausmitte_y_leuchte = ausmitte_y_leuchte_excel
#print("Ausmitte_y Leuchte:" , ausmitte_y_leuchte_excel)

#input für die Zusatzmassen
#Im Folgenden können Sie die Höhe [m], die Masse [kg] und die projizierte Fläche [m^2] von Zusatzmassen in die Listen eingeben.
#Die Einträge an der gleichen Stelle der jeweiligen Listen sollten dabei der gleichen Zusatzmasse entsprechen.
z_zusatzmasse_list = []
A_x_zusatzmasse_list = []
A_y_zusatzmasse_list = []
m_zusatzmasse_list = []
z_zusatzmasse_excel = daten.iloc[19,2]
anzahl_zusatzmassen = 0
ausmitte_x_zusatzmasse_list = []
ausmitte_y_zusatzmasse_list = []
while pd.notnull(z_zusatzmasse_excel):
    A_x_zusatzmasse_excel = daten.iloc[20,2+anzahl_zusatzmassen]
    A_y_zusatzmasse_excel = daten.iloc[21,2+anzahl_zusatzmassen]
    m_zusatzmasse_excel = daten.iloc[22,2+anzahl_zusatzmassen]
    ausmitte_x_zusatzmasse_excel = daten.iloc[23,2+anzahl_zusatzmassen]
    ausmitte_y_zusatzmasse_excel = daten.iloc[24,2+anzahl_zusatzmassen]
    anzahl_zusatzmassen += 1
    z_zusatzmasse_list.append(z_zusatzmasse_excel)
    A_x_zusatzmasse_list.append(A_x_zusatzmasse_excel)
    A_y_zusatzmasse_list.append(A_y_zusatzmasse_excel)
    m_zusatzmasse_list.append(m_zusatzmasse_excel)
    ausmitte_x_zusatzmasse_list.append(ausmitte_x_zusatzmasse_excel)
    ausmitte_y_zusatzmasse_list.append(ausmitte_y_zusatzmasse_excel)
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
#print("ausmitte_x_zusatzmasse_list")
#print(ausmitte_x_zusatzmasse_list)
#print("ausmitte_y_zusatzmasse_list")
#print(ausmitte_y_zusatzmasse_list)

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

#Lastbeiwerte gemäss welcher Norm? Geben Sie 1,2,3 oder 4 ein. 1 = SIA 260, 2 = SN-EN 40-3-3, 5.4, Tabelle 1, Klasse A, 3 = SN-EN 40-3-3, 5.4, Tabelle 1, Klasse B, 4 = SN-EN 40-3-3, 5.4, Tabelle 1, Klasse Grenzzustand der Tragfähigkeit
norm_excel = daten.iloc[43, 1]
if norm_excel == "SIA 260":
    norm = 1
elif norm_excel == "EN 40-3-3 Klasse A (Tab. 1)":
    norm = 2
elif norm_excel == "EN 40-3-3 Klasse B (Tab.1)":
    norm = 3
elif norm_excel == "EN 40-3-3 Grenzzustand der Tragfähgikeit (Tab.1)":
    norm = 4
#print("norm")
#print(norm)

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

#Berechnung inputabhängiger Variablen
#Durchmesser wenn achteckiger Querschnitt
d_flanke = [None] * (len(d_list_eingabe))
d_aussen = [None] * (len(d_list_eingabe))
if form == 2:
    for i in range (len(d_list_eingabe)):
        #d_flanke bezeichnet den Flankendurchmesser bei achteckigen Querschnitten
        d_flanke[i] = d_list_eingabe[i]/math.tan(math.pi/8)
        #print("Flankendurchmesser:" , d_flanke[i])
        #d_aussen bezeichnet den Aussendurchmesser bei achteckigen Querschnitten
        d_aussen[i] = d_list_eingabe[i]/(math.sin(math.pi/8))
        #print("Aussendurchmesser:" , d_aussen[i])
else: #bei kreisförmigen Querschnitten sind d_flanke und d_aussen gleich
    d_flanke = d_list_eingabe
    d_aussen = d_list_eingabe

#Materialkennwerte
if material == 1:
    f_y = 235 #in N/mm^2
    E = 210000 #in N/mm^2
    rho = 7850 #in kg/m^3
    gamma_m = 1.05
elif material == 2:
    f_y = 275 #in N/mm^2
    E = 210000 #in N/mm^2
    rho = 7850 #in kg/m^3
    gamma_m = 1.05 
elif material == 3:
    f_y = 355 #in N/mm^2
    E = 210000 #in N/mm^2
    rho = 7850 #in kg/m^3
    gamma_m = 1.05 
elif material == 4:
    f_y = 240 #in N/mm^2
    E = 70000 #in N/mm^2
    rho = 2700 #in kg/m^3
    gamma_m = 1.15 #gemäss SN-EN-40-3-3, Tab.2

#gemäss BA2023 kann konservativ mit T=3.5s gerechnet werden
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
#Lastbeiwerte
if norm == 1:
    gamma_Q = 1.5
    gamma_G_sup = 1.35
elif norm == 2:
    gamma_Q = 1.4
    gamma_G_sup = 1.2
elif norm == 3:
    gamma_Q = 1.2
    gamma_G_sup = 1.2
elif norm == 4:
    gamma_Q = 1.0
    gamma_G_sup = 1.0
#Klasse Verschiebungen
if klasse_verschiebung == 1:
    verschiebung_zugelassen = 0.04
elif klasse_verschiebung == 2:
    verschiebung_zugelassen = 0.06
elif klasse_verschiebung == 3:
    verschiebung_zugelassen = 0.1


#Inputkontrolle
inputkontrolle = True
inputfehler = 0
if hoehe > 20:
    inputkontrolle = False
    sheet.append(["Die verwendete Norm SN-EN-40-3-3 gilt nur bis zu einer Höhe von 20 m."])
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
    
#Berechnungen Schleife 1
if inputkontrolle == True:   
    #print()
    #z_m enthält die Höhe [m] des Mittelpunktes von jedem Element
    z_m = [None] * (anzahl_elemente+1)
    #c_h, Profilbeiwert c_h von jedem Element(gemäss Höhe des Mittelpunkts) gemäss SIA 261, 6.2.1.2
    c_h = [None] * (anzahl_elemente+1)
    #c_e, Standortbeiwert, gemäss BA2023, S.10
    c_e = [None] * (anzahl_elemente+1)
    #q_z [N/m^2], charakteristischer Winddruck gemäss SN-EN 40-3-1, 5.2.1
    q_z = [None] * (anzahl_elemente+1)
    #d_m_flanke, Flankendurchmesser, bei kreisförmigen Querschnitten gleich d_m_aussen
    d_m_flanke = [None] * (anzahl_elemente+1)
    #d_m_aussen, Aussendurchmesser, bei kreisförmigen Querschnitten gleich d_m_flanke
    d_m_aussen = [None] * (anzahl_elemente+1)
    #d_seite_elementmitte, Seitenlänge aussen in der Mitte des Elements, wird nur für achteckige Querschnitte verwendet
    d_seite_elementmitte = [None] * (anzahl_elemente+1)
    #delta_h
    delta_h = [None] * (anzahl_elemente+1)
    #v_Wind [m/s], Windgeschwindigkeit, gemäss SN_EN 40-3-1, 5.3.2, Koeffizienten gemäss BA2023, S.
    v_wind = [None] * (anzahl_elemente+1)
    #re, Reynoldszahl gemäss SN-EN 40-3-1, 5.3.2, mit Flankendurchmesser berechnet (achteckige Querschnitte)
    reynoldszahl = [None] * (anzahl_elemente+1)
    #r_achteck, Eckradius, Es wird davon ausgegegangen, dass r_achteckt unbekannt ist. Deshalb wird es konservatvi zu 0 gesetzt.
    r_achteck = [None] * (anzahl_elemente+1)
    #r/d =r_achteck/d_m_flanke gemäss SN_EN 40-3-1, 5.3.2, zur Verwendung von Bild 3
    r_durch_d = [None] * (anzahl_elemente+1)
    #c formbeiwert gemäss SN-EN 40-3-1, 5.3.2, Bild 3
    c_formbeiwert = [None] * (anzahl_elemente+1)
    #Fläche Mast, die Fläche eines Elements (Windangriffsfläche) [m^2]
    flaeche_mast = [None] * (anzahl_elemente+1)
    #Fläche Zusatzmassen und Leuchten pro Element [m^2] in x-Richtung
    flaeche_zm_x = [0] * (anzahl_elemente+1)
    #Fläche Zusatzmassen und Leuchten pro Element [m^2] in y-Richtung
    flaeche_zm_y = [0] * (anzahl_elemente+1)
    #Fläche total in x-Richtung, Addition der Flächen von Mast, Leuchte, Zusatzmasse pro Element [m^2]
    flaeche_tot_x = [None] * (anzahl_elemente+1)
    #Fläche total in y-Richtung, Addition der Flächen von Mast, Leuchte, Zusatzmasse pro Element [m^2]
    flaeche_tot_y = [None] * (anzahl_elemente+1)
    #Masse Mast, Masse des Mastelements [kg]
    masse_mast = [None] * (anzahl_elemente+1)
    #Masse Zusatzmassen und Leuchten pro Element [kg]
    masse_zm = [0] * (anzahl_elemente+1)
    #Masse total [kg]
    masse_tot = [None] * (anzahl_elemente+1)
    #F_d, Windkraft [N] auf Designniveau pro Element in x-Richtung
    f_d_x = [None] * (anzahl_elemente+1)
    #F_d, Windkraft [N] auf Designniveau pro Element in y-Richtung
    f_d_y = [None] * (anzahl_elemente+1)
    #G_d, Gewichtskraft [N] auf Designniveau pro Element
    g_d = [None] * (anzahl_elemente+1)
    #Gewicht [N] des gesamten Mastens
    gewicht_gesamt = 0
    #Multiplikation der Fläche einer Zusatzmasse/Leuchte mit der Ausmittung in x-Richtung, Einheit [m^3], zur Berechnung des Torsionsmoment
    flaeche_mal_abstand_x = [0] * (anzahl_elemente+1)
    #Multiplikation der Fläche einer Zusatzmasse/Leuchte mit der Ausmittung in y-Richtung, Einheit [m^3], zur Berechnung des Torsionsmoment
    flaeche_mal_abstand_y = [0] * (anzahl_elemente+1)
    #Torsionsbeitrag_x = Fläche mal Abstand von der Achse (x-Richtung) mal Winddruck mal Gamma_Q, Einheit [Nm]
    #Im Moment wird noch nicht berücksichtigt, dass der Wind nicht in x-Richtung wirken muss. Das wird später in einer Schleife mit verschiedenen Windrichtungen ergänzt.
    torsionsbeitrag_x = [0] * (anzahl_elemente+1)
    #Torsionsbeitrag_y = Fläche mal Abstand von der Achse (y-Richtung) mal Winddruck mal Gamma_Q,  Einheit [Nm]
    #Im Moment wird noch nicht berücksichtigt, dass der Wind nicht in y-Richtung wirken muss. Das wird später in einer Schleife mit verschiedenen Windrichtungen ergänzt.
    torsionsbeitrag_y = [0] * (anzahl_elemente+1)
    
    #Nun wird für jedes Element die oben definierten Werte ausgerechnet.
    for i in range (anzahl_elemente+1):
        #print(i) #Kontrollausgabe ohne Funktion
        z_m[i] = (hoehe/anzahl_elemente)*(i+0.5)
        if i == (anzahl_elemente):
            z_m[i]= hoehe
        z_m[i] = round(z_m[i],4)
        #print("z_m:" , z_m[i]) #Kontrollausgabe ohne Funktion
        if gelaendekategorie in ["2","2a","3"]:
            if z_m[i] <= 5:
                z_temp = 5
            else:
                z_temp = z_m[i]
        if gelaendekategorie == "4":
            if z_m[i] <= 10:
                z_temp = 10
            elif z_m[i] > 30:
                z_g = 450
                alpha_r = 0.23
                z_temp == z_m[i]
            else:
                z_temp == z_m[i]
        c_h[i] = 1.6*((z_temp/z_g)**alpha_r+0.375)**2
        #print("c_h:" , c_h[i]) #Kontrollausgabe ohne Funktion
        c_e[i] = c_h[i]/(1.6*( (10/300)**0.16+0.375)**2)*(1+0.375*(300/10)**0.16)**2
        #print("c_e:" , c_e[i])  #Kontrollausgabe ohne Funktion
        q_z[i] = delta*beta*f*c_e[i]*q_10
        #print("q_z:" , q_z[i]) #Kontrollausgabe ohne Funktion
        if form == 3: # form = zylindrisch, d_m_flanke bzw. d_m_aussen werden entsprechend der Höhe bestimmt
            for j in range (len(z_list)):
                if z_list[j] <= z_m[i]:
                    d_m_flanke[i] = d_flanke[j]
                    d_m_aussen[i] = d_aussen[j]
                else:
                    break
        if form == 1 or form == 2: # form = konisch, lineare Interpolation
            d_m_flanke[i] = d_flanke[0] - ((d_flanke[0]-d_flanke[1])/(z_list[1]-z_list[0]))*(z_m[i]-z_list[0])
            d_m_aussen[i] = d_aussen[0] - ((d_aussen[0]-d_aussen[1])/(z_list[1]-z_list[0]))*(z_m[i]-z_list[0])
            d_seite_elementmitte[i] = d_list_eingabe[0] - ((d_list_eingabe[0]-d_list_eingabe[1])/(z_list[1]-z_list[0]))*(z_m[i]-z_list[0])
        #print("d_m_flanke:" , d_m_flanke[i]) #Kontrollausgabe ohne Funktion
        #print("d_m_aussen:" , d_m_aussen[i]) #Kontrollausgabe ohne Funktion
        delta_h[i] =  hoehe/anzahl_elemente
        v_wind[i] = 1/c_s*math.sqrt(q_z[i]/(rho_luft*beta*delta*0.5))
        reynoldszahl[i] = d_m_flanke[i]*v_wind[i]/(15.1*10**(-6))*10**(-5)
        if form == 2:
            r_achteck[i] = 0 #Eckradien sind nicht bekannt, werden konservativ so angenommen, dass r/D < 0.075
            r_durch_d[i] = r_achteck[i]/d_m_flanke[i]
            if r_durch_d[i] < 0.075: #Kurve 1, Bild 3, SN-EN 40-3-1
                if reynoldszahl[i] >= 3:
                    c_formbeiwert[i] = 1.3
                elif reynoldszahl[i] < 2.3:
                    c_formbeiwert[i] = 1.45
                else:
                    c_formbeiwert[i] = 1.45-(0.15/0.7)*(reynoldszahl[i]-2.3)
            else: # Kurve 2, Bild 3, SN-EN 40-3-1, in der aktuellen Version des codes wird nie Kurve 2 verwendet
                if reynoldszahl[i] >= 7:
                    c_formbeiwert[i] = 1.1
                elif reynoldszahl[i] < 2:
                    c_formbeiwert[i] = 1.29
                else:
                    c_formbeiwert[i] = 1.29-(0.19/5)*(reynoldszahl[i]-2)
        elif form == 1 or form == 3:
            r_achteck[i] = 0
            r_durch_d[i] = 0
            if reynoldszahl[i] > 4:
                c_formbeiwert[i] = 0.5 + (1/60)*(reynoldszahl[i]-4)
            elif reynoldszahl[i] > 2 and reynoldszahl[i] <= 4:
                c_formbeiwert[i] = 1.2 - 0.35*(reynoldszahl[i]-2)
            else:
                c_formbeiwert[i] = 1.2
        
        if i == anzahl_elemente:
            delta_h[i] = 0
            v_wind[i] = 0
            reynoldszahl[i] = 0
            r_achteck[i] = 0
            r_durch_d[i] = 0
            c_formbeiwert[i] = 1
        #print("delta_h:" , delta_h[i]) #Kontrollausgabe ohne Funktion
        #print("v_wind:" , v_wind[i]) #Kontrollausgabe ohne Funktion
        #print("Reynoldszahl:" , reynoldszahl[i]) #Kontrollausgabe ohne Funktion
        #print("r:" , r_achteck[i]) #Kontrollausgabe ohne Funktion
        #print("r/d" , r_durch_d[i]) #Kontrollausgabe ohne Funktion
        #print("c_formbeiwert:" , c_formbeiwert[i]) #Kontrollausgabe ohne Funktion
            
        flaeche_mast[i] = delta_h[i]*d_m_aussen[i]*c_formbeiwert[i]
        #print(flaeche_mast[i]) #Kontrollausgabe ohne Funktion
        if form == 1 or form == 3:
            masse_mast[i] = (d_m_flanke[i]**2-(d_m_flanke[i]-2*t)**2)*math.pi/4*delta_h[i]*rho
        elif form == 2:
            masse_mast[i] = 8*t*(d_seite_elementmitte[i]-t/math.tan(3*math.pi/8))*delta_h[i]*rho
        for k in range (len(z_zusatzmasse_list)): #Falls eine Zusatzmasse gerade an der Grenze von zwei Elementen liegt, wird sie gleichmässig auf die beiden Elemente aufgeteilt.
            if i == 0 and z_zusatzmasse_list[k] == 0:
                flaeche_zm_x[i] += A_x_zusatzmasse_list[k]
                flaeche_zm_y[i] += A_y_zusatzmasse_list[k]
                masse_zm[i] += m_zusatzmasse_list[k]
                flaeche_mal_abstand_x[i] += A_x_zusatzmasse_list[k]*ausmitte_x_zusatzmasse_list[k]
                flaeche_mal_abstand_y[i] += A_y_zusatzmasse_list[k]*ausmitte_y_zusatzmasse_list[k]
            elif i == anzahl_elemente and z_zusatzmasse_list[k] == hoehe: #damit Zusatzmassen an der Spitze sicher auch berücksichtigt werden
                flaeche_zm_x[i] += A_x_zusatzmasse_list[k]
                flaeche_zm_y[i] += A_y_zusatzmasse_list[k]
                masse_zm[i] += m_zusatzmasse_list[k]
                flaeche_mal_abstand_x[i] += A_x_zusatzmasse_list[k]*ausmitte_x_zusatzmasse_list[k]
                flaeche_mal_abstand_y[i] += A_y_zusatzmasse_list[k]*ausmitte_y_zusatzmasse_list[k]
            elif z_m[i]-(delta_h[i]/2) < z_zusatzmasse_list[k] and z_m[i]+(delta_h[i]/2) > z_zusatzmasse_list[k]:
                flaeche_zm_x[i] += A_x_zusatzmasse_list[k]
                flaeche_zm_y[i] += A_y_zusatzmasse_list[k]
                masse_zm[i] += m_zusatzmasse_list[k]
                flaeche_mal_abstand_x[i] += A_x_zusatzmasse_list[k]*ausmitte_x_zusatzmasse_list[k]
                flaeche_mal_abstand_y[i] += A_y_zusatzmasse_list[k]*ausmitte_y_zusatzmasse_list[k]
            elif z_m[i]-(delta_h[i]/2) == z_zusatzmasse_list[k] or z_m[i]+(delta_h[i]/2) == z_zusatzmasse_list[k]:
                flaeche_zm_x[i] += 0.5*A_x_zusatzmasse_list[k]
                flaeche_zm_y[i] += 0.5*A_y_zusatzmasse_list[k]
                masse_zm[i] += 0.5*m_zusatzmasse_list[k]
                flaeche_mal_abstand_x[i] += 0.5*A_x_zusatzmasse_list[k]*ausmitte_x_zusatzmasse_list[k]
                flaeche_mal_abstand_y[i] += 0.5*A_y_zusatzmasse_list[k]*ausmitte_y_zusatzmasse_list[k]
        #Leuchte dazurechnen
        if i == anzahl_elemente:
            flaeche_zm_x[i] += A_x_leuchte
            flaeche_zm_y[i] += A_y_leuchte
            masse_zm[i] += m_leuchte
            flaeche_mal_abstand_x[i] += A_x_leuchte*ausmitte_x_leuchte
            flaeche_mal_abstand_y[i] += A_y_leuchte*ausmitte_y_leuchte
        flaeche_tot_x[i] = flaeche_mast[i] + flaeche_zm_x[i]
        flaeche_tot_y[i] = flaeche_mast[i] + flaeche_zm_y[i]
        masse_tot[i] = masse_mast[i] + masse_zm[i]
        #print("flaeche_mast." , flaeche_mast[i]) #Kontrollausgabe ohne Funktion
        #print("flaeche_zm_x:" , flaeche_zm_x[i]) #Kontrollausgabe ohne Funktion
        #print("flaeche_zm_y:" , flaeche_zm_y[i]) #Kontrollausgabe ohne Funktion
        #print("masse_tot:" , masse_tot[i]) #Kontrollausgabe ohne Funktion
        #Einwirkungen pro Element berechnen, auf Designniveau
        f_d_x[i] = flaeche_tot_x[i]*q_z[i]*gamma_Q
        f_d_y[i] = flaeche_tot_y[i]*q_z[i]*gamma_Q
        g_d[i] = masse_tot[i]*9.81*gamma_G_sup
        gewicht_gesamt += g_d[i]
        #print("f_d_x:" , f_d_x[i]) #Kontrollausgabe ohne Funktion
        #print("f_d_y:" , f_d_y[i]) #Kontrollausgabe ohne Funktion
        #print("g_d:" , g_d[i]) #Kontrollausgabe ohne Funktion 
        torsionsbeitrag_x[i] = flaeche_mal_abstand_x[i]*q_z[i]*gamma_Q
        torsionsbeitrag_y[i] = flaeche_mal_abstand_y[i]*q_z[i]*gamma_Q
        #print("Flaeche mal Abstand x:" , flaeche_mal_abstand_x[i])
        #print("Flaeche mal Abstand y:" , flaeche_mal_abstand_y[i])
        #print("Torsionsbeitrag x:" , torsionsbeitrag_x[i])
        #print("Torsionsbeitrag y:" , torsionsbeitrag_y[i])
        #print()
    #print("fertig mit Schleife 1")
    #print()
    #print()

#Berechnungen Schleife 2
    #Schnittgrösse: Biegemoment um x-Achse [Nm] pro Element an der Elementunterkante berechnen
    biegemoment_m_x = [0] * (anzahl_elemente+1)
    #Schnittgrösse: Biegemoment um y-Achse [Nm] pro Element an der Elementunterkante berechnen
    biegemoment_m_y = [0] * (anzahl_elemente+1)
    #Torsionsmoment [Nm] durch Wind in x-Richtung, pro Element an der Elementunterkante berechnen
    torsionsmoment_m_x = [0] * (anzahl_elemente+1)
    #Torsionsmoment [Nm] durch Wind in y-Richtung, pro Element an der Elementunterkante berechnen
    torsionsmoment_m_y = [0] * (anzahl_elemente+1)
    #z_grenze, Höhe der Elementunterkante (+ Oberkante des obersten Elements) [m]
    z_grenze = [0] * (anzahl_elemente+1)
    for i in range (anzahl_elemente+1):
        z_grenze[i] = z_m[i]-(delta_h[i]/2)
        #print("z:" , z_grenze[i])
        for j in range (i,anzahl_elemente+1):
            biegemoment_m_x[i] += (z_m[j]-(z_m[i]-delta_h[i]/2))*f_d_x[j]
            biegemoment_m_y[i] += (z_m[j]-(z_m[i]-delta_h[i]/2))*f_d_y[j]
            torsionsmoment_m_x[i] += torsionsbeitrag_x[j]
            torsionsmoment_m_y[i] += torsionsbeitrag_y[j]
        #print("Biegemoment_x:" , biegemoment_m_x[i])
        #print("Biegemoment_y:" , biegemoment_m_y[i])
        #print("Torsionsmoment_x:" , torsionsmoment_m_x[i])
        #print("Torsionsmoment_y:" , torsionsmoment_m_y[i])
        #print()
    #print("Schleife 2 fertig")
    #print()

#Berechnungen Schleife 3
    #Biegewiderstand [Nm] in x-Richtung an der Unterkante jedes Elements + ganz oben, gemäss SN-EN-40-3-3, 5.6.2.1
    biegewiderstand_m_x = [None] * (anzahl_elemente+1)
    #Biegewiderstand [Nm] in y-Richtung an der Unterkante jedes Elements + ganz oben, gemäss SN-EN-40-3-3, 5.6.2.1
    biegewiderstand_m_y = [None] * (anzahl_elemente+1)
    #Torsionswiderstand [Nm] an der Unterkante jedes Elements + ganz oben, gemäss SN-EN-40-3-3, 5.6.2.1
    torsionswiderstand_m = [None] * (anzahl_elemente+1)
    #d_m_widerstand, Durchmesser des Querschnitts an der Unterkante des Elements, bei Achtecken wird mit dem Flankendurchmesser (der Aussengeometrie) gerechnet, bei kreisförmigen Querschnitten mit dem Aussendurchmesser
    d_m_widerstand = [None] * (anzahl_elemente+1)
    #r_m, mittlerer Radius des Querschnitts an der Elementunterkante, gemäss SN-EN-40-3-3, 5.6.2.1
    r_m = [None] * (anzahl_elemente+1)
    #d_seite_elementunterkante, Seitenlänge aussen an der Elementunterkante, wird nur für achteckige Querschnitte verwendet
    d_seite_elementunterkante = [None] * (anzahl_elemente+1)
    #Epsilon, gemäss SN-EN-40-3-3, 5.6.2.1
    epsilon = [None] * (anzahl_elemente+1)
    #z_p, plastisches Modul des geschlossenen QS [mm^3], gemäss SN-EN-40-3-3, 5.6.2.1
    z_p = [None] * (anzahl_elemente+1)
    #phi_1, Beiwert gemäss SN-EN 40-3-3, Bild 2
    phi_1 = [None] * (anzahl_elemente+1)
    #phi_2, Beiwert gemäss SN-EN 40-3-3, 5.6.2.1
    phi_2 = [None] * (anzahl_elemente+1)
    for i in range (anzahl_elemente+1):
        if form == 3: # form = zylindrisch, d_m werden entsprechend der Höhe bestimmt
            for j in range (len(z_list)):
                if z_list[j] <= z_grenze[i]:
                    d_m_widerstand[i] = d_flanke[j]
        if form == 1 or form == 2: # form = konisch, lineare Interpolation
            d_m_widerstand[i] = d_flanke[0] - ((d_flanke[0]-d_flanke[1])/(z_list[1]-z_list[0]))*(z_grenze[i]-z_list[0])
            d_seite_elementunterkante[i] = d_list_eingabe[0] - ((d_list_eingabe[0]-d_list_eingabe[1])/(z_list[1]-z_list[0]))*(z_grenze[i]-z_list[0])
        #print("z:" , z_grenze[i])
        #print("d_m_widerstand:" , d_m_widerstand[i]) #Kontrollausgabe ohne Funktion
        r_m[i] = (d_m_widerstand[i]-t)/2
        #print("mittlerer Radius r_m:" , r_m[i]) #Kontrollausgabe ohne Funktion
        epsilon[i] = (r_m[i]/t)*math.sqrt(f_y/E)
        #print("epsilon:" , epsilon[i]) #Kontrollausgabe ohne Funktion
        if form == 1 or form == 3:
            z_p[i] = 4*r_m[i]**2*t *10**9 #*10^9 wegen der Einhheit: Z_p ist in mm^3
        elif form == 2:
            z_p[i] = 4.32*r_m[i]**2*t *10**9 #*10^9 wegen der Einhheit: Z_p ist in mm^3
        #print("z_p:" , z_p[i])  
        if form == 1 or form == 3:
            if  0 < epsilon[i] and epsilon[i] <= 0.8:
                phi_1[i] = 1
            elif 0.8 < epsilon[i]:
                phi_1[i] = (0.8/epsilon[i])**0.35
        elif form == 2:
            if  0 < epsilon[i] and epsilon[i] <= 0.8:
                phi_1[i] = 1
            elif 0.8 < epsilon[i] and epsilon[i]<= 1.53:
                phi_1[i] = (0.8/epsilon[i])**0.35
            elif 1.53 < epsilon[i]:
                phi_1[i] = 0.81-0.3*(epsilon[i]-1.5)**0.9
        #print("phi_1:" , phi_1[i]) #Kontrollausgabe ohne Funktion
        phi_2[i] = 0.474*E/(f_y*(r_m[i]/t)**1.5)
        #print("phi_2:" , phi_2[i]) #Kontrollausgabe ohne Funktion
        if phi_2[i] > 1:
            phi_2[i] = 1
        #print("phi_2:" , phi_2[i]) #Kontrollausgabe ohne Funktion
        if epsilon[i] > 2:
            #print("Der Biegewiderstand kann nicht ermittelt werden, da der Querschnitt zu dünn ist. Es ist nicht mehr möglich, den Beiwert phi_1 gemäss SN-EN 40-3-3, Bild 2 zu bestimmen.")
            inputkontrolle = False
            inputfehler = 1
        biegewiderstand_m_x[i] = f_y*phi_1[i]*z_p[i]/(10**3*gamma_m)
        biegewiderstand_m_y[i] = f_y*phi_1[i]*z_p[i]/(10**3*gamma_m)
        torsionswiderstand_m[i] = f_y*phi_2[i]*math.pi*r_m[i]**2 *t / (10**3*gamma_m) *1000*1000*1000 #Einheiten von r_m und t berücksichtigen (m ursprünglich, mm für die Formel)
        #print("biegewiderstand ohne Tür:" , biegewiderstand_m_x[i]) #Kontrollausgabe ohne Funktion
        #print("torsionswiderstand ohne Tür:" , torsionswiderstand_m[i]) #Kontrollausgabe ohne Funktion
        #print()
    #print("Tablle 3 fertig")
    #print()

#Berechnungen Schleife 4
    #Öffnungen berücksichtigen: unverstärkt oder verstärkt Typ 4, gemäss SN-EN 40-3-3
    #Annahme: pro Höhe nicht mehr als eine Öffnung, sonst kann nicht mehr gemäss SN-EN 40-3-3 gerechnet werden.
    #theta, halber Türöffnungswinkel gemäss SN-EN 40-3-3
    theta = [0] * (anzahl_elemente+1)
    #phi_3, phi_3 für unverstärkte Öffnung
    phi_3 = [0] * (anzahl_elemente+1)
    #phi_4, Beiwert für Torsionswiderstand, gemäss SN-EN 40-3-3, 5.6.2.3.2
    phi_4 = [0] * (anzahl_elemente+1)
    #phi_5, Beiwert für Torsionswiderstand, gemäss SN-EN 40-3-3, 5.6.2.3.2
    phi_5 = [0] * (anzahl_elemente+1)
    #phi_6, Beiwert für Torsionswiderstand, gemäss SN-EN 40-3-3, 5.6.2.3.2, der grössere der beiden folgenden Beiwerte kann verwendet werden
    phi_6_typ_2 = [0] * (anzahl_elemente+1)
    phi_6_typ_4 = [0] * (anzahl_elemente+1)
    #phi_7, Beiwert für Torsionswiderstand, gemäss SN-EN 40-3-3, 5.6.2.3.2
    phi_7 = [0] * (anzahl_elemente+1)
    #ny, Trägheitsradius der Türverstärkung [m]
    ny = [0] * (anzahl_elemente+1)
    #P, Beiwert für Torsionswiderstand, gemäss SN-EN 40-3-3, 5.6.2.3.2
    P = [0] * (anzahl_elemente+1)
    #m_x, Abstand von der x-Achse zur Mastwandmitte, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_x = [0] * (anzahl_elemente+1)
    #m_y, Abstand von der y-Achse zur Mastwandmitte, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_y = [0] * (anzahl_elemente+1)
    #m_0x, Abstand von x-Achse zum Schwerpunkt der Türverstärkung, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_0x = [0] * (anzahl_elemente+1)
    #m_0y, Abstand von y-Achse zum Schwerpunkt der Türverstärkung, gemäss SN-EN 40-3-3, 5.6.2.3.2
    m_0y = [0] * (anzahl_elemente+1)
    #b_x
    b_x = [0] * (anzahl_elemente+1)
    #b_y
    b_y = [0] * (anzahl_elemente+1)
    #z_pn, plastischer Modul des unverstärkten Querschnittes um die x-Achse [mm^3], gemäss SN-EN 40-3-3, 5.6.2.2
    z_pn = [0] * (anzahl_elemente+1)
    #z_py, plastischer Modul des unverstärkten Querschnittes um die y-Achse [mm^3], gemäss SN-EN 40-3-3, 5.6.2.2
    z_py = [0] * (anzahl_elemente+1)
    #z_pnr [mm^3], plastischer Modul des (verstärkten) Querschnittes um die x-Achse [mm^3], gemäss SN-EN 40-3-3, 5.6.2.2
    z_pnr = [0] * (anzahl_elemente+1)
    #z_pyr [mm^3], plastischer Modul des (verstärkten) Querschnittes um die y-Achse [mm^3], gemäss SN-EN 40-3-3, 5.6.2.2
    z_pyr = [0] * (anzahl_elemente+1)
    #g, ein Beiwert gemäss SN-EN 40-3-3, 5.6.2.2, für kreisförmige Querschnitte immmer 1, für achteckige Querschnitte später im Code definiert, gemäss SN-EN 40-3-3, mit folgender Korrektur: anstatt b_0 wird J_0 in der Formel verwendet.
    g = [1] * (anzahl_elemente+1)
    #z_offen, enthält die Höhen zwischen Elementen, an welchen sich eine Tür befindet, ansonsten 0.
    z_offen = [0] * (anzahl_elemente+1)
    #breite_tuere_elementunterkante, enthält die Breite der Tür, falls keine Tür, dann 0
    breite_tuere_elementunterkante = [0] * (anzahl_elemente+1)
    #Breite der Verstärkung
    breite_verstaerkung_elementunterkante = [0] * (anzahl_elemente+1)
    #Dicke der Verstärkung
    dicke_verstaerkung_elementunterkante = [0] * (anzahl_elemente+1)
    #f_beiwert, 2.0 für kreisförmige Querschnitte, 2.16 für achteckige Querschnitte, gemäss SN-EN 40-3-3, 5.6.2.2
    if form == 1 or form == 3:
        f_beiwert = 2.0
    elif form == 2:
        f_beiwert = 2.16
    #abgeminderter Biegewiderstand [Nm] in x-Richtung an der Grenze zwischen den Elementen, wenn sich auf dieser Höhe eine Tür/Öffnung befindet
    biegewiderstand_tuer_x = [0] * (anzahl_elemente+1)
    #abgeminderter Biegewiderstand [Nm] in y-Richtung an der Grenze zwischen den Elementen, wenn sich auf dieser Höhe eine Tür/Öffnung befindet
    biegewiderstand_tuer_y = [0] * (anzahl_elemente+1)
    #torsionswiderstand auf der Höhe einer Tür/Öffnung
    torsionswiderstand_tuer = [0] * (anzahl_elemente+1)
    #Ausrichtung, ist immmer x, ausser auf der Höhe einer Türöffnung mit Ausrichtung in y-Richtung, wird für die Berechnung des Biegewiderstands verwendet.
    #ausrichtung_tuere_list enthält nur so viele Elemente wie Anzahl Türen, ausrichtung_tuere enthält für jedes Berechnungselement einen Wert
    ausrichtung_tuere = ["x"] * (anzahl_elemente+1)
    if tuer == "Ja" or tuer == "ja":
        for i in range (anzahl_elemente+1):
            for a in range (anzahl_tueren):
                if z_grenze[i] >= hoehe_tuere_list[a] and z_grenze[i] <= hoehe_tuere_list[a]+laenge_tuere_list[a]:
                    z_offen[i] = z_grenze[i]
                    #print("Hier ist eine Tür:" , z_offen[i])
                    breite_tuere_elementunterkante[i] = breite_tuere_list[a]
                    ausrichtung_tuere[i] = ausrichtung_tuere_list[a]
                    if breite_tuere_list[a]/d_m_widerstand[i] > 0.8:
                        #print("die Tür ist zu breit.")
                        inputkontrolle = False
                        inputfehler = 2
                        break
                    if form == 1 or form == 3:
                        theta[i] = math.asin(breite_tuere_list[a]/d_m_widerstand[i])          
                    elif form == 2:
                        #theta für Achteck:
                        if breite_tuere_list[a] <= d_seite_elementunterkante[i]:
                            r_klein = 0.5*d_seite_elementunterkante[i]*(1+math.sqrt(2))
                        elif breite_tuere_list[a] > d_seite_elementunterkante[i]:
                            r_klein = 0.5*d_seite_elementunterkante[i]*(1+math.sqrt(2)) - 0.5*(breite_tuere_list[a]-d_seite_elementunterkante[i])
                        theta[i] = math.atan(breite_tuere_list[a]/2/r_klein)
                    phi_5[i] = 10*(math.cos(theta[i]/2))**2/(1+1.73*math.tan(theta[i])) * ((1+2.15*math.tan(theta[i])+0.85*r_m[i]/wirksame_laenge_tuere_list[a])/(1+2.15*math.tan(theta[i])+0.85*r_m[i]/wirksame_laenge_tuere_list[a]+3.8*(r_m[i]/wirksame_laenge_tuere_list[a])**2))
                    #print("phi_5:" , phi_5[i])
                    if dicke_verstaerkung_list[a] == 0:  #überprüft ob es keine verstaerkung hat
                        phi_3[i] = (t**2)*E/((t**2)*E + 0.07*r_m[i]*wirksame_laenge_tuere_list[a]*f_y)
                        if phi_3[i] > phi_1[i]:
                            phi_3[i] = phi_1[i]
                        #print("phi_3:" , phi_3[i])
                        phi_4[i] = t**2*E/((t**2)*E + 0.035*r_m[i]*wirksame_laenge_tuere_list[a]*f_y)
                        if phi_4[i] > phi_2[i]:
                            phi_4[i] = phi_2[i]
                        #print("phi_4:" , phi_4[i])
                        if form == 2:
                            j_achteck = d_seite_elementunterkante[i]-t/(math.tan(3*math.pi/8))
                            if breite_tuere_list[a] <= d_seite_elementunterkante[i]:
                                j_0 = 0.5*(j_achteck - breite_tuere_list[a])
                            elif breite_tuere_list[a] > d_seite_elementunterkante[i]:
                                breite_auf_einer_seite = 0.5*(breite_tuere_list[a]- j_achteck) *1/math.sin(math.pi/4)
                                j_0 = j_achteck - breite_auf_einer_seite
                            if j_0 < 4*t:
                                j_0 = j_achteck
                            g[i] = ( (15*t)/j_0 )**0.6
                            #print("j_0:" , j_0)
                            if g[i] > 1:
                                g[i] = 1
                        #print("Theta:" , theta[i])
                        #print("Theta in Grad:", theta[i]*180/math.pi)
                        z_pn[i] = 2*f_beiwert*r_m[i]**2*t*math.cos(theta[i]/2)*(1-math.sin(theta[i]/2)) *1000*1000*1000
                        #print("z_pn:" , z_pn[i])
                        z_py[i] = f_beiwert*r_m[i]**2*t*(1+math.cos(theta[i])) *1000*1000*1000
                        #print("z_py:" , z_py[i])
                        biegewiderstand_tuer_x[i] = f_y*g[i]*phi_3[i]*z_pn[i]/(gamma_m*1000)
                        biegewiderstand_tuer_y[i] = f_y*g[i]*phi_3[i]*z_py[i]/(gamma_m*1000)
                        torsionswiderstand_tuer[i] = f_y*g[i]*phi_4[i]*phi_5[i]*r_m[i]**3*t/(10**3 *gamma_m*wirksame_laenge_tuere_list[a]) *1000*1000*1000
                        if ausrichtung_tuere[i] == "y":
                            biegewiderstand_tuer_x[i], biegewiderstand_tuer_y[i] = biegewiderstand_tuer_y[i], biegewiderstand_tuer_x[i]
                        #print("abgeminderter Biegewiderstand x:" , biegewiderstand_tuer_x[i])
                        #print("abgeminderter Biegewiderstand y:" , biegewiderstand_tuer_y[i])
                        #print("abgeminderter Torsionswiderstand:" , torsionswiderstand_tuer[i])
                    if dicke_verstaerkung_list[a] != 0:  #überprüft ob es eine verstaerkung hat
                        breite_verstaerkung_elementunterkante[i] = breite_verstaerkung_list[a]
                        dicke_verstaerkung_elementunterkante[i] = dicke_verstaerkung_list[a]
                        phi_6_typ_4[i] = (2*t+dicke_verstaerkung_list[a])**2*E/((2*t+dicke_verstaerkung_list[a])**2*E + 0.32*r_m[i]*wirksame_laenge_tuere_list[a]*f_y)
                        if phi_6_typ_4[i] > phi_1[i]:
                            phi_6_typ_4[i] = phi_1[i]
                        #print("phi_6_typ_4:" , phi_6_typ_4[i])
                        P[i] = min(dicke_verstaerkung_list[a]*breite_verstaerkung_list[a]/(r_m[i]*t), wirksame_laenge_tuere_list[a]/(4*r_m[i]), 1.6 )
                        #print("P:" , P[i])
                        ny[i] = math.sqrt(1/12)*breite_verstaerkung_list[a]
                        phi_6_typ_2[i] = math.pi**2*E/(math.pi**2*E+f_y*(wirksame_laenge_tuere_list[a]/ny[i])**2)
                        if phi_6_typ_2[i] > phi_1[i]:
                            phi_6_typ_2[i] = phi_1[i]
                        #print("phi_6_typ_2:" , phi_6_typ_2[i])
                        #Hilfsvariablen zur Übersicht für die Berechnung von phi_7, gemäss SN-EN 40-3-3, Bild 8
                        L = wirksame_laenge_tuere_list[a]
                        R = r_m[i]
                        RL = R/L
                        win = theta[i]*180/math.pi #Theta in Grad
                        phi_7_1 = 12.6137 - 2.0293*(win/10) - 0.0571*(win/10)**2 + 0.0205*(win/10)**3
                        phi_7_2 = - 16.433*RL + 9.9812*RL*(win/10) - 2.1222*RL*(win/10)**2 + 0.1453*RL*(win/10)**3
                        phi_7_3 = - 91.9666*RL**2 + 10.6843*RL**2*(win/10) + 7.3863*RL**2*(win/10)**2 - 1.0161*RL**2*(win/10)**3
                        phi_7_4 = 314.5885*RL**3 - 109.7109*RL**3*(win/10) - 3.9352*RL**3*(win/10)**2 + 1.9119*RL**3*(win/10)**3
                        phi_7_5 = - 347.2925*RL**4 + 165.6309*RL**4*(win/10) - 6.927*RL**4*(win/10)**2 - 1.4166*RL**4*(win/10)**3
                        phi_7_6 = 129.8994*RL**5 - 74.523*RL**5*(win/10) + 5.6642*RL**5*(win/10)**2 + 0.351*RL**5*(win/10)**3
                        phi_7[i] = phi_7_1 + phi_7_2 + phi_7_3 + phi_7_4 + phi_7_5 + phi_7_6 
                        if form == 2:
                            if breite_tuere_list[a] <= d_seite_elementunterkante[i]:
                                m_x[i] = 0.5*d_seite_elementunterkante[i]*(1+math.sqrt(2)) - 0.5*t
                                m_y[i] = 0.5*breite_tuere_list[a]
                            elif breite_tuere_list[a] > d_seite_elementunterkante[i]:
                                m_x[i] = 0.5*d_seite_elementunterkante[i]*(1+math.sqrt(2)) - 0.5*(breite_tuere_list[a]-d_seite_elementunterkante[i]) - math.sqrt(2)/4*t
                                m_y[i] = 0.5*breite_tuere_list[a] - math.sqrt(2)/4*t
                            if breite_tuere_list[a] + 2*breite_verstaerkung_list[a] <= d_seite_elementunterkante[i]:
                                m_0x[i] = 0.5*d_seite_elementunterkante[i]*(1+math.sqrt(2)) - t - 0.5*dicke_verstaerkung_list[a]
                                m_0y[i] = m_y[i] + 0.5*breite_verstaerkung_list[a]
                            elif breite_tuere_list[a] <= d_seite_elementunterkante[i]:
                                m_0x[i] = 0.5*d_seite_elementunterkante[i]*(1+math.sqrt(2)) - (t+0.5*dicke_verstaerkung_list[a]+0.5*breite_verstaerkung_list[a])*math.sqrt(2)/2
                                m_0y[i] = 0.5*d_seite_elementunterkante[i] - (t+0.5*dicke_verstaerkung_list[a])*math.sqrt(2)/2 + breite_verstaerkung_list[a]*math.sqrt(2)/4
                            elif breite_tuere_list[a] > d_seite_elementunterkante[i]:
                                m_0x[i] = 0.5*d_seite_elementunterkante[i]*(1+math.sqrt(2)) - 0.5*(breite_tuere_list[a]-d_seite_elementunterkante[i]) - (t+0.5*dicke_verstaerkung_list[a]+0.5*breite_verstaerkung_list[a])*math.sqrt(2)/2
                                m_0y[i] = 0.5*breite_tuere_list[a] - (t+0.5*dicke_verstaerkung_list[a])*math.sqrt(2)/2 + breite_verstaerkung_list[a]*math.sqrt(2)/4
                        if form == 1 or form == 3:
                            m_x[i] = r_m[i]*math.cos(theta[i])
                            m_y[i] = r_m[i]*math.sin(theta[i])
                            m_0x[i] = m_x[i] - 0.5*breite_verstaerkung_list[a]*math.sin(theta[i]) - 0.5*(t+dicke_verstaerkung_list[a])*math.cos(theta[i])
                            m_0y[i] = m_y[i] - 0.5*(t+dicke_verstaerkung_list[a])*math.sin(theta[i]) + 0.5*breite_verstaerkung_list[a]*math.cos(theta[i])
                        #print("Theta:" , theta[i])
                        #print("Theta in Grad:", theta[i]*180/math.pi)
                        b_x[i] = (dicke_verstaerkung_list[a]*breite_verstaerkung_list[a])/(r_m[i]*t) * m_0x[i]/m_x[i]
                        #print("b_x:" , b_x[i])
                        b_y[i] = (dicke_verstaerkung_list[a]*breite_verstaerkung_list[a])/(r_m[i]*t) * m_0y[i]/m_y[i]
                        #print("b_y:" , b_y[i])
                        
                        #Die Winkel werden von Python im Bogenmass gerechnet, die Formel in SN-En 40-3-3 ist allerdings in Grad. Darum gibt es eine entsprechnde Umformung der Terme.
                        z_pnr[i] = f_beiwert*r_m[i]**2 *t*(2*math.cos(theta[i]/2-b_x[i]/2) - math.sin(theta[i]) + b_x[i]*math.cos(theta[i]))*1000*1000*1000
                        z_pyr[i] = f_beiwert*r_m[i]**2 *t*(1+math.cos(theta[i])+b_y[i]*math.sin(theta[i]))*1000*1000*1000
                        #print("m_x:" , m_x[i])
                        #print("m_0x:" , m_0x[i])
                        #print("z_pnr:" , z_pnr[i])
                        #print("m_y:" , m_y[i])
                        #print("m_0y:" , m_0y[i])
                        #print("z_pyr:" , z_pyr[i])
                        phi_6 = max(phi_6_typ_4[i], phi_6_typ_2[i])
                        biegewiderstand_tuer_x[i] = f_y*phi_6*z_pnr[i]/(gamma_m*1000)
                        biegewiderstand_tuer_y[i] = f_y*phi_6*z_pyr[i]/(gamma_m*1000)
                        torsionswiderstand_tuer[i] = f_y*phi_6*(phi_5[i]+P[i]*phi_7[i])*r_m[i]**3*t/(10**3*gamma_m*wirksame_laenge_tuere_list[a])*1000*1000*1000
                        if ausrichtung_tuere[i] == "y":
                            biegewiderstand_tuer_x[i], biegewiderstand_tuer_y[i] = biegewiderstand_tuer_y[i], biegewiderstand_tuer_x[i]
                        #print("abgeminderter Widerstand x:" , biegewiderstand_tuer_x[i])
                        #print("abgeminderter Widerstand y:" , biegewiderstand_tuer_y[i])
                        #print("abgeminderter Torsionswiderstand:" , torsionswiderstand_tuer[i])
                    #print()

#Berechnungen Schleife 5
    #für die massgebende Richtung: Ausnutzung und Biegemoment
    ausnutzung_x_massgebend = [0] * (anzahl_elemente+1)
    ausnutzung_y_massgebend = [0] * (anzahl_elemente+1)
    ausnutzung_torsion_massgebend = [0] * (anzahl_elemente+1)
    ausnutzung_tot_massgebend = [0] * (anzahl_elemente+1)
    ausnutzung_tot_wind_x = [0] * (anzahl_elemente+1)
    ausnutzung_tot_wind_y = [0] * (anzahl_elemente+1)
    biegemoment_m_x_massgebend = [0] * (anzahl_elemente+1)
    biegemoment_m_y_massgebend = [0] * (anzahl_elemente+1)
    torsionsmoment_massgebend = [0] * (anzahl_elemente+1)
    windrichtung_massgebend = 0
    windlast_x_massgebend = 0
    windlast_y_massgebend = 0
    ausnutzung_max = 0
    einspannmoment_x_wind_x = 0
    einspannmoment_y_wind_y = 0
    windlast_x_wind_x = 0
    windlast_y_wind_y = 0
    #gesamte Windlast [N]
    windlast_gesamt_massgebend = 0
    #Ausnutzung wird für alle Windrichtungen 0°,1°,2°,...,89°,90° durchgerechnet
    for w in range (91):
        #Windrichtung definieren, Windlast wird dementsprechend in x- und y-Richtung aufgeteilt. Winkel 0° entspricht Wind in x Richtung.
        #Einheit [rad], Bereich 0 bis Pi/2
        windrichtung = math.pi/2/90*w
        #print("Windrichtung:" , w)
        windlast_x = math.cos(windrichtung)
        windlast_y = math.sin(windrichtung)
        #print("x-Richtung:" , windlast_x)
        #print("y-Richtung:" , windlast_y)
        torsionsmoment_m = [0] * (anzahl_elemente+1)
        ausnutzung_x = [None] * (anzahl_elemente+1)
        ausnutzung_y = [None] * (anzahl_elemente+1)
        ausnutzung_torsion = [None] * (anzahl_elemente+1)
        ausnutzung_tot = [None] * (anzahl_elemente+1)
        biegemoment_m_p = [0] * (anzahl_elemente+1)
        biegewiderstand_tatsaechlich_x = [0]*(anzahl_elemente+1)
        biegewiderstand_tatsaechlich_y = [0]*(anzahl_elemente+1)
        torsionswiderstand_tatsaechlich = [0]*(anzahl_elemente+1)
        #gesamte Windlast [N]
        windlast_gesamt = 0
        for i in range (anzahl_elemente+1):
            torsionsmoment_m[i] = abs(torsionsmoment_m_x[i]*windlast_x + torsionsmoment_m_y[i]*windlast_y)
            windlast_gesamt += math.sqrt( (f_d_x[i]*windlast_x)**2 + (f_d_y[i]*windlast_y)**2)
            if biegewiderstand_tuer_x[i] != 0: #überprüft ob es auf dieser Höhe eine Tür hat
                biegewiderstand_tatsaechlich_x[i] = biegewiderstand_tuer_x[i]
                biegewiderstand_tatsaechlich_y[i] = biegewiderstand_tuer_y[i]
                torsionswiderstand_tatsaechlich[i] = torsionswiderstand_tuer[i]
                ausnutzung_x[i] = biegemoment_m_x[i]*windlast_x/biegewiderstand_tatsaechlich_x[i]
                ausnutzung_y[i] = biegemoment_m_y[i]*windlast_y/biegewiderstand_tatsaechlich_y[i]
                ausnutzung_torsion[i] = torsionsmoment_m[i]/torsionswiderstand_tatsaechlich[i]
                ausnutzung_tot[i] = ausnutzung_x[i] + ausnutzung_y[i] + ausnutzung_torsion[i]
            else: #falls es auf dieser Höhe keine Tür hat
                biegemoment_m_p[i] = math.sqrt( (biegemoment_m_x[i]*windlast_x)**2 + (biegemoment_m_y[i]*windlast_y)**2)
                biegewiderstand_tatsaechlich_x[i] = biegewiderstand_m_x[i]
                biegewiderstand_tatsaechlich_y[i] = biegewiderstand_m_y[i]
                torsionswiderstand_tatsaechlich[i] = torsionswiderstand_m[i]
                ausnutzung_x[i] = biegemoment_m_x[i]*windlast_x/biegewiderstand_tatsaechlich_x[i]
                ausnutzung_y[i] = biegemoment_m_y[i]*windlast_y/biegewiderstand_tatsaechlich_y[i]
                ausnutzung_torsion[i] = torsionsmoment_m[i]/torsionswiderstand_tatsaechlich[i]
                ausnutzung_tot[i] = biegemoment_m_p[i]/biegewiderstand_tatsaechlich_x[i] + ausnutzung_torsion[i] #ohne Tür Biegewiderstand in x- und y-Richtung gleich
        if w == 0:
            ausnutzung_tot_wind_x = ausnutzung_tot.copy()
            einspannmoment_x_wind_x = biegemoment_m_x[0]
            windlast_x_wind_x = windlast_gesamt
        if w == 90:
            ausnutzung_tot_wind_y = ausnutzung_tot.copy()
            einspannmoment_y_wind_y = biegemoment_m_y[0]
            windlast_y_wind_y = windlast_gesamt
        if ausnutzung_max < max(ausnutzung_tot):
            ausnutzung_max = max(ausnutzung_tot)
            windlast_gesamt_massgebend = windlast_gesamt
            windrichtung_massgebend = windrichtung
            windlast_x_massgebend = windlast_x
            windlast_y_massgebend = windlast_y
            biegemoment_m_x_massgebend = biegemoment_m_x.copy()
            biegemoment_m_y_massgebend = biegemoment_m_y.copy()
            torsionsmoment_massgebend = torsionsmoment_m.copy()
            ausnutzung_x_massgebend = ausnutzung_x.copy()
            ausnutzung_y_massgebend = ausnutzung_y.copy()
            ausnutzung_torsion_massgebend = ausnutzung_torsion.copy()
            ausnutzung_tot_massgebend = ausnutzung_tot.copy()

#Berechnungen Schleife 6
    #horizontale Verschiebung
    #einwirkendes Biegemoment auf charakteristischem Niveau, x-Richtung
    biegemoment_char_x = [0] * (anzahl_elemente+1)
    #einwirkendes Biegemoment auf charakteristischem Niveau, y-Richtung
    biegemoment_char_y = [0] * (anzahl_elemente+1)
    #einwirkendes Biegemoment durch eine Einheitslast an der Mastspitze
    biegemoment_1 = [0] * (anzahl_elemente+1)
    #Wert des zu integrierenden Termms: M einwirkend (charakteristisch) * M_1 /(EI), x-Richtung
    element_integrand_x = [0] * (anzahl_elemente+1)
    #Wert des zu integrierenden Termms: M einwirkend (charakteristisch) * M_1 /(EI), y-Richtung
    element_integrand_y = [0] * (anzahl_elemente+1)
    #Wert des ausgerechneten Integrals über delta h, wird aus dem Mittelwert der beiden zu inntegrierenden Termen * delta h berechnet, x-Richtung
    element_integral_resultat_x = [0] * (anzahl_elemente)
    #Wert des ausgerechneten Integrals über delta h, wird aus dem Mittelwert der beiden zu inntegrierenden Termen * delta h berechnet, y-Richtung
    element_integral_resultat_y = [0] * (anzahl_elemente)
    #horizontale Verschiebung [m], bei Biegung um x-Achse
    verschiebung_horizontal_x = 0
    #horizontale Verschiebung [m], bei Biegung um y-Achse
    verschiebung_horizontal_y = 0
    #Flächenträgheitsmoment des entsprechenden Querschnitts, um x-Achse
    flaechentraegheitsmoment_x = [0] * (anzahl_elemente+1)
    #Flächenträgheitsmoment des entsprechenden Querschnitts, um y-Achse
    flaechentraegheitsmoment_y = [0] * (anzahl_elemente+1)
    #EI, Biegesteifigkeit an der entsprechenden Stelle des Querschnitts, um x-Achse
    EI_x = [0] * (anzahl_elemente+1)
    #EI, Biegesteifigkeit an der entsprechenden Stelle des Querschnitts, um y-Achse
    EI_y = [0] * (anzahl_elemente+1)
    #Fläche an der Elementunterkante für den kompletten Querschnitt, nur für Acheckquerschnitte verwendet
    flaeche_ganz_elementunterkante = [0] * (anzahl_elemente+1)
    #Schwerpunktverschiebung des Querschnitts durch das Loch, nur für Achteckquerschnitte verwendet, darf nur bei unverstärkten QS in möglichen späteren Berechnungen angewendet werden!
    schwerpunktverschiebung_elementunterkante = [0] * (anzahl_elemente+1)
    for i in range (anzahl_elemente+1):
        #print("z:" , z_grenze[i])
        biegemoment_char_x[i] = biegemoment_m_x[i]/gamma_Q
        biegemoment_char_y[i] = biegemoment_m_y[i]/gamma_Q
        biegemoment_1[i] = hoehe - z_grenze[i]
        #print("M_char_x:" , biegemoment_char_x[i])
        #print("M_char_y:" , biegemoment_char_y[i])
        #print("M_1:" , biegemoment_1[i])
        #Flächenträgheitsmoment berechnen:
        if form == 2: #Achteck
            if theta[i] == 0:
                flaechentraegheitsmoment_x[i] = (11+8*math.sqrt(2))/12 * ( (d_seite_elementunterkante[i])**4 - (d_seite_elementunterkante[i] - 2*t*math.tan(math.pi/8))**4)
                #print("D:" , d_seite_elementunterkante[i])
                flaechentraegheitsmoment_y[i] = flaechentraegheitsmoment_x[i]
            elif theta[i] != 0:
                flaechentraegheitsmoment_ohne_loch = (11+8*math.sqrt(2))/12 * ( (d_seite_elementunterkante[i])**4 - (d_seite_elementunterkante[i] - 2*t*math.tan(math.pi/8))**4)
                flaeche_ganz_elementunterkante[i] = 8*t*(d_seite_elementunterkante[i]-t/math.tan(3*math.pi/8))
                if breite_tuere_elementunterkante[i] <= d_seite_elementunterkante[i]:
                    schwerpunktverschiebung_elementunterkante[i] = -breite_tuere_elementunterkante[i]*t*(d_seite_elementunterkante[0]/(2*math.tan(math.pi/8)))/(flaeche_ganz_elementunterkante[i] - breite_tuere_elementunterkante[i]*t)
                    flaechentraegheitsmoment_x[i] = flaechentraegheitsmoment_ohne_loch + flaeche_ganz_elementunterkante[i]*schwerpunktverschiebung_elementunterkante[i]**2 - 1/12*breite_tuere_elementunterkante[i]*t**3 - breite_tuere_elementunterkante[i]*t*( (d_seite_elementunterkante[i]/(2*math.tan(math.pi/8))) -0-5*t - schwerpunktverschiebung_elementunterkante[i] )**2
                    flaechentraegheitsmoment_y[i] = flaechentraegheitsmoment_ohne_loch - 1/12*t*breite_tuere_elementunterkante[i]**3
                    if breite_verstaerkung_elementunterkante[i] != 0:  #überprüft ob es eine verstaerkung hat
                        flaeche_verstaerkung = breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]
                        schwerpunktverschiebung_neu = (-breite_tuere_elementunterkante[i]*t*(d_seite_elementunterkante[0]/(2*math.tan(math.pi/8))) + 2*flaeche_verstaerkung*m_0x[i])/(flaeche_ganz_elementunterkante[i] - breite_tuere_elementunterkante[i]*t + 2*flaeche_verstaerkung)
                        if breite_tuere_elementunterkante[i] + 2*breite_verstaerkung_elementunterkante[i] <= d_seite_elementunterkante[i]:
                            beitrag1 = 2*(1/12*breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]**3 + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_neu)**2)
                            flaechentraegheitsmoment_x[i] += (flaeche_ganz_elementunterkante[i]-breite_tuere_elementunterkante[i]*t)*(schwerpunktverschiebung_elementunterkante[i]-schwerpunktverschiebung_neu)**2 + beitrag1
                            flaechentraegheitsmoment_y[i] += 2*breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]*m_0y[i]**2 + 1/6*dicke_verstaerkung_elementunterkante[i]*breite_verstaerkung_elementunterkante[i]**3
                        elif breite_tuere_elementunterkante[i] + 2*breite_verstaerkung_elementunterkante[i] > d_seite_elementunterkante[i]:
                            beitrag1 = 2*( 0.5*1/12*breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]**3 + 0.5*1/12*dicke_verstaerkung_elementunterkante[i]*breite_verstaerkung_elementunterkante[i]**2 + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_neu)**2 )
                            flaechentraegheitsmoment_x[i] += (flaeche_ganz_elementunterkante[i]-breite_tuere_elementunterkante[i]*t)*(schwerpunktverschiebung_elementunterkante[i]-schwerpunktverschiebung_neu)**2 + beitrag1
                            flaechentraegheitsmoment_y[i] += 2*breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]*m_0y[i]**2 + 1/12*( breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]**3 + dicke_verstaerkung_elementunterkante[i]*breite_verstaerkung_elementunterkante[i]**3 )
                elif breite_tuere_elementunterkante[i] > d_seite_elementunterkante[i]:
                    #die Berechnung enthält leichte Vereinfachungen: der Schwerpunkt der Stirnfläche, welche nun aufgrund der Öffnung nicht mehr im Querschnitt enthalten ist, wurde in der Mitte der Dicke angenommen, die seitlichen Komponenten, welche nun nicht mehr vorhanden sind, wurden als Rechteck behandelt.
                    d_aussen = d_seite_elementunterkante[i]
                    r_klein = d_aussen/(2*math.tan(math.pi/8))
                    breite_tuer = breite_tuere_elementunterkante[i]
                    flaechenabzug1 = t*(d_seite_elementunterkante[i]-t/(math.tan(3*math.pi/8)))
                    flaechenabzug2 = math.sqrt(2)/2*(breite_tuere_elementunterkante[i]-d_seite_elementunterkante[i])*t
                    flaechenabzug = flaechenabzug1 + 2*flaechenabzug2
                    schwerpunktverschiebung_elementunterkante[i] = (-flaechenabzug1*(r_klein-0.5*t)-2*flaechenabzug2*(r_klein-0.5*t-0.5*0.5*(breite_tuer-d_aussen)))/(flaeche_ganz_elementunterkante[i]-flaechenabzug)
                    beitrag1 = 1/12*d_aussen*t**3 + flaechenabzug1*(r_klein-0.5*t-schwerpunktverschiebung_elementunterkante[i])**2
                    beitrag2 = 2*( 0.5*1/12*math.sqrt(2)/2*(breite_tuer-d_aussen) *t**3 + 0.5*1/12*t * (math.sqrt(2)/2*(breite_tuer-d_aussen))**3 + flaechenabzug2*( r_klein-0.5*t-0.5*0.5*(breite_tuer-d_aussen)-schwerpunktverschiebung_elementunterkante[i])**2 )
                    flaechentraegheitsmoment_x[i] = flaechentraegheitsmoment_ohne_loch + flaeche_ganz_elementunterkante[i]*schwerpunktverschiebung_elementunterkante[i]**2 - beitrag1 - beitrag2
                    beitrag_y_1 = -1/12*t*(d_seite_elementunterkante[i] - t/(math.tan(3*math.pi/8)))**3 - math.sqrt(2)*t*(breite_tuer-d_seite_elementunterkante[i]) * (d_seite_elementunterkante[i]/4 + breite_tuer/4 - math.sqrt(2)/4*t)**2
                    beitrag_y_2 = -math.sqrt(2)/24*t**3*(breite_tuer-d_seite_elementunterkante[i]) - math.sqrt(2)/48*t*(breite_tuer-d_seite_elementunterkante[i])**3
                    flaechentraegheitsmoment_y[i] = flaechentraegheitsmoment_ohne_loch + beitrag_y_1 + beitrag_y_2
                    if breite_verstaerkung_elementunterkante[i] != 0:  #überprüft ob es eine verstaerkung hat
                        flaeche_verstaerkung = breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]
                        schwerpunktverschiebung_neu = (-flaechenabzug1*(r_klein-0.5*t)-2*flaechenabzug2*(r_klein-0.5*t-0.5*0.5*(breite_tuer-d_aussen)) + 2*flaeche_verstaerkung*m_0x[i])/( flaeche_ganz_elementunterkante[i]-flaechenabzug+2*flaeche_verstaerkung )
                        beitrag1 = 2*( 0.5*1/12*breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]**3 + 0.5*1/12*dicke_verstaerkung_elementunterkante[i]*breite_verstaerkung_elementunterkante[i]**2 + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_neu)**2 )
                        flaechentraegheitsmoment_x[i] += (flaeche_ganz_elementunterkante[i]-flaechenabzug)*(schwerpunktverschiebung_elementunterkante[i]-schwerpunktverschiebung_neu)**2 + beitrag1
                        flaechentraegheitsmoment_y[i] += 2*breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]*m_0y[i]**2 + 1/12*( breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]**3 + dicke_verstaerkung_elementunterkante[i]*breite_verstaerkung_elementunterkante[i]**3 )
        elif form == 1 or form == 3: #kreisförmiger Querschnitt
            if theta[i] == 0:
                flaechentraegheitsmoment_x[i] = math.pi/4* ( (r_m[i]+(t/2))**4 - (r_m[i]-(t/2))**4 )
                flaechentraegheitsmoment_y[i] = flaechentraegheitsmoment_x[i]
            elif theta[i] != 0:
                r_aussen = r_m[i]+(t/2)
                r_innen = r_m[i]-(t/2)
                flaechentraegheitsmoment_x[i] = 1/4*(r_aussen**4-r_innen**4)*(math.pi - theta[i] - math.sin(theta[i])*math.cos(theta[i]) ) + 4/9*(r_aussen**3 - r_innen**3)**2 * math.sin(theta[i])*math.sin(theta[i])* 1/( (r_aussen**2 - r_innen**2)*(math.pi-theta[i])  )
                flaechentraegheitsmoment_y[i] = 1/4*(r_aussen**4-r_innen**4) * (math.pi - theta[i] + math.sin(theta[i])*math.cos(theta[i]))
                if breite_verstaerkung_elementunterkante[i] != 0: #überprüft ob es eine verstaerkung hat
                    flaeche_verstaerkung = breite_verstaerkung_elementunterkante[i]*dicke_verstaerkung_elementunterkante[i]
                    #die folgende Verschiebung berechnet den Abstand vom Schwerpunkt zur x-Achse und nicht die reine Verschiebung des Schwerpunkts durch die Verstärkung.
                    schwerpunktverschiebung_elementunterkante[i] = (2*flaeche_verstaerkung*m_0x[i] - (2/3*(r_aussen**3 - r_innen**3) * math.sin(theta[i])) ) /(2*flaeche_verstaerkung + (r_aussen**2 - r_innen**2)*(math.pi-theta[i]) )
                    beitrag1 = 2*( 1/12*dicke_verstaerkung_elementunterkante[i]**3 *breite_verstaerkung_elementunterkante[i] *math.cos(theta[i])*math.cos(theta[i]) + 1/12*breite_verstaerkung_elementunterkante[i]**3 *dicke_verstaerkung_elementunterkante[i] *math.sin(theta[i])*math.sin(theta[i]) + flaeche_verstaerkung*(m_0x[i]-schwerpunktverschiebung_elementunterkante[i])**2)
                    beitrag2 = (math.pi-theta[i])*(r_aussen**2 - r_innen**2)* (-2/3*(r_aussen**3 - r_innen**3)*math.sin(theta[i])/((r_aussen**2 - r_innen**2)*(math.pi-theta[i]))   + schwerpunktverschiebung_elementunterkante[i] )**2
                    flaechentraegheitsmoment_x[i] += beitrag2 - beitrag1
                    flaechentraegheitsmoment_y[i] += 2*flaeche_verstaerkung*m_0y[i]**2 + 1/6*( breite_verstaerkung_elementunterkante[i]**3 *dicke_verstaerkung_elementunterkante[i] *math.cos(theta[i])**2 + dicke_verstaerkung_elementunterkante[i]**3 *breite_verstaerkung_elementunterkante[i] *math.sin(theta[i])**2 )
        #Je nach Ausrichtung der Türe: flächenträgheitsmomente vertauschen -->m_x etc. sind noch nicht nach der tatsächlichen Asurichtung orientiert.
        if ausrichtung_tuere[i] == "y":
            flaechentraegheitsmoment_x[i], flaechentraegheitsmoment_y[i] = flaechentraegheitsmoment_y[i], flaechentraegheitsmoment_x[i]
        #print("Flächenträgheitsmoment x:" , flaechentraegheitsmoment_x[i])
        #print("Flächenträgheitsmoment y:" , flaechentraegheitsmoment_y[i])
        EI_x[i] = E*1000000 * flaechentraegheitsmoment_x[i] #bei E mal 1'000'000 wegen Einheit
        EI_y[i] = E*1000000 * flaechentraegheitsmoment_y[i] #bei E mal 1'000'000 wegen Einheit
        #print("EI_x:" , EI_x[i])
        #print("EI_y:" , EI_y[i])
        element_integrand_x[i] = (biegemoment_char_x[i]*biegemoment_1[i])/(EI_x[i])
        element_integrand_y[i] = (biegemoment_char_y[i]*biegemoment_1[i])/(EI_y[i])
        #print("Element Integral x" , element_integrand_x[i])
        #print("Element Integral y" , element_integrand_y[i])
        #print()
        if i > 0:
            element_integral_resultat_x[i-1] = 0.5*(element_integrand_x[i-1] + element_integrand_x[i])*delta_h[i-1]
            element_integral_resultat_y[i-1] = 0.5*(element_integrand_y[i-1] + element_integrand_y[i])*delta_h[i-1]
            verschiebung_horizontal_x += element_integral_resultat_x[i-1]
            verschiebung_horizontal_y += element_integral_resultat_y[i-1]
    #print("horizontale Verschiebung der Mastspitze x:" , verschiebung_horizontal_x*1000 , "mm")
    #print("horizontale Verschiebung der Mastspitze y:" , verschiebung_horizontal_y*1000 , "mm")
    #print("zulässige horizontale Verschiebung:" , verschiebung_zugelassen*hoehe*1000 , "mm")
    #if verschiebung_horizontal_x <= verschiebung_zugelassen*hoehe and verschiebung_horizontal_y <= verschiebung_zugelassen*hoehe:
        #print("horizontale Verformungen i.O.")
    #else:
        #print("horizontale Verformungen zu gross.")

#Darstellung der Resultate
if inputkontrolle == True:    
    #Ergebnisse
    #print("Ergebnisse")
    #print("Gewicht G [N]:" , gewicht_gesamt)
    #print("massgebende Windrichtung [°]:" , windrichtung_massgebend*180/math.pi)
    #print("0° = Wind in Richtung der x-Achse, 90° = Wind in Richtung der y-Achse")
    #print("gesamte massgebende Windlast [N]:" , windlast_gesamt_massgebend)
    #print("gesamte Windlast [N], Wind aus x-Richtung:" , round(windlast_x_wind_x,2))
    #print("gesamte Windlast [N], Wind aus y-Richtung:" , round(windlast_y_wind_y,2))
    #print("Einspannbiegemomentmoment x [Nm] bei massgebender Windrichtung:" , biegemoment_m_x_massgebend[0]*windlast_x_massgebend)
    #print("Einspannbiegemomentmoment y [Nm] bei massgebender Windrichtung:" , biegemoment_m_y_massgebend[0]*windlast_y_massgebend)
    #print("Einspannbiegemoment x [Nm] bei Wind aus x-Richtung:" ,round(einspannmoment_x_wind_x,2))
    #print("Einspannbiegemoment y [Nm] bei Wind aus y-Richtung:" ,round(einspannmoment_y_wind_y,2))
    #print("Torsionsmoment Einspannung [Nm]:" , torsionsmoment_massgebend[0])
    #print()
    #print("GZ Tragsicherheit")
    #for i in range (anzahl_elemente+1):
       #print("z[m]:" , round(z_grenze[i],5) , "Ausnutzung:" , round(ausnutzung_tot_massgebend[i]*100,3) , "%") 
    maximale_ausnutzung = max(ausnutzung_tot_massgebend)
    index_maximale_ausnutzung = ausnutzung_tot_massgebend.index(maximale_ausnutzung)
    #print("Maximale Ausnutzung:" , round(maximale_ausnutzung*100,3), "%", "in der Höhe:" ,  round(z_grenze[index_maximale_ausnutzung],5))
    #print("GZ Gebrauchstauglichkeit")
    #print("horizontale Verschiebung der Mastspitze in x-Richtung:" , verschiebung_horizontal_x*1000 , "mm")
    #print("horizontale Verschiebung der Mastspitze in y-Richtung:" , verschiebung_horizontal_y*1000 , "mm")
    #print("zulässige horizontale Verschiebung:" , verschiebung_zugelassen*hoehe*1000 , "mm")
    #if verschiebung_horizontal_x <= verschiebung_zugelassen*hoehe and verschiebung_horizontal_y <= verschiebung_zugelassen*hoehe:
        #print("horizontale Verformungen i.O.")
    #else:
        #print("horizontale Verformungen zu gross.")
    #print("Ausnutzung:" , max(verschiebung_horizontal_x,verschiebung_horizontal_y)/(verschiebung_zugelassen*hoehe)*100 , "%")
    #print()
    
    sheet.append(["Gewicht G [N]:" , round(gewicht_gesamt,2)])
    sheet.append(["massgebende Windrichtung [°]:" , round(windrichtung_massgebend*180/math.pi,2)])
    sheet.append(["0° = Wind in Richtung der x-Achse, 90° = Wind in Richtung der y-Achse"])
    sheet.append(["gesamte massgebende Windlast [N]:" , round(windlast_gesamt_massgebend,2)])
    sheet.append(["gesamte Windlast [N], Wind aus x-Richtung:" , round(windlast_x_wind_x,2)])
    sheet.append(["gesamte Windlast [N], Wind aus y-Richtung:" , round(windlast_y_wind_y,2)])
    sheet.append(["Einspannbiegemoment x [Nm] bei massgebender Windrichtung:" , round(biegemoment_m_x_massgebend[0]*windlast_x_massgebend,2)])
    sheet.append(["Einspannbiegemoment y [Nm] bei massgebender Windrichtung:" , round(biegemoment_m_y_massgebend[0]*windlast_y_massgebend,2)])
    sheet.append(["Einspannbiegemoment x [Nm] bei Wind aus x-Richtung:" ,round(einspannmoment_x_wind_x,2)])
    sheet.append(["Einspannbiegemoment y [Nm] bei Wind aus y-Richtung:" ,round(einspannmoment_y_wind_y,2)])
    sheet.append(["Torsionsmoment Einspannung [Nm]:" , round(torsionsmoment_massgebend[0],2)])
    sheet.append([])
    sheet.append(["GZ Gebrauchstauglichkeit"])
    sheet.append(["horizontale Verschiebung der Mastspitze x:" , round(verschiebung_horizontal_x*1000,2) , "mm"])
    sheet.append(["horizontale Verschiebung der Mastspitze y:" , round(verschiebung_horizontal_y*1000,2) , "mm"])
    sheet.append(["zulässige horizontale Verschiebung:" , verschiebung_zugelassen*hoehe*1000 , "mm"])
    if verschiebung_horizontal_x <= verschiebung_zugelassen*hoehe and verschiebung_horizontal_y <= verschiebung_zugelassen*hoehe:
        sheet.append(["horizontale Verformungen i.O."])
    else:
        sheet.append(["horizontale Verformungen zu gross."])
    sheet.append(["Ausnutzung:" , round(max(verschiebung_horizontal_x,verschiebung_horizontal_y)/(verschiebung_zugelassen*hoehe)*100,2) , "%"])
    sheet.append([])
    
    sheet.append(["GZ Tragsicherheit"])
    sheet.append(["massgebende Windrichtung","","","","","","","","x-Richtung","","","","","y-Richtung"])
    sheet.append([])
    maximale_ausnutzung = max(ausnutzung_tot_massgebend)
    index_maximale_ausnutzung = ausnutzung_tot_massgebend.index(maximale_ausnutzung)
    maximale_ausnutzung_wind_x = max(ausnutzung_tot_wind_x)
    index_maximale_ausnutzung_wind_x = ausnutzung_tot_wind_x.index(maximale_ausnutzung_wind_x)
    maximale_ausnutzung_wind_y = max(ausnutzung_tot_wind_y)
    index_maximale_ausnutzung_wind_y = ausnutzung_tot_wind_y.index(maximale_ausnutzung_wind_y)
    sheet.append(["Maximale Ausnutzung:","","", round(maximale_ausnutzung*100,3), "%", "in der Höhe [m]:" ,  round(z_grenze[index_maximale_ausnutzung],5),"",round(maximale_ausnutzung_wind_x*100,3), "%", "in der Höhe [m]:" ,  round(z_grenze[index_maximale_ausnutzung_wind_x],5),"",round(maximale_ausnutzung_wind_y*100,3), "%", "in der Höhe [m]:" ,  round(z_grenze[index_maximale_ausnutzung_wind_y],5)])
    for i in range (anzahl_elemente+1):
       sheet.append(["z[m]:" , round(z_grenze[i],5) , "Ausnutzung:" , round(ausnutzung_tot_massgebend[i]*100,3) , "%","","","",round(ausnutzung_tot_wind_x[i]*100,3),"%","","","",round(ausnutzung_tot_wind_y[i]*100,3),"%"])
    
#Inputkontrolle 2     
elif inputkontrolle == False:
    if inputfehler == 1:
        sheet.append(["Der Biegewiderstand kann nicht ermittelt werden, da der Querschnitt zu dünn ist. Es ist nicht mehr möglich, den Beiwert phi_1 gemäss SN-EN 40-3-3, Bild 2 zu bestimmen."])
    elif inputfehler == 2:
        sheet.append(["Die Breite einer Tür übersteigt 80% des Durchmessers auf dieser Höhe."])
    #print("Input ist falsch.")
    sheet.append(["Bitte überprüfen sie den Input."])

#workbook speichern
workbook.save('Resultate_Standsicherheit.xlsx') #Die neue Excel Datei wird im gleichen Ordner gespeichert wie die Jupyter Datei