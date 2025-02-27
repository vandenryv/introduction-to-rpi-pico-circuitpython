from gurgleapps_webserver import GurgleAppsWebserver
import config
import utime as time
import uasyncio as asyncio
from machine import Pin
import ujson as json
from board import Board

BOARD_TYPE = Board().type
print("Board type: " + BOARD_TYPE)

if BOARD_TYPE == Board.BoardType.PICO_W:
    led = Pin("LED", Pin.OUT)
elif BOARD_TYPE == Board.BoardType.PICO:
    led = Pin(25, Pin.OUT)
elif BOARD_TYPE == Board.BoardType.ESP8266:
    led = Pin(2, Pin.OUT)
else:
    led = Pin(2, Pin.OUT)

async def main():
    while True:
        await asyncio.sleep(1)
            
server = GurgleAppsWebserver(config.WIFI_SSID, config.WIFI_PASSWORD, port=config.PORT, timeout=20, doc_root="/www", log_level=2)

asyncio.run(server.start_server_with_background_task(main))
print('DONE')
