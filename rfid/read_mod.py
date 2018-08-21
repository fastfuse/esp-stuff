import mfrc522


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

    except KeyboardInterrupt:
        print("Bye")
