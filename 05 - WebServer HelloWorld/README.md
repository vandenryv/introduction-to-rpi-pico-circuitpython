# WebServer

In this part of the tutorial we will connect the pi to the wifi and display an html hello world.

## Configuration

First we need a few files to be in your pi root file directory:
- these files can be found in the common folder of the repository:
  - board.py
  - config.py
  - gurgleapps_webserver.py
  - request.py
  - response.py
- these folder and file can be found in this folder:
  - www
    - index.html
  - main.py

Copy these file following these instructions: 

*In Thonny go to the top menu, in "View", check "Files" if it is not already checked. Two tabs will display on the left, the top one represents the files in your computer and the bottom one the files in your rpi. In the computer file tab navigate to this repository folder, go to the common folder, right click on "color.py" and choose "upload to /".*

You can keep these files in your pi, from now on only `config.py` and `main.py` will change.

In your raspberry pi folder tab, click on `config.py` to edit it.

In this file you can add variables that you need in the `main.py` script, but for now set up the wifi credential.

You can look at the "main.py".

As usual we import a lot of stuff.

```python
from gurgleapps_webserver import GurgleAppsWebserver
import config
import utime as time
import uasyncio as asyncio
from machine import Pin
import ujson as json
from board import Board
```

This piece of code allows us (and the server) to guess the kind of controller we use and to find its led.

```python
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

```

The `async` keyword here means the function will not return immediatly and can temporize its return... Too complicated? Yeah, ignore it for now, just know that you can't call an async function "normally". Also the `sleep()` function in a `async` function should be `asyncio.sleep()`.

*If you want to know, `sleep()` stops the execution, blocking all other executions while `asyncio.sleep()` temporizes it allowing other executions while it waits.*

The main function here do nothing because only the server will serve files, but the server will stop when the main function stops. We just make it sleep indefinetly for now.

```python
async def main():
    while True:
        await asyncio.sleep(1)
```

With this we build the web server, giving him needed parameters, like the wifi credential from the config file, the timeout on pages, the root of your html folder and your log level.

```python
server = GurgleAppsWebserver(config.WIFI_SSID, config.WIFI_PASSWORD, port=config.PORT, timeout=20, doc_root="/www", log_level=2)
```

Then we run it, giving it our main function.

```python
asyncio.run(server.start_server_with_background_task(main))
print('DONE')
```

If you run this script in your main.py file, the pi should connect to the wifi and give you its IP.

```
Board type: Raspberry Pi Pico W
GurgleApps.com Webserver
connected
ip = 192.168.XXX.XXX
point your browser to http:// 192.168.XXX.XXX
exit constructor
start_server
```

For this exemple you can go to http://192.168.XXX.XXX and check that you get an hello world.

Good job, now your raspberry pi is connected, and answers your http request.

You can now go to the WebServer Interaction Tutorial.