"""
Basic multi thread example
"""

import sys
import rp2
import socket
import network
from time import sleep
from picozero import pico_led
import asyncio

exit_flag = False


async def exit_thread(n):
    global exit_flag
    counter = n
    while True:
        if rp2.bootsel_button() == 1:
            print("Button pressed - raising exit flag")
            exit_flag = True
            break
        print(counter)
        counter += 2
        await asyncio.sleep(1)


async def handleClientConnections():
    global exit_flag
    print("Connecting to WiFi...")
    ssid = "Tom and Alex Wifi"
    password = "TomTom0312!"
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        if rp2.bootsel_button() == 1:
            sys.exit()
        print("Waiting for connection...")
        pico_led.on()
        await asyncio.sleep(0.5)
        pico_led.off()
        await asyncio.sleep(0.5)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    pico_led.on()
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    # connection.setblocking(False) # This does not work
    connection.settimeout(1)  # This works like magic
    connection.listen(5)
    print(connection)

    while True:
        try:
            client, addr = connection.accept()
            print("Got a connection from %s" % str(addr))
            request = client.recv(1024)
            print("Content = %s" % str(request))
            response = "Hello World!"
            print("Sending response...")
            client.send(response)
            print("Response sent")
            client.close()
        except:
            pass
        finally:
            if exit_flag:
                print("Exit flag raised - closing connection")
                break
        await asyncio.sleep(0.1)


async def main():
    asyncio.create_task(exit_thread(0))
    asyncio.create_task(handleClientConnections())


loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()
