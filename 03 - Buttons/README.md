# Buttons
## Connect to buttons

In this we will see how tointeract with buttons in a synchronous way.

What do we need :
- a button : there is two installed on GP14 and GP17
- a pull-up : Integrated in the rpi
- something to do : What about lightning up the neopixel

In electronics for buttons to work we need a pull-up or a pull-down resistor, that will keep the input pin at one value when the button is not pushed, but let the button pull the pin to the other value when puhed. A pull-up keep the pin high waiting for the button to bring it down and a pull-down keeps the pin low waiting for the button to pull it up.

Fortunatly for us, the rp2040 on the rpi hs integrated pull-up resistor on demand, we just need to ask it to activate them :

First we import what we need 

```python
import board
# DigitalInOut to declare a High or Low pin
# Direction to declare if we want a Input or Output
# Pull to declare we want a Pull-up resistor
from digitalio import DigitalInOut, Direction, Pull
```

then we declare our buttons 

```
pin14 = DigitalInOut(board.GP14)
pin14.direction = Direction.INPUT
pin14.pull = Pull.UP

pin17 = DigitalInOut(board.GP17)
pin17.direction = Direction.INPUT
pin17.pull = Pull.UP
```

to read there value we need to use the `value` and check if it is True or False, remember we are using a pull-up, it means that the value will be High (or True) when the button is NOT pressed, and Low (or False) when pressed

```python
while True:
    if pin17.value == False:
        print("pin17 is pushed")
    if pin14.value == False:
        print("pin14 is pushed")
```

that result with this code 

```python
import board
# DigitalInOut to declare a High or Low pin
# Direction to declare if we want a Input or Output
# Pull to declare we want a Pull-up resistor
from digitalio import DigitalInOut, Direction, Pull

pin14 = DigitalInOut(board.GP14)
pin14.direction = Direction.INPUT
pin14.pull = Pull.UP

pin17 = DigitalInOut(board.GP17)
pin17.direction = Direction.INPUT
pin17.pull = Pull.UP

while True:
    if pin17.value == False:
        print("pin17 is pushed")
    if pin14.value == False:
        print("pin14 is pushed")
```

If you run it and push the button you might see a problem...
The print statement are called multiple times when you only push once. It is due to 2 things:
- The code goes fast enough that it can read the button's value multiple times while you press it 
- The buttons bounce, the blade that creates contact between the two cables act like a spring and when you push it there is a chance that in a very fast time lapse, touch, separate and touch again the ends of the cable. This create multiple Highs and Lows in the pin.

To help with both issues we can use debouncing, it can be done with a resitor and a capacitor fine tuned combo... or lazily with a bit of code. AND as we are using python it is already written.

It was written by the folks over at adafruit, let import their library

```python
from adafruit_debouncer import Debouncer
```

Now instead of directly using the pin valuewe will use the debouncer `fell` value, we use `fell` because the deboucer will tell us if the pin went from High to Low in the past. And for the debouncer to know if the button signal fell we need to allow it to `update()` very regularly by calling it at the beginning of our loop

```python
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Debouncer

pin14 = DigitalInOut(board.GP14)
pin14.direction = Direction.INPUT
pin14.pull = Pull.UP
btn14 = Debouncer(pin14)

pin17 = DigitalInOut(board.GP17)
pin17.direction = Direction.INPUT
pin17.pull = Pull.UP
btn17 = Debouncer(pin17)

while True:
    btn14.update()
    btn17.update()
    if btn17.fell:
        print("pin17 is pushed")
    if btn14.fell:
        print("pin14 is pushed")

```

But the debouncer is not the only thing this library has to offer, it also has the Button object, which will allow us to easily use simple or multiple short presses:

```python
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_debouncer import Button

pin14 = DigitalInOut(board.GP14)
pin14.direction = Direction.INPUT
pin14.pull = Pull.UP
btn14 = Button(pin14)

pin17 = DigitalInOut(board.GP17)
pin17.direction = Direction.INPUT
pin17.pull = Pull.UP
btn17 = Button(pin17)

while True:
    btn14.update()
    btn17.update()
    if btn17.pressed:
        print("pin17 is pressed")
    if btn17.long_press:
        print("pin17 is long_press")
    if btn17.short_count == 3:
        print("pin17 is pressed 3 times rapidly")
    if btn14.pressed:
        print("pin14 is pressed")
    if btn14.long_press:
        print("pin14 is long_press")
    if btn14.short_count == 3:
        print("btn14 is pressed 3 times rapidly")

```