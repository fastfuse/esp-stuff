from machine import Pin
import time
import dht
import json
import network
import ubinascii
from umqtt.simple import MQTTClient

import BlynkLib


INTERNAL_LED = 2
DHT_DATA = 16

# Default MQTT server to connect to
MQTT_SERVER = "test.mosquitto.org"
TOPIC_TEMP_HUM = b"lwo/iot/temp_hum"

# Uniq client ID
CLIENT_ID = ubinascii.hexlify(machine.unique_id())

BLYNK_AUTH = 'd0f353a80b484ab5b9cf72b2b967db5c'


# TODO: add logging


def toggle_led(led):
    """
    Utility function to toggle LED
    """
    led.value(not led.value())


def wlan_connect():
    """
    Function to connect to WIFI network.
    """
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    with open('wlan') as wlan_creds:
        # ssid, pswd = creds.read().splitlines()
        ssid, pswd = [line.strip() for line in wlan_creds.readlines()]

    if not sta_if.isconnected():
        print('Connecting to network...')

        sta_if.active(True)
        sta_if.connect(ssid, pswd)

        while not sta_if.isconnected():
            pass

    ap_if.active(False)

    print('Connected. Network config:', sta_if.ifconfig())


def main():
    """
    Main loop
    """

    wlan_connect()

    import BlynkLib

    led = Pin(INTERNAL_LED, Pin.OUT, value=0)
    dht_sensor = dht.DHT22(Pin(DHT_DATA))


    # Initialize Blynk
    blynk = BlynkLib.Blynk(BLYNK_AUTH)

    # Register Virtual Pins
    @blynk.VIRTUAL_WRITE(1)
    def my_write_handler(value):
        print('Current V1 value: {}'.format(value))
        toggle_led(led)

    # @blynk.VIRTUAL_WRITE(2)
    # def my_write_handler(value):
    #     print('Current V1 value: {}'.format(value))
        # toggle_led(led)

    @blynk.VIRTUAL_READ(2)
    def my_read_handler():
        # this widget will show some time in seconds..
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        blynk.virtual_write(2, temp)
        blynk.virtual_write(3, hum)


    while True:
        blynk.run()

    # dht_sensor = dht.DHT22(Pin(DHT_DATA))

    # while True:
    #     # toggle_led(led)

    #     dht_sensor.measure()

    #     toggle_led(led)

    #     time.sleep(4)



if __name__ == '__main__':
    main()
