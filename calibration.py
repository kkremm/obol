print("\n\n-----calibration module-----\n")

import csv
import ephem as ep
from math import degrees

import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit(address=0x61)

def float_deg(input):
    return degrees(float(input))

def current_alt(idk):
    return float_deg(idk.alt)

def current_az(idk):
    return float_deg(idk.az)

def norm(idk):
    return str(idk).capitalize()

def release_mot():
    kit.stepper1.release()
    kit.stepper2.release()

with open(r'saved_settings.txt', 'r') as csv_file:
    list = []
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if row == []:
            pass
        else:
            list.append(row[0])
location=ep.Observer()
location.lat, location.lon, location.elevation = list[0], list[1], float(list[2])
location.date = ep.now() #date must be input as GMT
# ----
while True:
    while True:
        calibration_mode = input("calibration mode [polaris]/[custom star]/[planet]: ")

        if calibration_mode=="polaris" or calibration_mode=="pol":
            desired_object = ep.star("Polaris")
            desired_object.compute(location)
            break

        elif calibration_mode=="planet" or calibration_mode=="pl":
            plvar=input("enter planet: ")
            try:
                desired_object = eval("ep."+norm(plvar)+"(location)")
            except:
                print("\n------/!!\------\nplease enter a valid planet\n------/!!\------\n\n")
            else:
                break

        elif calibration_mode=="custom star" or calibration_mode=="custom" or calibration_mode=="star":
            strvar=norm(input("enter star: "))
            try:
                desired_object = ep.star(strvar)
            except:
                print("\n------/!!\------\nplease enter a valid star\n------/!!\------\n\n")
            else:
                desired_object.compute(location)
                break

        elif planet_or_star == "exit":
            exit()

        else:
            print("\n------/!!\------\nplease enter a valid mode\n------/!!\------\n\n")

    print("\n"+desired_object.name+"'s location: ")
    print("altitude: ",current_alt(desired_object))
    print("azimut: ",current_az(desired_object))

    if current_alt(desired_object)<0:
        print("\n------/!!\------\nplease choose visible object\n------/!!\------\n\n")
    else:
        break

print("\n---please point to reference object---")

# -----------------------------------------------
import tkinter
cadre=tkinter.Tk()
cadre.geometry("800x200")

last_known_position_alt=0
last_known_position_az=0

pas_az=tkinter.Scale(cadre, #azimut
                    orient="horizontal",
                    length=300,
                    troughcolor='red',
                    sliderlength=10,
                    from_=0,
                    to=50,
                    tickinterval=5)
pas_az.set(10)
pas_az.place(x=70,y=0)
tkinter.Label(text='pas azimut: ').place(x=10,y=20)

pas_alt=tkinter.Scale(cadre, #altitude
                    orient="horizontal",
                    length=300,
                    troughcolor='green',
                    sliderlength=10,
                    from_=0,
                    to=50,
                    tickinterval=5)

pas_alt.set(10)
pas_alt.place(x=470,y=0)
tkinter.Label(cadre,text='step altitude: ').place(x=410,y=20)
tkinter.Label(cadre,text=r'Appuyez sur les fleches pour pointer le telescope vers une etoile connue ... ').place(x=50,y=80)

val_az=tkinter.Label(cadre,text='azimut')
val_az.place(x=100,y=100)
val_alt=tkinter.Label(cadre,text='altitude')
val_alt.place(x=500,y=100)
confirm_puher=tkinter.Button(cadre, text="telescope pointed ?",
                    command=cadre.quit,
                    background='light blue',
                    activebackground='red')

confirm_puher.place(x=350,y=150)

def action_alt():
    val_alt.config(text=("altitude: ", round(last_known_position_alt+moteurs.alt_diff*0.1, 2)) )

def action_az():
    val_az.config(text=("azimut: ", round(last_known_position_az+moteurs.az_diff*0.1, 2)) )

def moteurs(evt):
    s_time=1/100

    if evt.keysym=='Down':
        moteurs.alt_diff=moteurs.alt_diff-pas_alt.get()
        action_alt()

        for m in range(0,pas_alt.get(),1):
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
            time.sleep(s_time)


    if evt.keysym=='Up':
        moteurs.alt_diff=moteurs.alt_diff+pas_alt.get()
        action_alt()

        for m in range(0,pas_alt.get(),1):
            kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
            time.sleep(s_time)

    if evt.keysym=='Right':
        moteurs.az_diff=moteurs.az_diff+pas_az.get()
        action_az()

        for m in range(0,pas_az.get(),1):
            kit.stepper2.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
            time.sleep(s_time)

    if evt.keysym=='Left':
        moteurs.az_diff=moteurs.az_diff-pas_az.get()
        action_az()

        for m in range(0,pas_az.get(),1):
            kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
            time.sleep(s_time)


moteurs.az_diff=0
moteurs.alt_diff=0
cadre.bind('<Key>',moteurs)
cadre.mainloop()
cadre.quit
# --------------------------------
location.date = ep.now() #date must be input as GMT
if calibration_mode=="polaris" or or calibration_mode=="pol":
    desired_object = ep.star("Polaris")
    desired_object.compute(location)

elif calibration_mode=="planet" or calibration_mode=="pl":
    desired_object = eval("ep."+norm(plvar)+"(location)")

elif calibration_mode=="custom star" or calibration_mode=="custom" or calibration_mode=="star":
    desired_object = ep.star(strvar)
    desired_object.compute(location)

# set desired_object's alt az as last_known_position (via csv_writer)
with open(r'last_known_position.txt', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([current_alt(desired_object)])
    csv_writer.writerow([current_az(desired_object)])

print("calibration complete")


exec(open(r"option_menu.py").read())
