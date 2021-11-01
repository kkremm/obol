import sys
print(sys.version)
import csv
import ephem as ep
from math import degrees

def float_deg(input):
    return degrees(float(input))

#specify location
settings_mode=str(input("mode [new]/[old]: "))

if settings_mode == "new" or settings_mode == "n":
    print("---input coord or city---")
    city=str(input("city: "))
    if city != "":
        location=ep.city(city)
        location.date = ep.now() #date must be input as GMT

    else:
        lat=input("latitude: ")
        lon=input("longitude: ")
        elevation=float(input("elevation: "))
        location=ep.Observer()
        location.lat, location.lon, location.elevation = lat, lon, elevation

elif settings_mode == "old" or settings_mode == "o":
    # reuse old settings
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


else:
    print("please only enter 'new' or 'old'")
    pass

location.date = ep.now() #date must be input as GMT


# save settings
with open(r"saved_settings.txt", "w") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([location.lat])
    csv_writer.writerow([location.lon])
    csv_writer.writerow([location.elevation])

# return to check info
print("\nlat: ",float_deg(location.lat))
print("lon: ",float_deg(location.lon))
print("alt: ",location.elevation)
print("time (GMT): ",location.date)
print("")

# calibration
print("---proceding to calibration---")
exec(open(r"calibration.py").read())
