import mfrc522
import os
import ubinascii


KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]


def read_uid():

    reader = mfrc522.MFRC522(0, 2, 4, 5, 14)

    print()
    print("Place card before reader to read UID")
    print()

    try:
        while True:
            status, _ = reader.request(reader.REQIDL)

            if status == reader.OK:

                stat, raw_uid = reader.anticoll()

                if stat == reader.OK:
                    print("Card detected...")
                    print("RAW_UID: {}".format(raw_uid))

                    uid = '{:02x}{:02x}{:02x}{:02x}'.format(*raw_uid[:4]).upper()

                    print("UID: {}".format(uid))
                    print("")

                    if reader.select_tag(raw_uid) == reader.OK:
                        if reader.auth(reader.AUTHENT1A, 8, KEY, raw_uid) == reader.OK:
                            data = os.urandom(16)
                            stat = reader.write(8, data)
                            reader.stop_crypto1()

                            if stat == reader.OK:
                                print("Data written to card: {}".format(data))
                            else:
                                print("Failed to write data to card")
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")


def read_tag():
    """
    Read tag UID and data (address 0x08)
    """
    reader = mfrc522.MFRC522(0, 2, 4, 5, 14)

    print()
    print("Place card before reader to read UID and data")
    print()

    try:
        while True:
            status, _ = reader.request(reader.REQIDL)

            if status == reader.OK:

                stat, raw_uid = reader.anticoll()

                if stat == reader.OK:
                    print("Card detected...")
                    print("RAW_UID: {}".format(raw_uid))

                    uid = '{:02x}{:02x}{:02x}{:02x}'.format(*raw_uid[:4]).upper()

                    print("UID: {}".format(uid))
                    print()

                    if reader.select_tag(raw_uid) == reader.OK:

                        if reader.auth(reader.AUTHENT1A, 8, KEY, raw_uid) == reader.OK:
                            print("Address 8 data: {}".format(reader.read(8)))
                            reader.stop_crypto1()
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")


def write_data(data):
    """
    Write data to card (address 0x08)
    """
    reader = mfrc522.MFRC522(0, 2, 4, 5, 14)

    print()
    print("Place card before reader to read UID and data")
    print()

    try:
        while True:
            status, _ = reader.request(reader.REQIDL)

            if status == reader.OK:

                stat, raw_uid = reader.anticoll()

                if stat == reader.OK:
                    print("Card detected...")
                    print("RAW_UID: {}".format(raw_uid))

                    uid = '{:02x}{:02x}{:02x}{:02x}'.format(*raw_uid[:4]).upper()

                    print("UID: {}".format(uid))
                    print()

                    if reader.select_tag(raw_uid) == reader.OK:

                        if reader.auth(reader.AUTHENT1A, 8, KEY, raw_uid) == reader.OK:
                            stat = reader.write(8, data)
                            reader.stop_crypto1()
                            if stat == reader.OK:
                                print("Data written to card")
                            else:
                                print("Failed to write data to card")
                        else:
                            print("Authentication error")
                    else:
                        print("Failed to select tag")

    except KeyboardInterrupt:
        print("Bye")
