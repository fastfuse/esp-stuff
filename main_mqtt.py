import time

import dht
import machine
import ubinascii
import json
from umqtt.simple import MQTTClient

from utils import wlan_connect, toggle_led

INTERNAL_LED = 2
DHT_DATA = 16

# Default MQTT server to connect to
MQTT_SERVER = "test.mosquitto.org"
# MQTT_SERVER = "broker.hivemq.com"
TOPIC_TEMP_HUM = b"lwo/iot/temp_hum"

# Uniq client ID
CLIENT_ID = ubinascii.hexlify(machine.unique_id())


def main(server=MQTT_SERVER):
    """
    Main loop
    """

    wlan_connect()

    # led = machine.Pin(INTERNAL_LED, machine.Pin.OUT)
    dht_sensor = dht.DHT22(machine.Pin(DHT_DATA))

    c = MQTTClient(CLIENT_ID, server)
    c.connect()

    while True:
        dht_sensor.measure()

        msg = json.dumps({"temperature": dht_sensor.temperature(),
                          "humidity": dht_sensor.humidity()}).encode()

        c.publish(TOPIC_TEMP_HUM, msg)

        time.sleep(5)

    c.disconnect()


if __name__ == "__main__":
    main()
