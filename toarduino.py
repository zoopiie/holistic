import serial
import time
ser = serial.Serial('COM3', 9600)
def write_read(x):
    ser.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = ser.readline()
    return data

while True:
    red = int((input("Enter red: ")))# Taking input from user
    blue = int((input("Enter blue: ")))
    green = int((input("Enter green: ")))
    if red < 10:
        red = '00{}'.format(red)
    elif 10 <= red < 100:
        red = '0{}'.format(red)
    if blue < 10:
        blue = '00{}'.format(blue)
    elif 10 <= blue < 100:
        blue = '0{}'.format(blue)
    if green < 10:
        green = '00{}'.format(green)
    elif 10 <= green < 100:
        green = '0{}'.format(green)
    color = '{}{}{}'.format(red, green, blue)
    print(color)


    ser.write(bytes(color, 'utf-8'))
