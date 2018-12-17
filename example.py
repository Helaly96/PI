#!/usr/bin/python
import ms5837
import time

sensor = ms5837.MS5837_30BA() 
# We must initialize the sensor before reading it
if not sensor.init():
        exit(1)

# We have to read values from sensor to update pressure and temperature
if not sensor.read():

    exit(1)

print("Pressure: %.2f atm  %.2f Torr  %.2f psi",
sensor.pressure(ms5837.UNITS_atm))

print("Temperature: %.2f C  %.2f F  %.2f K",
sensor.temperature(ms5837.UNITS_Centigrade))

freshwaterDepth = sensor.depth() # default is freshwater
sensor.setFluidDensity(ms5837.DENSITY_SALTWATER)
saltwaterDepth = sensor.depth() # No nead to read() again
sensor.setFluidDensity(1000) # kg/m^3

time.sleep(5)

# Spew readings
while True:
        if sensor.read():
                print(
                sensor.pressure(), 
                sensor.temperature())
        else:
                print("feh moshkela")
