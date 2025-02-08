import rp2  # type: ignore
import sys
import socket
import network # type: ignore
from time import sleep
from picozero import pico_led


# thread that exits when button pressed
def exit_thread():
    counter = 0
    while True:
        print(counter)
        counter += 2
        sleep(1)


print("Connecting to WiFi...")
ssid = "Tom and Alex Wifi"
password = "TomTom0312!"


def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print("Waiting for connection...")
        pico_led.on()
        sleep(0.5)
        pico_led.off()
        sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    pico_led.on()
    return ip


def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


ip = connect()
connection = open_socket(ip)
print(connection)


while True:
    try:
        client, addr = connection.accept()
        print("Got a connection from %s" % str(addr))
        request = client.recv(1024)
        print("Content = %s" % str(request))
        response = "Hello World!"
        client.send(response)
        client.close()
    except:
        pass
    finally:
        if rp2.bootsel_button() == 1:
            break
    sleep(0.1)
