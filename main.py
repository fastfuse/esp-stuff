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

BLYNK_AUTH = 'd0f353a80b484ab5b9cf72b2b967db5c'


def toggle_led(led):
    """
    Utility function to toggle LED
    """
    led.value(not led.value())


def wlan_connect():
    """
    Connect to WIFI network
    """
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    with open('wlan') as wlan_creds:
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
