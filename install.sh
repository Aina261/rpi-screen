apt update && apt upgrade -y
apt install -y i2c-tools python3-pil python3-setuptools python3-rpi.gpio python3-setuptools git
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
python3 setup.py install
