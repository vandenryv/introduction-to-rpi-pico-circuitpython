# Neopixel

## HelloWorld 

In this we will see how to use WS2812 LED aka Neopixels with the rpi pico microcontroller

*Neopixel are RGB or RGBW (W being White) LED with a tiny embedded microcontroller, they are addressable so you can light up one in one color and the second in another. It works by sending all the color data to the Data input (Din) of the microcontroller. The microcontroller will take the first 3 (or 4 when RGBW) bytes of data it receive and send the remaining to the next Neopixel through its Data output pin (Do or Dout). The color are coded with 8 bits each, with a total of 24 (or 32) bits by pixel and a speed of 800kbps, if your controller has enough memory you could address more then 30 000 LED with only one pin with a refresh rate of 1 refresh per second or a 1000 led with a 30 refresh per second*

What will we need :
- Tell the interpreter we need one pin as Output
- Prepare some memory to manage the Pixels
- Wait a bit between change

With thoose needs the impors will be :

```python
import board
from time import sleep
from neopixel import NeoPixel
```

Now we need to declare how much pixel we have and on wich pin, we have 12 on the GP27 pin. (GP meaning General Purpose)

```python
pixels = NeoPixel(board.GP27, 12)
```

We set the brightness to 10% because these neopixel can be very shiny

```
pixels.brightness = 0.1
```

Now we can turn on the first LED in red, the second in green, and the third in yellow

```python
pixels[0] = (255,0,0)   # it is RGB, the first represent the red, then blue, then green
pixels[1] = (0,255,0)   # The value are from 0 to 255, and always integers
pixels[2] = (127,127,0) # the LED can get really bright really fast so I tune off the values a bit
```

With the previous instructions we set the color data in our microcontroller's memory but now we need to send the datas to the Pixels

```python
pixels.write()
```

Nice but it is always better to extract constant from the running code (you will thank me later)

```python
import board
import neopixel
from time import sleep

PIXEL_PIN = board.GP27
NB_PIXEL = 12

pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels[0] = (255,0,0)
pixels[1] = (0,255,0)
pixels[2] = (127,127,0)
pixels.write()
```

Write that down in your code.py, STOP and START, and your three first LED should light up.

## Animation
### Basics 
We can now use this object and the sleep function to create animation

```python
import board
from neopixel import NeoPixel
from time import sleep

PIXEL_PIN = board.GP27
NB_PIXEL = 12

pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

while True:
    pixels[0] = (255,0,0)
    pixels[1] = (255,0,0)
    pixels[2] = (255,0,0)
    pixels[3] = (255,0,0)
    pixels[4] = (255,0,0)
    pixels[5] = (255,0,0)
    # ...
    pixels.write()
    sleep(0.5)
    pixels[0] = (0,255,0)
    pixels[1] = (0,255,0)
    pixels[2] = (0,255,0)
    pixels[3] = (0,255,0)
    pixels[4] = (0,255,0)
    pixels[5] = (0,255,0)
    # ...
    pixels.write()
    sleep(0.5)
    pixels[0] = (0,0,255)
    pixels[1] = (0,0,255)
    pixels[2] = (0,0,255)
    pixels[3] = (0,0,255)
    pixels[4] = (0,0,255)
    pixels[5] = (0,0,255)
    # ...
    pixels.write()
    sleep(0.5)
```

### Iterate over LED indexes

Well using numbers directly can be quite cumbersome, let's use a loop. We will use a `for <var> in <list of objects>:` loop with the function `range(x,y)`

- `for <var> in <list of objects>:` will iterate the block under it with `<var>` taking one by one the value in `<list of objects>`
- `range(x,y)` will create a list\* of all the numbers between `x` included and `y` excluded

```python
import board
from neopixel import NeoPixel
from time import sleep

PIXEL_PIN = board.GP27
NB_PIXEL = 12
PERIOD = 0.5
pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

while True:
    for i in range(0,NB_PIXEL):
        pixels[i] = (255,0,0)
    pixels.write()
    sleep(PERIOD)
    for i in range(0,NB_PIXEL):
        pixels[i] = (0,255,0)
    pixels.write()
    sleep(PERIOD)
    for i in range(0,NB_PIXEL):
        pixels[i] = (0,0,255)
    pixels.write()
    sleep(PERIOD)
```

Ways better, don't you think?
But they are all the same color, let try to light them one by one.

For that we will need to track the lit LED and turn it off when we turn on the next and use a modulo to never go over the 12th LED (number 11).

*The modulo is needed because if we try to set a color to an index that is out of bound (for us over 11) the code will throw an OutOfBound Error and crash the program*

```python
import board
from neopixel import NeoPixel
from time import sleep

PIXEL_PIN = board.GP27
NB_PIXEL = 12
PERIOD = 0.5
pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1
tracker = 0

while True:
    # Turn off the previous LED
    pixels[tracker] = (0,0,0)
    # The tracker goes 0 1 2 3 4 5 6 7 8 9 10 11 0 1 2 3 4 5 6 7 ...
    tracker = (tracker + 1) % 12 
    # Turn on the next LED
    pixels[tracker] = (0,0,255)
    pixels.write()
    sleep(PERIOD)
```

With this code a blue dot should go accross your led indefenitly.

### Iterate over colors

You can also prepare some colors in variables to use them later

```python
import board
from neopixel import NeoPixel
from time import sleep

PIXEL_PIN = board.GP27
NB_PIXEL = 12
PERIOD = 0.5
pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (127,127,0)
CYAN = (0,127,127)
MAGENTA = (127,0,127)
OFF = (0,0,0)

tracker = 0
while True:
    # Turn off the previous LED
    pixels[tracker] = OFF
    tracker = (tracker + 1) % 12 
    # Turn on the next LED
    pixels[tracker] = BLUE
    pixels.write()
    sleep(PERIOD)
```

If we put our colors in an list, we can use a variable the same way we use `tracker` to get a new color each time 

```python
import board
from neopixel import NeoPixel
from time import sleep

PIXEL_PIN = board.GP27
NB_PIXEL = 12
PERIOD = 0.5
pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (127,127,0)
CYAN = (0,127,127)
MAGENTA = (127,0,127)
OFF = (0,0,0)

COLORS = [RED,GREEN,BLUE,YELLOW,CYAN,MAGENTA]

color_tracker = 0
led_tracker = 0
while True:
    pixels[led_tracker] = OFF
    led_tracker = (led_tracker + 1) % 12 
    # len is a function that return the lenght of the list you give it
    color_tracker = (color_tracker + 1) % len(COLORS)
    # We get the color at the color_tracker index
    pixels[led_tracker] = COLORS[color_tracker]
    pixels.write()
    sleep(PERIOD)
```

Now that you have the basics to do animations you can try yourself to do more crazy things

### Rainbows

Would it not be nice to be able to have very smooth colors. Well, we can use the chromatic disk, but for that we need ... MATHS !!!

Don't worry the maths are already done (a common thing in python) in rainbowio

As usual, we tell the interpreter we need something :

```python
from rainbowio import colorwheel
```
*The chromatic disk represent value with an angle, a lengh and an intensity, also know as hue, saturation and value -> HSV*
With  colorwheel the angle is between 0 and 255 and can be a decimal value

```python
import board
from neopixel import NeoPixel
from time import sleep
from rainbowio import colorwheel

PIXEL_PIN = board.GP27
NB_PIXEL = 12
PERIOD = 0.5
pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

while True:
    for angle in range(0,255):
        for led_tracker in range(0,NB_PIXEL):
            # colorwheel return a integer usable in NeoPixel
            pixels[led_tracker] = colorwheel(angle)
        pixels.write()
        sleep(PERIOD)
```

Now your LED should smoothly change color over time. If we want it to go faster we can reduce the PERIOD value or decrease the number of discreet angles in the first `for` loop by giving a `step` value to range 


```python
import board
from neopixel import NeoPixel
from time import sleep
from rainbowio import colorwheel

PIXEL_PIN = board.GP27
NB_PIXEL = 12
PERIOD = 0.01
pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

while True:
    for angle in range(0,255,5):
        for led_tracker in range(0,NB_PIXEL):
            # colorwheel return a integer usable in NeoPixel
            pixels[led_tracker] = colorwheel(angle)
        pixels.write()
        sleep(PERIOD)
```

With a little bit of code and maths we can create an angle offset between all LEDs, creating an ilusion of a moving rainbow.

```python
import board
from neopixel import NeoPixel
from time import sleep
from rainbowio import colorwheel

PIXEL_PIN = board.GP27
NB_PIXEL = 12
PERIOD = 0.01
pixels = NeoPixel(PIXEL_PIN, NB_PIXEL)
pixels.brightness = 0.1

# We prepare the angle
ANGLE_BETWEEN_LED =  255 / NB_PIXEL

while True:
    for angle in range(0,255,5):
        for led_tracker in range(0,NB_PIXEL):
            # We add as much angle as the offset
            pixels[led_tracker] = colorwheel(angle + ANGLE_BETWEEN_LED * led_tracker)
        pixels.write()
        sleep(PERIOD)
```
Now you should have a rainbow going across your LEDs

You now have a few of tool to build animation with the led matrix

\* Technically it is not a list, it is a sequence, the number are not kept in memory but generated on the go each time you need them.
