import board, busio, time
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from time import sleep
import socketpool
import wifi
from server import Server


SERVER_NICK="Local"
SERVER_IP="0.0.0.0"
SERVER_PORT=0
SSID="AP"
PASSWD="12345678"


pool=socketpool.SocketPool(wifi.radio)
while not wifi.radio.ipv4_address:
    try:
        wifi.radio.connect(SSID,PASSWD)
    except ConnectionError as e:
        print("Connection Error:", e)
        print("Retrying in 10 seconds")
    time.sleep(10)

connSoc=pool.socket(pool.AF_INET,pool.SOCK_DGRAM)

address=pool.getaddrinfo(SERVER_IP,SERVER_PORT)[0][-1]
connSoc.connect(address)
server=Server(address,connSoc)


sda, scl = board.GP0, board.GP1
i2c = busio.I2C(scl,sda)
lcd = LCD(I2CPCF8574Interface(i2c,0x27), num_rows=4, num_cols=16)

while True:
    server.getInfo()
    result=server.dict()
    if len(f"{SERVER_NICK} {result['playingPlayerCount']}/{result['maxPlayerCount']}")>=16:
        lcd.print(f"{SERVER_NICK} {result['playingPlayerCount']}/{result['maxPlayerCount']}Map: {result['serverMap']}")
    else:
        lcd.print(f"{SERVER_NICK} {result['playingPlayerCount']}/{result['maxPlayerCount']}\nMap: {result['serverMap']}")
    sleep(60)
