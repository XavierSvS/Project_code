# Import required packages
import smbus2  # import SMBus module of I2C
import time
from time import sleep
from datetime import datetime
import csv
import os
from picamera import PiCamera
import RPi.GPIO as GPIO

#MPU6050 Registers and their Address
MPU_Address = 0x68  # I2C device address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_CONFIG = 0x1C
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47
#ADXL345 Registers and their Address
ADXL_Address = 0x53  # I2C Device Adress
ADXL_OUTPUTRATE = 0x2C
ADXL_POWER_CTL = 0x2D
ADXL_DATA_FORMAT = 0x31
ADXL_DATAX0 = 0x32
ADXL_DATAX1 = 0x33
ADXL_DATAY0 = 0x34
ADXL_DATAY1 = 0x35
ADXL_DATAZ0 = 0x36
ADXL_DATAZ1 = 0x37
#Switch adress and setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.IN)

def ADXL_Init():
    # Sets Output rate to 800 Hz (most suitable to MPU rate = 1000Hz while having same power consumption as 100 Hz)
    bus.write_byte_data(ADXL_Address, ADXL_OUTPUTRATE, 13)

    # Set Sensor into Read mode
    bus.write_byte_data(ADXL_Address, ADXL_POWER_CTL, 8)

    # Set acc-range to ±4g and (p.27 data sheet) -> 11 bit output now!, right justified
    # ATTENTION: When changing the range, function ADXL_read_raw_data needs to be adjusted because the
    # bit resolution will change too!!! (change values 0x07 and 1024/2048)
    bus.write_byte_data(ADXL_Address, ADXL_DATA_FORMAT, 9)

def ADXL_read_raw_data(addr):
    # Read data back from 0x32(50), 2 bytes
    # X-Axis LSB, X-Axis MSB
    data0 = bus.read_byte_data(ADXL_Address, addr)
    data1 = bus.read_byte_data(ADXL_Address, addr+1)

    # Combine the values from two registers to 11-bits (±4g range)
    value = ((data1 & 0x07) * 256) + data0

    # to get signed value
    if (value > 1024):
        value = value - 2048
    return value

def set_frequency():
    global Fs
    global t
    global img
    Fs = 500
    t = 1/Fs
    img = 5
    #print('Data Saving-Frequency is {} Hz. It can be changed in function set_frequency(). Photo is being taken every {} seconds.'.format(Fs, img))

def create_data():
    global data
    Ax_adxl = round(ADXL_read_raw_data(ADXL_DATAX0) * 0.004, 4)
    Ay_adxl = round(ADXL_read_raw_data(ADXL_DATAY0) * 0.004, 4)
    Az_adxl = round(ADXL_read_raw_data(ADXL_DATAZ0) * 0.004, 4)

    Time1 = str(datetime.now())
    Time2 = time.time()
    data = [Time1, Time2, Ax_adxl, Ay_adxl, Az_adxl]

def write_csv_internal (data, i):
        with open('/home/pi/Vibration_ADXL/Vibration_ADXL_{}.csv'.format(i), 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(data)

def save_csv_and_img ():
    global i
    #initializing camera (all camera lines commented out for maximum sample rate)
    #camera = PiCamera()
    #camera.rotation = 180

    #Create enumerated csv file and name its columns
    i = 0
    while os.path.exists('Vibration_ADXL/Vibration_ADXL_{}.csv'.format(i)):
        i += 1                  
    with open('/home/pi/Vibration_ADXL/Vibration_ADXL_{}.csv'.format(i), 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(['Date and Timestamp (string)','Timestamp (float)', 'X-Acc ADXL [g]', 'Y-Acc ADXL [g]', 'Z-Acc ADXL [g]'])

    # Create directory for camera images
    # dir = '/home/pi/Images_Camera/{}'.format(i)
    # if not os.path.exists(dir):
    # os.mkdir(dir)

    # Endless Loop for Data and Image saving, only executed as long as switch is set to 'HIGH'
    while GPIO.input(12) == GPIO.HIGH:
        create_data()
        write_csv_internal(data, i)
        # sleep(t) ; commented out to reach maximum sample rate

        # Take photo every 'img' seconds
        # recent_time = time.time()
        # if recent_time - start_time >= img:
        # d = data[0]
        # camera.capture('/home/pi/Images_Camera/{}/{}.jpg'.format(i,d))
        # start_time = recent_time
            
###ACTUAL PROGRAM
bus = smbus2.SMBus(1)  # initialize smbus
ADXL_Init()
set_frequency()
sleep (1) #allow sensor to settle after initialisation

#Checking every 3 second wether switch is set to HIGH -> triggers data saving process
while True:
    if GPIO.input(12) == GPIO.HIGH:
        save_csv_and_img()
    if GPIO.input(12) == GPIO.LOW:
        sleep(3)