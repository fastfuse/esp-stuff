from machine import Pin
import time
import random
import urequests as requests
import wifi_connect


# Many ESP8266 boards have active-low "flash" button on GPIO0.
button = Pin(0, Pin.IN)
led = Pin(1, Pin.OUT)

TOKENS = []
# URL = "https://jsonplaceholder.typicode.com/users/1"
URL = "http://"


def main():
    """
    Main loop
    """
    print("Main loop started...")

    # connec to wifi network
    wifi_connect.connect()

    while True:
        # button loop
        while True:
            # wait for button click
            if button.value() == 0:
                break

            led.on()
            time.sleep_ms(20)

        print("Button pressed. Sending request...")

        # r = requests.get(URL)
        r = requests.post(URL, data={'uid': random.choice(TOKENS)})

        print("Response status: {}".format(r.status_code))
        # print("Response data: {}".format(r.json()))

        if r.status_code != 200:
            print("Error")
            print(r.json())

        else:
            print("Success")
            print(r.json())

            led.off()

        # It's mandatory to close response objects as soon as you finished
        # working with them. On MicroPython platforms without full-fledged
        # OS, not doing so may lead to resource leaks and malfunction.
        r.close()

        time.sleep_ms(200)



if __name__ == "__main__":
    main()
