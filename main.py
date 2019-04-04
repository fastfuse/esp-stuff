import BlynkLib
import dht
from machine import Pin

from utils import wlan_connect

INTERNAL_LED = 2
DHT_DATA = 16

BLYNK_AUTH = 'd0f353a80b484ab5b9cf72b2b967db5c'


def main():
    """
    Main loop
    """

    # connect to wifi
    wlan_connect()

    led = Pin(INTERNAL_LED, Pin.OUT)
    dht_sensor = dht.DHT22(Pin(DHT_DATA))

    # Initialize Blynk
    blynk = BlynkLib.Blynk(BLYNK_AUTH)

    # Register Virtual Pins
    @blynk.VIRTUAL_WRITE(1)
    def button_handler(value):
        # blynk.virtual_write(4, value)
        led.value(int(value[0]))

    @blynk.VIRTUAL_READ(2)
    def temp_hum_handler():
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        blynk.virtual_write(2, temp)
        blynk.virtual_write(3, hum)

    while True:
        blynk.run()


if __name__ == '__main__':
    main()
