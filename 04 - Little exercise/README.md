# Consolidation

In this part I propose you to try and use all we did since the beginning. 

## Simple button/LED interaction
Can you write a code so that each button put a led to a certain color (your choice) and each consecutive push on any button color the next LED 

<details>
    <summary>My solution</summary>

```python
import board
from neopixel import NeoPixel
from rainbowio import colorwheel
import time

from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Button

PIXEL_PIN = board.GP27
NB_PIXEL = 12

pin14 = DigitalInOut(board.GP14)
pin14.direction = Direction.INPUT
pin14.pull = Pull.UP
btn14 = Button(pin14)

pin17 = DigitalInOut(board.GP17)
pin17.direction = Direction.INPUT
pin17.pull = Pull.UP
btn17 = Button(pin17)

pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

BTN14_COLOR = (255,0,0)
BTN17_COLOR = (0,255,0)

tracker_led = 0
next_color = None

while True:
    btn14.update()
    btn17.update()
    if btn17.pressed:
        next_color = BTN17_COLOR
    if btn14.pressed:
        next_color = BTN14_COLOR
    if next_color is not None:
        pixels[tracker_led] = next_color
        pixels.write()
        next_color = None
        tracker_led = (tracker_led + 1) % NB_PIXEL
```

</details>

