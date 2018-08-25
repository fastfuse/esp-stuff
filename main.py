from machine import Pin
import time
import json
import urequests as requests
import wifi_connect
import mfrc522
import config


# Many ESP8266 boards have active-low "flash" button on GPIO0.
# button = Pin(0, Pin.IN)


def toggle_led(led):
    """
    Utility function to toggle LED
    """
    led.value(not led.value())


def format_uid(raw_uid):
    """
    Format UID of RFID tag (list of integers -> hex)
    """
    # '{:02x}{:02x}{:02x}{:02x}'.format(*raw_uid[:4]).upper()
    return '{:02x}-{:02x}-{:02x}-{:02x}'.format(*raw_uid[:4])


def read_rfid(reader):
    """
    Read UID of RFID tag
    """
    status, _ = reader.request(reader.REQIDL)

    if status == reader.OK:
        status, raw_uid = reader.anticoll()

        if status == reader.OK:
            print("Card detected...")
            # print("Raw UID: {}".format(raw_uid))
            uid = format_uid(raw_uid)

            print("UID: {}".format(uid))

            return uid

    else:
        return False


def main():
    """
    Main loop
    """
    # connect to wifi network
    # TODO: move to boot.py? UPD: some issues w/ boot.py
    wifi_connect.connect()

    READER = mfrc522.MFRC522(0, 2, 4, 5, 14)

    LED = Pin(2, Pin.OUT)
    REGISTRATION_MODE = Pin(12, Pin.IN, Pin.PULL_UP)
    REFILL_MODE = Pin(13, Pin.IN, Pin.PULL_UP)

    print("Main loop started...")
    while True:
        # RFID tag loop
        while True:
            # wait for RFID tag
            tag_uid = read_rfid(READER)

            if tag_uid:
                break

            # ready to accept payment (LED is on)
            LED.off()
            time.sleep_ms(200)

        # processing (LED off)
        toggle_led(LED)

        print("Tag detected. Sending request...")

        data = {'uid': tag_uid}

        if not REGISTRATION_MODE.value():
            url = config.REGISTRATION_URL
        elif not REFILL_MODE.value():
            url = config.REFILL_URL
            data.update({"trips": config.DEFAULT_REFILL_NUMBER})
        else:
            url = config.PAYMENT_URL

        r = requests.post(url,
                          data=json.dumps(data),
                          headers=config.HEADERS)

        print("Response status: {}".format(r.status_code))
        print("Response data: {}".format(r.json()))

        # It's mandatory to close response objects as soon as you finished
        # working with them. On MicroPython platforms without full-fledged
        # OS, not doing so may lead to resource leaks and malfunction.
        r.close()

        # time.sleep_ms(200)
        time.sleep(3)


if __name__ == "__main__":
    main()
