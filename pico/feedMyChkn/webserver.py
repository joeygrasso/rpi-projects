import network
import re
import socket
import sys
import time

from machine import Pin

sys.path.append('/lib')
import diagnostic
import feeder

class WebServer():
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.connect(ssid, password)
        self.addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        self.s = socket.socket()
        self.s.bind(self.addr)
        self.s.listen(1)

    def connect(self):
        max_wait = 10
        while max_wait > 0:
            if self.wlan.status() < 0 or self.wlan.status() >= 3:
                break
            max_wait -= 1
            print('waiting for connection...')
            time.sleep(1)

        if self.wlan.status() != 3:
            raise RuntimeError('network connection failed')
        else:
            print('connected')
            status = self.wlan.ifconfig()
            print('ip = ' + status[0])

    def listen_and_serve(self):          
        try:
            cl, addr = self.s.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)

            url = self.get_request_url(request)
            
            if url.find('/led/on') is not -1:
                print("led on")
                diagnostic.led_on()
                stateis = "LED is ON"
            elif url.find('/led/off') is not -1:
                print("led off")
                diagnostic.led_off()
                stateis = "LED is OFF"
            elif url.find('/led/flash') is not -1:
                print("led flash")
                p = self.extract_query_parameters(url)
                if 'duration' in p:
                    duration = int(p['duration'])
                    diagnostic.blink_status_led(duration)
                else:
                    print("led flash duration not specified")
                    diagnostic.blink_status_led(5)
                stateis = "LED is FLASH"
            elif url.find('/feeder/run') is not -1:
                print("feeder run")
                p = self.extract_query_parameters(url)
                if 'duration' in p:
                    duration = int(p['duration'])
                    feeder.run_feeder(duration)
                else:
                    print("feeder run duration not specified")
                    feeder.run_feeder(10)
                stateis = "Feeder is RUNNING for %d seconds" % (duration if 'duration' in p else 10)
            else:
                print("failed to detect endpoint")
                stateis = "NOT FOUND"

            response = html % stateis

            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()

        except OSError as e:
            cl.close()
            print('connection closed')

    def get_request_url(self, byte_array) -> str:
        """
        Extract a URL string from a byte array

        Args:
            byte_array (byte object): The byte array typically received from a
                                      socket buffer.

        Returns:
            str: The extracted URL string or "None" if extraction fails.
        """
        
        try:
            decoded_string = byte_array.decode('utf-8')
            request_line = decoded_string.split('\n')[0]
            url = request_line.split(' ')[1]
            return url
        except (UnicodeDecodeError, IndexError):
            return "None"
    
    def extract_query_parameters(self, url):
        """
        Extract query parameters from a URL string using regex.

        Args:
            url (str): The URL string.

        Returns:
            dict: A dictionary of query parameters and their values.
        """
        query_params = {}
        match = re.search(r'\?(.*)', url)
        if match:
            query_string = match.group(1)
            pairs = query_string.split('&')
            for pair in pairs:
                key, value = pair.split('=')
                query_params[key] = value
        return query_params

html = """<!DOCTYPE html>
<html>
    <head> <title>Feed My Chickens</title> </head>
    <body> <h1>Feed My Chickens</h1> <hr />
        <p>%s</p>
    </body>
</html>
"""
