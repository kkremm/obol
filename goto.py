import csv
import ephem as ep
from math import degrees

def float_deg(input):
    return degrees(float(input))

def current_alt(idk):
    return float_deg(idk.alt)

def current_az(idk):
    return float_deg(idk.az)

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
    while True:
        planet_or_star = input("[star]/[planet]: ")

        if planet_or_star=="planet" or planet_or_star == "p":
            plvar=input("enter planet: ")
            try:
                desired_object = eval("ep."+norm(plvar)+"(location)")
            except:
                print("\n------/!!\------\nplease enter a valid planet\n------/!!\------\n\n")
            else:
                break

        elif planet_or_star=="star" or planet_or_star == "s":
            strvar=norm(input("enter star: "))
            try:
                desired_object = ep.star(strvar)
            except:
                print("\n------/!!\------\nplease enter a valid star\n------/!!\------\n\n")
            else:
                desired_object.compute(location)
                break

        elif planet_or_star == "exit":
            import board
            from adafruit_motorkit import MotorKit
            from adafruit_motor import stepper
            kit= MotorKit(adress=0x61)
            kit.stepper1.release()
            kit.stepper2.release()
            exit()

        else:
            print("\n------/!!\------\nplease enter a valid mode\n------/!!\------\n\n")

    print("\n"+desired_object.name+"'s location: ")
    print("altitude: ",current_alt(desired_object))
    print("azimut: ",current_az(desired_object))
    print("\n---pointing "+desired_object.name+"---")

    if current_alt(desired_object)<0:
        print("\n------/!!\------\nplease choose visible object\n------/!!\------\n\n")
    else:
        break

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
pos2_alt=current_alt(desired_object)

pos1_az=list[1]
pos2_az=current_az(desired_object)

print("to travel alt: ", to_travel_alt(pos1_alt, pos2_alt))
print("to travel az: ", to_travel_az(pos1_az, pos2_az))




pos1_alt=list[0]
pos2_alt=current_alt(desired_object)

pos1_az=list[1]
pos2_az=current_az(desired_object)

# update last_known_position
location.date = ep.now()

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


with open(r"last_known_position.txt", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([current_alt(desired_object)])
    csv_writer.writerow([current_az(desired_object)])

time.sleep(1)

print("\n-----telescope pointed at "+desired_object.name+"---")
exec(open(r"option_menu.py").read())
