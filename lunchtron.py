# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from time import sleep
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306


# Raspberry Pi pin configuration:
RST = None  # on the PiOLED this pin isnt used

# 128x64 display with hardware I2C:
DISP = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Note you can change the I2C address by passing an i2c_address parameter like:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

# Alternatively you can specify an explicit I2C bus number, for example
# with the 128x32 display you would use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

# 128x32 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# 128x64 display with hardware SPI:
# disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Alternatively you can specify a software SPI implementation by providing
# digital GPIO pin numbers for all the required display pins.  For example
# on a Raspberry Pi with the 128x32 display you might use:
# disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

# Initialize library.
DISP.begin()

# Clear display.
DISP.clear()
DISP.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
W = DISP.width
H = DISP.height

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
PADDING = 0
TOP = PADDING
BOTTOM = H - PADDING
# Move left to right keeping track of the current x position for drawing shapes.
x = 2

FONT = ImageFont.truetype('resources/fonts/YanoneKaffeesatz-Regular.ttf', 24)
FONT_BOLD = ImageFont.truetype('resources/fonts/YanoneKaffeesatz-Bold.ttf', 30)


def intro():
    with Image.open('resources/gfx/ProVeg_Badge_i.png').convert('1') as img:
        display(img)


def print_balance(name, balance):
    # Draw a black filled box to clear the image.
    img = Image.new('1', (W, H))
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, W, H), outline=0, fill=0)

    draw.text((x, TOP), name, font=FONT, fill=255)
    draw.text((x, TOP + 30), "Saldo:", font=FONT, fill=255)
    draw.text((x + 50, TOP + 24), "{} €".format(balance), font=FONT_BOLD, fill=255)
    display(img)


def display(img):
    DISP.image(img)
    DISP.display()


def main():
    while True:
        intro()
        sleep(1)
        print_balance('Salomon Popp', 19.5)
        sleep(1)


main()
