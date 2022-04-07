apt update
apt install -y i2c-tools python3-pip python3-pil python3-setuptools python3-rpi.gpio python3-setuptools git
python3 -m pip install --force-reinstall adafruit-blinka adafruit-circuitpython-ssd1306 pillow psutil

cat >/lib/systemd/system/screen-stats.service <<-EOM
[Unit]
Description=Screen stats is a screen for rasberry pi for show system stats via I2C
After=multi-user.target
Conflicts=getty@tty1.service

[Service]
User=root
Type=simple
ExecStart=/usr/bin/python3 /usr/bin/screen-stats/run.py
StandardInput=tty-force
Restart=always

[Install]
WantedBy=multi-user.target
EOM

mkdir -p /usr/bin/screen-stats/
cat >/usr/bin/screen-stats/run.py <<-EOM
import board
import time
import socket
import os
import shutil
import psutil

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

while True:
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
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
    draw.text((x, top + 20), f"Cpu: {cpu_percent}%", fill=255)
    draw.text((x, top + 30), f"Cpu Temp: {cpu_temp}°c", fill=255)
    draw.text((x, top + 40), f"Ram: {ram_percent}%", fill=255)
    draw.text(
        (x, top + 50),
        f"Disk: {hdd_used_formatted}/{hdd_total_formatted} G",
        fill=255,
    )

    oled.image(image)
    oled.show()
    time.sleep(1)
EOM

systemctl daemon-reload
systemctl enable screen-stats.service
systemctl start screen-stats.service