systemctl stop screen-stats.service
apt update
python3 -m pip uninstall adafruit-blinka adafruit-circuitpython-ssd1306 pillow psutil
rm -rf /lib/systemd/system/screen-stats.service
rm -rf /usr/bin/screen-stats
systemctl daemon-reload