import atexit
import board
import time
import socket
import os
import shutil
import psutil
from datetime import datetime

import adafruit_ssd1306

from PIL import Image, ImageDraw

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
WIDTH = 128
HEIGHT = 64

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)
oled.fill(0)
oled.show()
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

padding = -2
top = padding
bottom = oled.height - padding
x = 0

def exit_handler():
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    oled.image(image)
    oled.show()
atexit.register(exit_handler)

ram_total = str("%.2f" % (psutil.virtual_memory().total / (1024 ** 3)))
while True:
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    hdd_total, hdd_used, hdd_free = shutil.disk_usage("/")

    hostname = str(socket.gethostname())
    ip = str(os.popen("hostname -I").read())[:12]
    cpu_percent = str(psutil.cpu_percent())
    cpu_temp = str("%.2f" % (float(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000))
    ram_percent = str(psutil.virtual_memory().percent)
    hdd_used_formatted = str("%.2f" % (hdd_used / (1024.0**3)))
    hdd_total_formatted = str("%.2f" % (hdd_total / (1024.0**3)))
    uptime = datetime.fromtimestamp(int(os.popen("date -d "$(who -b | awk '{print $4,$3}' | tr - / )" +%s").read()))
    
    draw.text((x, top), f"Host: {hostname}", fill=255)
    draw.text((x, top + 8), f"Ip: {ip}", fill=255)
    draw.text((x, top + 16), f"Cpu: {cpu_percent}%", fill=255)
    draw.text((x, top + 24), f"Cpu Temp: {cpu_temp}°c", fill=255)
    draw.text((x, top + 32), f"Ram: {ram_percent}% / {ram_total}g", fill=255)
    draw.text(
        (x, top + 40),
        f"Disk: {hdd_used_formatted}g / {hdd_total_formatted}g",
        fill=255,
    )
    draw.text((x, top + 48), f"Uptime: {uptime}")

    oled.image(image)
    oled.show()
    time.sleep(1)

