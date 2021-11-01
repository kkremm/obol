import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit(address=0x61)


kit.stepper1.release()
kit.stepper2.release()
print("\n-----telescope released---\n")
exec(open(r"option_menu.py").read())
