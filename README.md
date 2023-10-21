# PicoServerInfo
Server info for Source 1 based games on Pico. Needs LCD Display


## Requirements
1. Raspberry Pico W
2. 2x16 LED Display
3. I2C Converter for display


## Installation
1. Plug 4 cables to converter connect them to pico with these pins: GND - Any ground pin, VCC - VBUS pin cuz it gives 5 V, SDA and SCL can be connected to any non-ground pin. In my code, I used GP0 for SDA and GP1 for SCL
2. Install LCD library of CircuitPython on Pico (Download lcd folder to /lib of pico): https://github.com/dhalbert/CircuitPython_LCD
3. Add server.py into /lib folder of pico as well
4. Add main.py to pico (not in /lib folder)
5. Change server nick, server ip, server port, your wifi's SSID(Name) and password.

## Notes
The reason why I used server nick instead of server name is because server names might be too big for small lcd display like this.

## Donation
Contact me here for donations(even 1 USD is accepted)  
Instagram: @atlas_c0  
Discord: @atlas_c0
