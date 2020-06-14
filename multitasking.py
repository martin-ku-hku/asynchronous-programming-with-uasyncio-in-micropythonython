from machine import Pin, PWM, ADC
import uasyncio

led = PWM(Pin(5), 5000)
pot = ADC(Pin(36))
pot.atten(ADC.ATTN_11DB)

brightness = 0

async def blink():
    global brightness
    while True:
        led.duty(brightness)
        await uasyncio.sleep(1)
        led.duty(0)
        await uasyncio.sleep(1)
        
async def update_brightness():
    global brightness
    while True:
        brightness = int(round(pot.read() / 4))
        await uasyncio.sleep_ms(100)
        
event_loop = uasyncio.get_event_loop()
event_loop.create_task(blink())
event_loop.create_task(update_brightness())
event_loop.run_forever()