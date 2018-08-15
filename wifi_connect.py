"""
WIFI connection stuff
"""

def connect():
    """
    Function to connect to WIFI network.
    """

    import network
    sta_if = network.WLAN(network.STA_IF)

    with open('wlan') as creds:
        ssid, pswd = creds.read().splitines()

    if not sta_if.isconnected():
        print('Connecting to network...')

        sta_if.active(True)
        sta_if.connect(ssid, pswd)

        while not sta_if.isconnected():
            pass

    print('Connected. Network config:', sta_if.ifconfig())
