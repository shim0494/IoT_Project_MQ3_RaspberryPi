import spidev
import time

spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=500000

def read_spi_adc(adcChannel):
    adcValue=0
    buff=spi.xfer2([1,(8+adcChannel)<<4,0])
    adcValue=((buff[1]&3)<<8)+buff[2]
    return adcValue

def valueTomL(adcValue):
    R2=2000
    adc_volt=(adcValue)/1024*5.0
    gas=((5.0*R2)/adc_volt)-R2
    R0 = 16000
    ratio = gas/R0
    x = 0.4*ratio
    BAC= x**(-1.431)
    return BAC

try:
    while True:
        adcChannel=0
        adcValue=read_spi_adc(adcChannel)
        BAC = valueTomL(adcValue)
        print("BAC = ")
        print(BAC*0.0001)
        print(" g/DL\n\n")
        time.sleep(0.2)
except KeyboardInterrupt:
    spi.close()