from machine import Pin
import ubinascii
import time
import os
import json
import urequests as requests
import wifi_connect
import mfrc522
import config


KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

# Many ESP8266 boards have active-low "flash" button on GPIO0.
# button = Pin(0, Pin.IN)


class Token:
    """
    Helper class to work with bytes/hex repr of os.urandom string
    """
    def __init__(self, bytes_=16):
        self._token = os.urandom(bytes_)

    @property
    def token(self):
        """
        Token as bytes
        """
        return self._token

    @property
    def hex_token(self):
        """
        Token as hexadecimal string
        """
        return ubinascii.hexlify(self._token).decode()


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

# TODO: OOP
def read_uid(reader):
    """
    Read UID of RFID tag
    """
    status, _ = reader.request(reader.REQIDL)

    if status == reader.OK:
        status, raw_uid = reader.anticoll()

        if status == reader.OK:
            print("Card detected...")
            print("Raw UID: {}".format(raw_uid))
            # uid = format_uid(raw_uid)
            # print("UID: {}".format(uid))

            return raw_uid

    else:
        return False

# TODO: OOP
def write_data(reader, raw_uid, data):
    """
    Write data to card (address 0x08)
    """
    if reader.select_tag(raw_uid) == reader.OK:
        if reader.auth(reader.AUTHENT1A, 8, KEY, raw_uid) == reader.OK:
            status = reader.write(8, data)
            reader.stop_crypto1()

            # possible issue
            if status == reader.OK:
                print("Data written to card: {}".format(data))
            else:
                print("Failed to write data to card")
        else:
            print("Authentication error")
    else:
        print("Failed to select tag")



def main():
    """
    Main loop
    """
    # connect to wifi network
    # TODO: move to boot.py?
    # UPD: some issues w/ boot.py
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
            tag_raw_uid = read_uid(READER)

            if tag_raw_uid:
                transaction_id = Token()

                write_data(READER, tag_raw_uid, transaction_id.token)
                time.sleep(1)
                break

            # ready to accept payment (LED is on)
            LED.off()
            time.sleep_ms(200)

        # processing (LED off)
        toggle_led(LED)

        print("Tag detected. Sending request...")

        tag_uid = format_uid(tag_raw_uid)
        data = {'uid': tag_uid, 'transaction_id': transaction_id.hex_token}

        if not REGISTRATION_MODE.value():
            url = config.REGISTRATION_URL
        elif not REFILL_MODE.value():
            url = config.REFILL_URL
            data.update({"trips": config.DEFAULT_REFILL_NUMBER})
        else:
            url = config.PAYMENT_URL

        try:
            print("Request data: {}".format(data))

            r = requests.post(url,
                              data=json.dumps(data),
                              headers=config.HEADERS)

            print("Response status: {}".format(r.status_code))
            print("Response data: {}".format(r.json()))

            # It's mandatory to close response objects as soon as you finished
            # working with them. On MicroPython platforms without full-fledged
            # OS, not doing so may lead to resource leaks and malfunction.
            r.close()
        except:
            print("Failed to send request")

        # time.sleep_ms(200)
        time.sleep(3)


if __name__ == "__main__":
    main()
