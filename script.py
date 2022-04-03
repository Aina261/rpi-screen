import time
import socket
import os
import shutil
import psutil

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw

RST = None
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

display = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

display.begin()
display.clear()
display.display()
width = display.width
height = display.height
image = Image.new("1", (width, height))

draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

padding = -2
top = padding
bottom = height - padding
x = 0

while True:
    display.clear()
    display.display()
    hdd_total, hdd_used, hdd_free = shutil.disk_usage("/")

    hostname = str(socket.gethostname())
    ip = str(os.popen("hostname -I").read())[:12]
    cpu_percent = str(psutil.cpu_percent())
    cpu_temp = str("%.2f" % (float(open("/sys/class/thermal/thermal_zone0/temp").read()) / 1000))
    ram_percent = str(psutil.virtual_memory()[2])
    hdd_used_formatted = str("%.2f" % (hdd_used / (1024.0**3)))
    hdd_total_formatted = str("%.2f" % (hdd_total / (1024.0**3)))

    draw.text((x, top), f"Host: {hostname}", fill=255)
    draw.text((x, top + 10), f"Ip: {ip}", fill=255)
    draw.text(
        (x, top + 20),
        f"Cpu: {cpu_percent}% | Temp: {cpu_temp}°c",
        fill=255,
    )
    draw.text((x, top + 30), f"Ram: {ram_percent}%", fill=255)
    draw.text(
        (x, top + 40),
        f"Disk: {hdd_used_formatted}/{hdd_total_formatted} G",
        fill=255,
    )

    display.image(image)
    display.display()
    time.sleep(1)
