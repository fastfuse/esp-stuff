"""
WIFI connection stuff
"""

def connect():
    """
    Function to connect to WIFI network.
    """

    import network
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    with open('wlan') as creds:
        # ssid, pswd = creds.read().splitlines()
        ssid, pswd = [line.strip() for line in creds.readlines()]

    if not sta_if.isconnected():
        print('Connecting to network...')

        sta_if.active(True)
        sta_if.connect(ssid, pswd)

        while not sta_if.isconnected():
            pass

    ap_if.active(False)

    print('Connected. Network config:', sta_if.ifconfig())
