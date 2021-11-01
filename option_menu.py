print("\n\n-----option menu-----\n")
option_mode = input("option mode [goto]/[manual]/[calibrate]/[release motors]/[reset telescope]: ")

while True:
    if option_mode=="goto":
        exec(open(r"goto.py").read())
        break

    elif option_mode=="manual" or option_mode=="man":
        exec(open(r"manual_mode.py").read())
        break

    elif option_mode=="calibrate" or option_mode=="cal":
        exec(open(r"calibration.py").read())
        break

    elif option_mode=="release motors" or option_mode=="release":
        exec(open(r"release.py").read())
        break

    elif option_mode=="reset telescope" or option_mode=="reset":
        exec(open(r"reset.py").read())
        break

    elif option_mode=="exit":
        import board
        from adafruit_motorkit import MotorKit
        from adafruit_motor import stepper
        kit= MotorKit(adress=0x61)
        kit.stepper1.release()
        kit.stepper2.release()
        exit()

    else:
        print("\n------/!!\------\nplease enter a valid mode\n------/!!\------\n\n")
