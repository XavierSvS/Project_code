import smbus2
import time
import board
import adafruit_dht
import gps
from gpiozero import LED  # Example: LED to indicate data logging
from datetime import datetime

# Initialize sensors
mpu_addr = 0x68
bus = smbus2.SMBus(1)
bus.write_byte_data(mpu_addr, 0x6B, 0)  # Wake up MPU6050

# GPS module initialization
session = gps.gps(mode=gps.WATCH_ENABLE)

# Temperature and humidity sensor (DHT22)
dht22 = adafruit_dht.DHT22(board.D17)

# LED indicator (optional)
led = LED(18)

# Function to read MPU6050 accelerometer data
def read_mpu6050():
    accel_x = bus.read_word_data(mpu_addr, 0x3B)
    accel_y = bus.read_word_data(mpu_addr, 0x3D)
    accel_z = bus.read_word_data(mpu_addr, 0x3F)
    return accel_x, accel_y, accel_z

# Function to get GPS coordinates
def get_gps_data():
    while True:
        report = session.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                return report.lat, report.lon
        time.sleep(1)

# Function to read temperature and humidity from DHT22
def read_dht22():
    try:
        temperature = dht22.temperature
        humidity = dht22.humidity
        return temperature, humidity
    except RuntimeError as error:
        return None, None

# Get GPS coordinates to name the data file
latitude, longitude = get_gps_data()
date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"data_{latitude}_{longitude}_{date_str}.txt"

print(f"Saving data to file: {file_name}")

# Main loop: collect data every 10 seconds
while True:
    accel_x, accel_y, accel_z = read_mpu6050()
    temperature, humidity = read_dht22()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Save data to file
    with open(file_name, "a") as file:
        file.write(f"{timestamp}, {accel_x}, {accel_y}, {accel_z}, {temperature}, {humidity}\n")

    print(f"[{timestamp}] Accel: ({accel_x}, {accel_y}, {accel_z}) | Temp: {temperature}°C | Humidity: {humidity}%")

    # Blink LED to indicate data logging
    led.on()
    time.sleep(0.5)
    led.off()

    time.sleep(10)  # Wait 10 seconds before next measurement
