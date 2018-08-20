from machine import Pin
import time
import urequests as requests
import wifi_connect


# Many ESP8266 boards have active-low "flash" button on GPIO0.
button = Pin(0, Pin.IN)
URL = "https://jsonplaceholder.typicode.com/users/1"


def main():
    """
    Main loop
    """
    print("Main loop started...")

    wifi_connect.connect()

    while True:
        while True:
            if button.value() == 0:
                break
            time.sleep_ms(20)

        print("Button pressed. Sending request...")

        r = requests.get(URL)

        print("Response status: {}".format(r.status_code))
        print("Response data: {}".format(r.json()))

        # It's mandatory to close response objects as soon as you finished
        # working with them. On MicroPython platforms without full-fledged
        # OS, not doing so may lead to resource leaks and malfunction.
        r.close()

        time.sleep_ms(200)



if __name__ == "__main__":
    main()
