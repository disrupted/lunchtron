# Lunchtron

## What it is

This package is the automatic lunch money system used by ProVeg.

All employees have a card key based on a Myfare Classic 1k RFID smartcard,
and the UIDs are used to book every lunch an employeed has partaken.

The database backend is a MariaDB. Employees can top up their lunch money
account in cash with an administrator, who changes the amount in a
web interface.

In the future, topping up will also be possible using an automatic bank note
counter.

## Hardware

The "server" is a SBC, in our case a Raspberry Pi 3. Connected to it:
* via SPI: A RC522 board. See https://pimylifeup.com/raspberry-pi-rfid-rc522/
* via I2C: A 64x128 pixel OLED display for showing the current balance
* via USB: An ESC/POS receipt printer. (optional)

## Software

The software consists of three parts:
* The MariaDB backend
* The lunchtron-register python script that reads the RFID-cards, changes the balance and displays it.
* The lunchtron-admin where new users and cards can be created and the amount changed by admin users.
