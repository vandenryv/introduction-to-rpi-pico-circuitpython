# Building interaction

For this part we will be building from the `main.py` from the previous module.

First copy the folder `www` from this folder on the pi (replace `index.html` if needed).

The files can take a while to copy, let's think about our next step:
We need to make the server responde to remote call, and perform action accordingly.

We will use the `main.py` in this folder.

We added lines at 4 places: the led status, the functions, the binding of the functions and the update on the main.

- The led status

```python
led_status = False
```

It is simply a boolean value that track the state of the led

- The functions

```python
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
```

The functions are async, but again we can ignore it for now. They update, prepare and return the state of the led.

They all take `request` and `response`, `request` containing informations send by the requester and `response` handling what you respond to the requester.

```python
global led_status
```
This line declare to the interpreter that the `led_status` we will be talking about here is the one from the global context (any line without indentation). We need to declare it because the function will not be use in the global context and won't find `led_status`, so we basically tell the interpreter "When I talk about `led_status` I talk about the global one" 

```python
response_string = json.dumps({"lit": led_status})
```
Here we prepare our response in json format, `json.dumps()` will fetch and format our data with json's syntax saving it in a string in `response_string`. It will look something like this :
```json
{"lit":true}
```
or 
```json
{"lit":false}
```

```python
await response.send_json(response_string, 200)
```

Here we use `response` to handle the response, `send_json` to specify to the requester that it will receive json, we then send the data and response code in parameters.

In some of those functions we update `led_status` value:

```python
led_status = False
```
We set `led_status` to false.
```python
led_status = True
```
We set `led_status` to true.
```python
led_status = not led_status
```
We switch `led_status` to what it is not.

- The binding of the functions

After we declared the server we can bind function to it with their path.

*Http servers (or web server) handle queries based on the path and the method they are call with, for now Gurgle only manage GET request, so everything here is a GET*

```python
server.add_function_route("/state", send_state)
server.add_function_route("/switch", switch_and_send_state)
server.add_function_route("/off", turn_off_and_send_state)
server.add_function_route("/on", turn_on_and_send_state)
```

Each line bind a path to a function on the server. When we will be calling the `/switch` path with a GET call the function `switch_and_send_state` will be called.

- The `main` function

```python
async def main():
    while True:
        if led_status :
            led.on()
        else :
            led.off()
        await asyncio.sleep(0.3)
```

The main function was updated to reflect the value in `led_status` to the led on the board. We still need to use `asyncio.sleep()` to let the server handle request.

Copy the code to the `main.py` (don't forget to update the `www` folder !!) and run it. 

The web page was updated to have buttons, each button call a function (there is no button for state because it is called when the page load).

## Do it yourself

Try to implement the turning on and off of the Neopixel from the Browser.
