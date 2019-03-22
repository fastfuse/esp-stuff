from machine import Pin
import time
import dht
import json
import network
import ubinascii
from umqtt.simple import MQTTClient


INTERNAL_LED = 2
DHT_DATA = 16

# Default MQTT server to connect to
MQTT_SERVER = "test.mosquitto.org"
TOPIC_TEMP_HUM = b"lwo/iot/temp_hum"

# Uniq client ID
CLIENT_ID = ubinascii.hexlify(machine.unique_id())


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

    led = Pin(INTERNAL_LED, Pin.OUT, value=1)


    # TODO: subclass and add context manager
    client = MQTTClient(CLIENT_ID, MQTT_SERVER)


    dht_sensor = dht.DHT22(Pin(DHT_DATA))

    while True:
        toggle_led(led)

        dht_sensor.measure()

        data = json.dumps({"temperature": dht_sensor.temperature(),
                           "humidity": dht_sensor.humidity()})

        client.connect()
        client.publish(TOPIC_TEMP_HUM, data.encode())
        client.disconnect()

        toggle_led(led)

        time.sleep(2)



if __name__ == '__main__':
    main()
