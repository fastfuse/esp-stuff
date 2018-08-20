from machine import Pin
from urandom import getrandbits
import time
import json
import urequests as requests
import wifi_connect


# Many ESP8266 boards have active-low "flash" button on GPIO0.
button = Pin(0, Pin.IN)
led = Pin(2, Pin.OUT)

TOKENS = [
    "2c3a555b-01cb-4636-ab65-ad38e0aa706b",
    "5f44f87d-197f-4cf1-aa8b-fd622a8992c3",
    "1936e081-689a-45f2-bf93-a01232c5a9e5",
    "d75c5f40-26bb-41f3-8059-c88ac8b6eb31"
]

# TODO: get constants from config file
URL = "http://192.168.1.34:5000/api/v1/pay"

HEADERS = {
    'content-type': 'application/json'
}


def toggle_led(led):
    """
    Utility function to toggle LED
    """
    led.value(not led.value())


def main():
    """
    Main loop
    """
    print("Main loop started...")

    # connec to wifi network
    # TODO: move to boot.py ?
    wifi_connect.connect()

    while True:
        # button loop
        while True:
            # wait for button click
            if button.value() == 0:
                break

            # ready to accept payment (LED is on)
            led.off()

            time.sleep_ms(20)

        # processing (LED off)
        toggle_led(led)

        print("Button pressed. Sending request...")

        r = requests.post(URL,
                          data=json.dumps({'uid': TOKENS[getrandbits(2)]}),
                          headers=HEADERS)

        print("Response status: {}".format(r.status_code))
        print("Response data: {}".format(r.json()))

        if r.status_code != 200:
            print("Error")
            print(r.json())

        else:
            print("Success")
            print(r.json())

        # It's mandatory to close response objects as soon as you finished
        # working with them. On MicroPython platforms without full-fledged
        # OS, not doing so may lead to resource leaks and malfunction.
        r.close()

        # time.sleep_ms(200)
        time.sleep(3)



if __name__ == "__main__":
    main()
