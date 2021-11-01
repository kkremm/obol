print("\n\n-----manual mode-----\n")

import csv
import ephem as ep
from math import degrees

import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

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

with open(r"last_known_position.txt", "r") as csv_file:
    list = []
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if row == []:
            pass
        else:
            list.append(float(row[0]))
#--
pos1_alt=list[0]
pos1_az=list[1]
kit = MotorKit(address=0x61)

import tkinter
cadre=tkinter.Tk()
cadre.geometry("800x200")

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

val_az=tkinter.Label(cadre,text=('azimut: ', round(pos1_az, 1)))
val_az.place(x=100,y=100)
val_alt=tkinter.Label(cadre,text=('altitude: ', round(pos1_alt, 1)))
val_alt.place(x=500,y=100)
confirm_puher=tkinter.Button(cadre, text="telescope pointed ?",
                    command=cadre.quit,
                    background='light blue',
                    activebackground='red')

confirm_puher.place(x=350,y=150)

def action_alt():
    val_alt.config(text=("altitude: ", round(pos1_alt+moteurs.alt_diff*0.1, 1)) )

def action_az():
    val_az.config(text=("azimut: ", round(pos1_az+moteurs.az_diff*0.1, 1)) )

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

to_add_alt= moteurs.alt_diff * 0.1
to_add_az= moteurs.az_diff * 0.1

with open(r'last_known_position.txt', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([pos1_alt+to_add_alt])
    csv_writer.writerow([pos1_az+to_add_az])

#release_mot()
print(r"\n-----telescope pointed at:  " +str(pos1_alt+to_add_alt)+ "  ,  " +str(pos1_az + to_add_az)+ "  ---")
exec(open(r"option_menu.py").read())
