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

def MPU_Init():
    #reset all sensors, Bit-7 is set to 0 after reset, sleep for allowing to settle after reset
    bus.write_byte_data(MPU_Address, PWR_MGMT_1, 128)
    sleep(3)

    #Setting the sample rate
    #Setting to 128 while setting DLPF_CFG (part of CONFIG) to 0 sets sample rate to 1 kHz
    #Since Accelerometer output is always 1kHz, sample rate is set to 1kHZ (Change? -> See p.12 on MPU register sheet)
    bus.write_byte_data(MPU_Address, SMPLRT_DIV, 128)

    # Write to power management register
    # Connect clock to gyroscope x-axis (improved accuracy) and disable temperature sensor
    bus.write_byte_data(MPU_Address, PWR_MGMT_1, 9)

    # Write to Configuration register
    # Set Bandwidth Acc to 260Hz (Fs=1kHz) and Gyro to 256 Hz (Fs=8kHz)
    bus.write_byte_data(MPU_Address, CONFIG, 0)

    # Write to Gyro configuration register: set gyro scale range to ±250°/s
    # Ranges: (±250:0; ±500:8; ±1000:16; ±2000:24)
    bus.write_byte_data(MPU_Address, GYRO_CONFIG, 0)

    # Write to Acc configuration register: set acc scale to ±4g
    # Set Accelerometer Range (±2g:0; ±4g:8; ±8g:16; ±16g:24)
    bus.write_byte_data(MPU_Address, ACCEL_CONFIG, 8)

    # Write to interrupt enable register
    # Enables the Data Ready interrupt (higher quality data)
    bus.write_byte_data(MPU_Address, INT_ENABLE, 1)

def MPU_read_raw_data(addr):
    # Accel and Gyro values are 16-bit (2 registers, high (MSB) and low (LSB))
    # High Endian because low byte is at higher address!
    # Info: Max. 2-byte Value is 65535 (unsigned)
    high = bus.read_byte_data(MPU_Address, addr)
    low = bus.read_byte_data(MPU_Address, addr + 1)

    # concatenate higher and lower value: Shifting the high byte to the left by 8 bits!
    value = ((high << 8) | low)

    # Get signed value from MPU6050
    if (value > 32768):
        value = value - 65536
    return value

def scalefactor():
    #Determine range and define scale factor based on that
    global scalegyro
    global scaleacc
    rangegyro = bus.read_byte_data(MPU_Address, GYRO_CONFIG)
    rangeacc = bus.read_byte_data(MPU_Address, ACCEL_CONFIG)

    if rangegyro == 0:
        #print ('Range of Gyro is ±250 °/s')
        scalegyro = 131
    elif rangegyro == 8:
        scalegyro = 65.5
        #print('Range of Gyro is ±500 °/s')
    elif rangegyro == 16:
        scalegyro = 32.8
        #print('Range of Gyro is ±1000 °/s')
    elif rangegyro == 24:
        scalegyro = 16.4
        #print('Range of Gyro is ±2000 °/s')
    else:
        sleep(1)
        #print('Set Gyro cale is not available')

    if rangeacc == 0:
        #print ('Range of Accelerometer is ±2g')
        scaleacc = 16384
    elif rangeacc == 8:
        scaleacc = 8192
        #print('Range of Accelerometer is ±4g')
    elif rangeacc == 16:
        scaleacc = 4096
        #print('Range of Accelerometer is ±8g')
    elif rangeacc == 24:
        scaleacc = 2048
        #print('Range of Accelerometer is ±16g')
    else:
        sleep(1)
        #print('Set Accelerometer scale is not available')
    #print ('If other scale range is desired, change in function MPU_init at GYRO_CONFIG AND ACCEL_.CONFIG.')

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
    Ax_mpu = round(MPU_read_raw_data(ACCEL_XOUT_H) / scaleacc,4)
    Az_mpu = round(MPU_read_raw_data(ACCEL_YOUT_H) / scaleacc,4)
    Ay_mpu = round(MPU_read_raw_data(ACCEL_ZOUT_H) / scaleacc,4)

    Time1 = str(datetime.now())
    Time2 = round(time.time(),5)
    data = [Time1, Time2, Ax_mpu, Ay_mpu, Az_mpu]

def write_csv_internal (data, i):
        #write list 'data' to csv file as new row
        with open('/home/pi/Vibration_MPU/Vibration_MPUA_{}.csv'.format(i), 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(data)

def save_csv_and_img ():
    global i
    #initializing camera (all camera lines commented out for maximum sample rate)
    #camera = PiCamera()
    #camera.rotation = 180

    #Create enumerated csv file and name its columns
    i=0
    while os.path.exists('Vibration_MPU/Vibration_MPUA_{}.csv'.format(i)):
        i += 1                  
    with open('/home/pi/Vibration_MPU/Vibration_MPUA_{}.csv'.format(i), 'w', newline='') as outcsv:
        writer = csv.writer(outcsv)
        writer.writerow(['Date and Timestamp (string)','Timestamp (float)', 'X-Acc MPU [g]', 'Y-Acc MPU [g]', 'Z-Acc MPU [g]'])

    #Create directory for camera images
    #dir = '/home/pi/Images_Camera/{}'.format(i)
    #if not os.path.exists(dir):
        #os.mkdir(dir)

    #Endless Loop for Data and Image saving, only executed as long as switch is set to 'HIGH'
    while GPIO.input(12) == GPIO.HIGH:
        create_data()
        write_csv_internal(data,i)
        #sleep(t) ; commented out to reach maximum sample rate

        #Take photo every 'img' seconds
        #recent_time = time.time()
        #if recent_time - start_time >= img:
            #d = data[0]
            #camera.capture('/home/pi/Images_Camera/{}/{}.jpg'.format(i,d))
            #start_time = recent_time

###ACTUAL PROGRAM
bus = smbus2.SMBus(1)  # initialize smbus
MPU_Init()
scalefactor()
set_frequency()
sleep (1) #allow sensor to settle after initialisation

#Checking every 3 second wether switch is set to HIGH -> triggers data saving process
while True:
    if GPIO.input(12) == GPIO.HIGH:
        save_csv_and_img()
    if GPIO.input(12) == GPIO.LOW:
        sleep(3)