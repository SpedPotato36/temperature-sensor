from machine import Pin, I2C
import time, onewire, ds18x20
from pico_i2c_lcd import I2cLcd
#LCD setup
i2c = I2C(0,scl = Pin(1), sda = Pin(0), freq = 400000)
LCD = I2cLcd(i2c, 0x27, 2, 16)
#sensor setup
data_pin = Pin(15)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(data_pin))
roms = ds_sensor.scan()
#buzzer setup
buzzer = Pin(17, Pin.OUT)
#Pico led setup
Pico_led = Pin("LED", Pin.OUT)

#target temp is 50 degrees celcius
target_temp = 50

while True:
  #loop: recieve data from sensor, output on lcd
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  temp = ds_sensor.read_temp(roms[0])
  LCD.clear()
  LCD.putstr(f"temp: {temp}")
  if temp < target_temp - 2:
    buzzer.off()
    LCD.putstr("keep heating")
    Pico_led.off()
  elif temp <= target_temp + 2:
    buzzer.off()
    LCD.putstr("Perfect")
    Pico_led.on()
  else:
     LCD.putstr("Too hot")
     buzzer.on()
     Pico_led.toggle()
  time.sleep(1)
