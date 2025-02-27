
# Raspberry pi pico Hello World

## Step 1 - Flash the Raspberry pi pico with Circuitpython firmware

The rpi pico is designed to be easily flashable with different type of firmware, even your own. Here we will be using the last version of circuitPython.

- First download the latest version of the circuitPython firmware for raspberry pi pico W  : [HERE](https://circuitpython.org/board/raspberry_pi_pico_w/) (the W part is important here otherwise you will not be able to use wifi) You should get a **.uf2** file.
- Prepare your raspberry pi pico and your microUsb cable by pluging **ONLY** the USB-A(The big rectangular part) part of your cable in your computer.
- Instruction : While pushing on the rpi pico 'BOOTSEL' button insert the other end of the cable in it.

*The Pico is flashable with the 'BOOTSEL' button. If the Pico is powered on while this button is pushed the Pico will simulate a USB drive, your computer will see it as such allowing you to simply drag-and-drop (or just copy-paste) the firmware into it.* Be aware that this operation will erase everything in the pi memory. 
- Your computer should react and show you a new drive containing two files, just ignore them and copy your .uf2 file in it. It should disconnect automatically.

Well done you just successfully flash a rpi pico with a circuitPython firmware.

## Step 2 - Install and configure Thonny for circuitPyhton

Thonny is a simple python IDE that integrate microPython (circuitPyhton is written in microPython) and microcontroller interface.

- Download the last version of Thonny for your os. Which you can find [HERE](https://thonny.org/).
- Install it, instructions vary depending on your OS.
- Launch it, go to Tools -> Options.
- In the Interpreter tab under "Which kind of interpreter ..." choose "CircuitPython (generic)".
- Click OK.

That's it. Thonny is ready to read and write your code to your rpi pico.

## Step 3 - Hello World

A necessary step to check that your installation works is to make the rpi pico say Hello World : We will do it 2 ways, the Dev way and the Maker way.

### The Dev way :
We will simply make the rpi pico execute a python command to print "Hello World" to its serial output. 

*A Serial connection is a simple text based connection between machine, simple and reliable it is widely use in industries. The serial output of the rpi is connected to the serial input of the virtual\* serial interface of your computer so we will see it*.

In your brand new configured Thonny click on the red STOP button, the STOP button stops the current operation and restart the connection. You should now have a Shell tab on the bottom side of Thonny in it write (or copy) after the `>>>`

```python
print('Hello World') 
```

and then press Enter, the Raspberry should answer with "Hello World".

Good job, the Rpi just obey your command.

### The Maker way

A microcontroller is made to interact with the world so one of the best way to make it "Hello World"s is to make it do something elsewhere than on our screen. We will make it blink a LED. How convinient there is a small LED on the rpi.

To make a LED blink we need a few more step :
- Declare the pin where the led is connected as binary output <- Because we will send highs and lows to it

*CircuitPython give us a neat way to find what is available on the board. We will use the embeded board library to address the pi's led*

- Send the led a 1 to turn it on.
- Wait a bit.
- Send the led a 0 to turn it off.
- Wait a bit.
- Repeat the last 4 commands.

Now to code the blinking you can use the code.py file in the tabs in front of you :
- First we need to import a few things from the circuitPython firmware. To interact with pins we need the `DigitalInOut` object, you will find it in the `digitalio` package. And to wait a bit between the different states we will need the `sleep()` function from the `time` package. And to know where things are plugged on the micro controller we will use the `board` library.

```python
import board
import digitalio
from time import sleep
``` 

- Then we declare than we want control of the LED *in a DigitalInOut* and we want it as an Output.

```python
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
```

- Now that we have our led object that control the led on the pi we can turn it on.

```python
    led.value = True
```
Now you should have something like this.

```python

import board
import digitalio
from time import sleep

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

led.value = True
```

With that in your editor click on the green Play button, it will send the code to your pi and command it to run the code. The LED should light up.

__"But the LED doesn't blink, it just stays on"__ you might say. Yes now we can add a loop with the `while <condition>:` keyword with `True` as condition, effectively creating a infinite loop.

*For the non-initiated, python creates blocks with lines that follow each other and have the same indentation.*

In the loop we turn the LED on, wait 1 second, turn it off, and wait 1 more second.

```python
import board
import digitalio
from time import sleep

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    sleep(0.5)
    led.value = False
    sleep(0.5)
```

*If you forgot the second `sleep(0.5)` you might think that the LED never turns off, but it does, the next instruction is to turn it on and it is so fast that you will never have the time to see it turn off.*

Now if you press Play, your LED should turn on and off each second. If you want it to go faster you can call sleep with smaller value or import and use sleep_ms for millisecond or sleep_us for micro second.

Good job, the Rpi now blink its LED.

### They grow so fast.

Last step of the "Hello World", we will make the rpi do the blinking without the computer sending it the script. 

The circuitPython firmware allows you to save file to rpi, if you save a script with the name "code.py" it will automatically start it when powered on.

From the screen with your script in the untitled file tab:
- Press Stop to stop the process and reconnect the pi.
- Press the Save button.

Your script is now saved as code.py at the root of the filesystem of the pi. You can unplug it from your computer and plug it ANYWHERE (where there is 5v) and the script will run and the LED will start blinking.

**HELLO WORLD of electronics and microcontrollers.**


\* Yeah!! it is virtual, the rpi has full control of the way it speaks to your computer, remember just a bit ago it was seen as a USB drive ;) It can change itself to a USBDrive, a serial interface, a keyboard, a mouse, a gamepad, a camera, and just anything you want as long as you have the code for it.
