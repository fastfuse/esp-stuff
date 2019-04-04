"""
Utility functions
"""

import network


def wlan_connect():
    """
    Connect to WIFI network
    """
    sta_if = network.WLAN(network.STA_IF)
    ap_if = network.WLAN(network.AP_IF)

    with open('wlan') as wlan_creds:
        ssid, pswd = [line.strip() for line in wlan_creds.readlines()]

    if not sta_if.isconnected():
        print('Connecting to network...')

        sta_if.active(True)
        sta_if.connect(ssid, pswd)

        while not sta_if.isconnected():
            pass

    ap_if.active(False)

    print('Connected. Network config:', sta_if.ifconfig())


def toggle_led(led):
    """
    Utility function to toggle LED
    """
    led.value(not led.value())
