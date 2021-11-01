import csv
import ephem as ep
from math import degrees

def float_deg(input):
    return degrees(float(input))

def norm(idk):
    return str(idk).capitalize()

def to_travel_az(A, B):
    sol1= abs(A-B)
    sol2= 360-max(A, B) + min(A, B)
    sol= min(sol1, sol2)
    if sol1<sol2:
        if A<=B:
            pass
        else:
            sol*=-1
    else:
        if A<=B:
            sol*=-1
        else:
            pass
    return(sol)

def to_travel_alt(A, B):
    return(B-A)

# get saved_settings
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

# user input loop
while True:
    confirm_choise = input("reset telescope? [Y]/[n]: ")

    if confirm_choise=="Y":
        zenith_alt=90
        zenith_az=0
        print("\n-----reseting telescope---\n")
        break

    elif confirm_choise=="n":
        exec(open(r"option_menu.py").read())
        break

    else:
        print("\n------/!!\------\nplease enter a valid mode\n------/!!\------\n\n")



# get last_known_position
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
pos2_alt=zenith_alt

pos1_az=list[1]
pos2_az=zenith_az

print("to travel alt: ", to_travel_alt(pos1_alt, pos2_alt))
print("to travel az: ", to_travel_az(pos1_az, pos2_az))




import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit(address=0x61)

alt_steps=int(10*round(to_travel_alt(pos1_alt, pos2_alt), 0))
az_steps=int(10*round(to_travel_az(pos1_az, pos2_az), 0))
alt_s_time=1/100
az_s_time=1/100

if alt_steps < 0:
    for i in range(abs(alt_steps)):
        kit.stepper1.onestep(style=stepper.INTERLEAVE)
        time.sleep(alt_s_time)
else:
    for i in range(abs(alt_steps)):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        time.sleep(alt_s_time)
print(r":)")
if az_steps > 0:
    for i in range(abs(az_steps)):
        kit.stepper2.onestep(style=stepper.INTERLEAVE)
        time.sleep(az_s_time)
else:
    for i in range(abs(az_steps)):
        kit.stepper2.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
        time.sleep(az_s_time)

kit.stepper1.release()
kit.stepper2.release()

with open(r'last_known_position.txt', 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([90])
    csv_writer.writerow([0])

time.sleep(1)

print("\n-----telescope reseted-----")
