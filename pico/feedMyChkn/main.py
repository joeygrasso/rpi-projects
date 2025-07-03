import sys

sys.path.append('/lib')
import webserver

def main():
    print("Starting the web server...")

    ssid = ''
    password = ''
    web_server = webserver.WebServer(ssid, password)
    web_server.connect()

    # Listen for connections
    print("Listening for connections...")
    while True:
        web_server.listen_and_serve()

if __name__ == "__main__":
    main()
