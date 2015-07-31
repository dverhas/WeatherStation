import requests
import stream
import os
import RPi.GPIO as GPIO
import time
import datetime
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import OpenWeather


hum_sensor_type = Adafruit_DHT.AM2302
hum_sensor_pin = 17

bmp180 = BMP085.BMP085()

GPIO.setmode(GPIO.BCM)
DEBUG = 1

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


def get_temp():
  f = open("/sys/bus/w1/devices/28-000006dd4064/w1_slave",'r')
  s = f.readlines()
  f.close()
  if not s[0].strip().endswith("YES"):
    return None
  else:
    t = float(s[1].split("=")[-1].strip())/1000;
    return t

zip_code = 44236
lat = 41.21
lon = -81.42

while True:
        light_channel= 0
        moist_channel = 1
        light = readadc(light_channel, SPICLK, SPIMOSI, SPIMISO, SPICS)
        moist = readadc(moist_channel, SPICLK, SPIMOSI, SPIMISO, SPICS)
        tempc = get_temp()
        http_code = stream.post('dverhas', lat, lon, tempc, light, zip_code, False)
        humidity, temp2 = Adafruit_DHT.read_retry(hum_sensor_type, hum_sensor_pin)
        print "http:",http_code
        print "light:",light
        print "tempc:",tempc
        print 'Temp = {0:0.2f} *C'.format(bmp180.read_temperature())
        print 'Pressure = {0:0.2f} Pa'.format(bmp180.read_pressure())
        print 'Pressure = {0:0.2f} atm'.format(101325/bmp180.read_pressure())
        print 'Altitude = {0:0.2f} m'.format(bmp180.read_altitude())
        print 'Sealevel Pressure = {0:0.2f} Pa'.format(bmp180.read_sealevel_pressure())
        print 'Humidity = {0:0.1f}%'.format(humidity)
        now = datetime.datetime.now()
        print now.strftime("%Y-%m-%d %H:%M")
        OpenWeather.post(tempc,bmp180.read_pressure(), humidity, bmp180.read_altitude())
        time.sleep(60*5)
