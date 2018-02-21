import smbus2 as smbus
import time
import datetime
import os

REGISTER_POWER_MANAGEMENT = 0x6b
SENSOR_ADDRESS = 0x68
ACCELEROMETER_CONFIG = 0x1c

def read_2_bytes(bus, register):
    high_bits = bus.read_byte_data(SENSOR_ADDRESS, register)
    low_bits = bus.read_byte_data(SENSOR_ADDRESS, register + 1)
    value = (high_bits << 8) + low_bits
    return value

def read_2_bytes_2c(bus, register):
    value = read_2_bytes(bus, register)
    if value & 0b1000000000000000 == 0b1000000000000000:
        return -(~(value - 1) & 0b0111111111111111)
    else:
        return value

def read_acceleration(bus):
    acceleration_x_raw = read_2_bytes_2c(bus, 0x3b)
    acceleration_y_raw = read_2_bytes_2c(bus, 0x3d)
    acceleration_z_raw = read_2_bytes_2c(bus, 0x3f)

    acceleration_x = acceleration_x_raw / 16384.0
    acceleration_y = acceleration_y_raw / 16384.0
    acceleration_z = acceleration_z_raw / 16384.0
    return (acceleration_x, acceleration_y, acceleration_z)    

def current_time_mus():
    return int(round(time.time() * 1000000))

time_left = 0

# duration in ms
def new_measurement(duration):
    global time_left
    if time_left > 0:
        print("Already measuring for the next " + str(time_left) + " ms")
        return

    time_left = duration

    bus = smbus.SMBus(1)
    bus.write_byte_data(SENSOR_ADDRESS, REGISTER_POWER_MANAGEMENT, 0)
    bus.write_byte_data(SENSOR_ADDRESS, ACCELEROMETER_CONFIG, 0)

    csv = ""
    t_start = current_time_mus()
    t_last = 0
    t_should = duration * 1000
    t = 0

    while t < t_should:
        t = current_time_mus() - t_start
        time_left = (t_should - t) / 1000
        if t - t_last >= 5000:
            (a_x, a_y, a_z) = read_acceleration(bus)
            csv += str(t) + "," + str(a_x) + "," + str(a_y) + "," + str(a_z) + "\n"
            t_last += 5000

    datetimestring = datetime.datetime.utcnow().isoformat()
    if not os.path.exists("./datasets"):
        os.makedirs("./datasets")
    with open("./datasets/" + datetimestring + ".csv", "w+") as csvfile:
        csvfile.write(csv)
        csvfile.close()

    time_left = 0
