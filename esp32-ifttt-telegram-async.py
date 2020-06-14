import network
import urequests as requests
from machine import Pin
from dht import DHT11
import uasyncio

wifi_ssid = "YOUR_WIFI_SSID"
wifi_password = "YOUR_WIFI_PASSWORD"
webhook_url = "https://maker.ifttt.com/trigger/esp32/with/key/YOUR_IFTTT_KEY"


sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(wifi_ssid, wifi_password)
while not sta_if.isconnected():
    print(".", end = "")

dht11 = DHT11(Pin(15))
# initialize the global variables
dht11.measure()
temperature = dht11.temperature()
humidity = dht11.humidity()

async def measure():
    global temperature, humidity
    while True:
        dht11.measure()
        temperature = dht11.temperature()
        humidity = dht11.humidity()
        await uasyncio.sleep(1)
        
async def send_message():
    global temperature, humidity
    while True:
        url = webhook_url + "?value1=" +  str(temperature) + "&value2=" + str(humidity)
        try:
            r = requests.get(url)
            print(r.text)
        except Exception as e:
            print(e)
        await uasyncio.sleep(60)
        
event_loop = uasyncio.get_event_loop()
event_loop.create_task(measure())
event_loop.create_task(send_message())
event_loop.run_forever()
