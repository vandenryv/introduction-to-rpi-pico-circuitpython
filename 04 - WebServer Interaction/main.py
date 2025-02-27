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

led_status = False

async def main():
    while True:
        if led_status :
            led.on()
        else :
            led.off()
        await asyncio.sleep(0.3)

async def send_state(request, response):
    global led_status
    response_string = json.dumps({"lit": led_status})
    await response.send_json(response_string, 200)

async def turn_off_and_send_state(request, response):
    global led_status
    led_status = False
    response_string = json.dumps({"lit": led_status})
    await response.send_json(response_string, 200)

async def turn_on_and_send_state(request, response):
    global led_status
    led_status = True
    response_string = json.dumps({"lit": led_status})
    await response.send_json(response_string, 200)

async def switch_and_send_state(request, response):
    global led_status
    led_status = not led_status
    response_string = json.dumps({"lit": led_status})
    await response.send_json(response_string, 200)

server = GurgleAppsWebserver(config.WIFI_SSID, config.WIFI_PASSWORD, port=config.PORT, timeout=20, doc_root="/www", log_level=2)

server.add_function_route("/state", send_state)
server.add_function_route("/switch", switch_and_send_state)
server.add_function_route("/off", turn_off_and_send_state)
server.add_function_route("/on", turn_on_and_send_state)

asyncio.run(server.start_server_with_background_task(main))
print('DONE')
