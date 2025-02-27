# Webserver, the IoT part

In this part we will put in place a tiny and fragile webserver, it is mainly to do a showcase of what is possible more than how to do it.
We will be using `adafruit_httpserver` again by adafruit.
This package will take care of serving and formating REST request as well as serving a tiny front end.

First, what weneed to import :
```python
# toconnect to the wifi
import wifi
from wifipsk import WIFI_SSID,WIFI_PASSWORD
# This is managing sockets, we don't need to look at it too much for today, just know that we need it
import socketpool
# The actual tiny server
from adafruit_httpserver import Server, Request, Response
# json because computer likes to talk like that
import json
# we wille be retrieving the cpu temperature to display it on our tiny front end
import microcontroller
# You already know these
import board
from neopixel import NeoPixel
```

We will be using the pixels so we initialise them 

```python
PIXEL_PIN = board.GP27
NB_PIXEL = 12

pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.50
```

Now we connect to the wifi, for that we will need to update the `WIFI_SSID` and `WIFI_PASSWORD` in the wifipsk in the lib folder

```python
WIFI_SSID = "Wifi name"
WIFI_PASSWORD = "Wifi password"
```

then we can add to code.py the code that connect to the wifi

```python 
print(f"Connecting to {WIFI_SSID}...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected to {WIFI_SSID}")
```

Now we tell the server that it will need to listen to the call from the wifi

```python
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)
```

Finally we tell the server to run forever

```python
server.serve_forever(str(wifi.radio.ipv4_address))
```

At this stage we should have that

```python
import socketpool
import wifi
from wifipsk import WIFI_SSID,WIFI_PASSWORD
from adafruit_httpserver import Server, Request, Response
import json
import microcontroller

import board
from neopixel import NeoPixel

PIXEL_PIN = board.GP27
NB_PIXEL = 12

pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.50

print(f"Connecting to {WIFI_SSID}...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected to {WIFI_SSID}")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

server.serve_forever(str(wifi.radio.ipv4_address))
```

If we run the code the server will start and listen to our requests
It wille also give us a link to access it, something like
```
Started development server on http://192.168.1.102:5000
```
If we click ont the link we see that we get an error, telling us that we don't have a index.html page in our static folder. Let's create it.
We shoudl have a static folder on this page, you can take the index.html from there and copy-paste it in a new folder named static on the fake flash drive the rpi makes available.

If we rerun the code and click on the link we should have a cute little page. That tries to display some state of our rpi.

And on the rpi we should be seeing calls, a lot of call responding with 404 errors. It is because the page is calling endpoint that doesn't exist yet on the pi

We need 3 of them a get_status, get_colors and post_colors. Get_status will retrieve and send the actual tempeature of the rpi, get_color will respond the current colors of the pixels and post_colors will set the color for 1 led.

For the `get_status` we will listen on the status endpoint and respond with the cpu temperature we get from `microcontroller.cpu.temperature`. We encapsulate it in a json and push it to the caller

```python 
@server.route("/status")
def status(request: Request):
    body = "{\"temperature\":"+str(microcontroller.cpu.temperature)+"}"
    return Response(request, body=body ,content_type="application/json")

```
Note that this code shuld be added before the `serve_forever` line, because the process of the rpi will never get out of `serve_forever` thus never running the code placed after and your route will never be declared.

We should have something like this 

```python
import socketpool
import wifi
from wifipsk import WIFI_SSID,WIFI_PASSWORD
from adafruit_httpserver import Server, Request, Response
import json
import microcontroller

import board
from neopixel import NeoPixel

PIXEL_PIN = board.GP27
NB_PIXEL = 12

pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.50

print(f"Connecting to {WIFI_SSID}...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected to {WIFI_SSID}")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/status")
def status(request: Request):
    body = "{\"temperature\":"+str(microcontroller.cpu.temperature)+"}"
    return Response(request, body=body ,content_type="application/json")

server.serve_forever(str(wifi.radio.ipv4_address))
```
 When we run this the `/status` call should give you 200 instead of 404 and the webpage should now display a temperature. It means that you just made your first very own connected temperature sensor, sadly it not the temperature of the room but the cpu's temperature but this is how you begin.

Nowwe can had two more routes, one to fetch the LED colors and one to push an LED color.


```python
@server.route("/colors", "GET")
def get_color(request: Request):
    global pixels,NB_PIXEL,glo_color,DEFAULT_COLOR
    leds = []
    for led in pixels:
        (r,g,b) = led
        color =  {
                "red":r,
                "green":g,
                "blue":b
                }
        leds.append(color)
        
    body=json.dumps(leds)
    return Response(request, body=body ,content_type="application/json")
```
We tell the route to listen to `GET` on `/colors`, so we gather the information from the pixel serialize them in json and send it to the caller.

```python
@server.route("/colors", "GET")
def get_color(request: Request):
    global pixels,NB_PIXEL,glo_color,DEFAULT_COLOR
    leds = []
    for led in pixels:
        (r,g,b) = led
        color =  {
                "red":r,
                "green":g,
                "blue":b
                }
        leds.append(color)
        
    body=json.dumps(leds)
    return Response(request, body=body ,content_type="application/json")
```

Now we declare a second route that listen to `POST` with a id in the path, we parse, we sanitize and we call the pixels to update them

```python
@server.route("/colors/<led_id>", "POST")
def post_one_color(request: Request,led_id ):
    global pixels,NB_PIXEL
    
    parsed = json.loads(request.body.decode("utf-8"))
    color = (int(parsed["red"]),int(parsed["green"]),int(parsed["blue"]))
    sanitized_index = int(led_id) % NB_PIXEL
    
    pixels[sanitized_index] = color
    pixels.write()
    print(pixels)
    return Response(request)

```

Now witheverything we added we should have something like this.

```python
import socketpool
import wifi
from wifipsk import WIFI_SSID,WIFI_PASSWORD
from adafruit_httpserver import Server, Request, Response
import json
import microcontroller

import board
from neopixel import NeoPixel

PIXEL_PIN = board.GP27
NB_PIXEL = 12

pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.50

print(f"Connecting to {WIFI_SSID}...")
wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
print(f"Connected to {WIFI_SSID}")

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static", debug=True)

@server.route("/status")
def status(request: Request):
    body = "{\"temperature\":"+str(microcontroller.cpu.temperature)+"}"
    return Response(request, body=body ,content_type="application/json")

@server.route("/colors", "GET")
def get_color(request: Request):
    global pixels,NB_PIXEL,glo_color,DEFAULT_COLOR
    leds = []
    for led in pixels:
        (r,g,b) = led
        color =  {
                "red":r,
                "green":g,
                "blue":b
                }
        leds.append(color)
        
    body=json.dumps(leds)
    return Response(request, body=body ,content_type="application/json")

@server.route("/colors/<led_id>", "POST")
def post_one_color(request: Request,led_id ):
    global pixels,NB_PIXEL
    
    parsed = json.loads(request.body.decode("utf-8"))
    color = (int(parsed["red"]),int(parsed["green"]),int(parsed["blue"]))
    sanitized_index = int(led_id) % NB_PIXEL
    
    pixels[sanitized_index] = color
    pixels.write()
    print(pixels)
    return Response(request)

server.serve_forever(str(wifi.radio.ipv4_address))
```

If you run this code,the webpage should display the temperature, and the rpi react to your color choices.

Congratulation you made your first IoT device, you can even connect it tosmart hubs like HomeAssistant to display color during certain event orwhen some conditions are met.

Next challenge for the bravest, make it so the rpi react to the button and make a call to some online services.