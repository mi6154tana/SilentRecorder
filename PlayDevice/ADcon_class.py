import RPi.GPIO as GPIO
import time

class ADcon:
    #GPIO nomber define
    spi_clk = 11
    spi_miso = 9
    spi_mosi = 10
    spi_cs = 8

    hoge = []

    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        #GPIO device setup
        GPIO.setup(spi_mosi, GPIO.OUT)
        GPIO.setup(spi_miso, GPIO.IN)
        GPIO.setup(spi_clk , GPIO.OUT)
        GPIO.setup(spi_cs, GPIO.OUT)
        #GPIO.setup(4, GPIO.OUT)
        #GPIO.setup(17, GPIO.OUT)

    def readadc(self, adcnum, clockpin, mosipin, misopin, cspin):
        if adcnum > 7 or adcnum < 0:
            return -1
        GPIO.output(cspin, GPIO.HIGH)
        GPIO.output(clockpin, GPIO.LOW)
        GPIO.output(cspin, GPIO.LOW)

        commandout = adcnum
        commandout |= 0x18
        commandout <<= 3   
        for i in range(5):
            if commandout & 0x80:
                GPIO.output(mosipin, GPIO.HIGH)
            else:
                GPIO.output(mosipin, GPIO.LOW)
            commandout <<= 1
            GPIO.output(clockpin, GPIO.HIGH)
            GPIO.output(clockpin, GPIO.LOW)
        adcout = 0

        for i in range(13):
            GPIO.output(clockpin, GPIO.HIGH)
            GPIO.output(clockpin, GPIO.LOW)
            adcout <<= 1
            if i>0 and GPIO.input(misopin)==GPIO.HIGH:
                adcout |= 0x1
        GPIO.output(cspin, GPIO.HIGH)
        return adcout

    def core(self):
        file = open('test.txt', 'w')
        try:
            while True:
                time.sleep(0.001)
                inputVal0 = self.readadc(0, spi_clk, spi_mosi, spi_miso , spi_cs)
                volume = inputVal0
                hoge.append(volume)
                if inputVal0 < 2117:
                    volume = 2117 + ( 2117 - inputVal0)
                    if volume > 4095:
                        volume = 4095
                '''
                #LEDを光らせる
                if volume >= 2350 and volume < 4095:
                    GPIO.output(4, True)
                else:
                    GPIO.output(4, False)

                if volume >= 4095:
                    GPIO.output(17, True)
                else:
                    GPIO.output(17, False)
                print(volume)
                '''
                file.write(str(volume) + '\n')
        except KeyboardInterrupt:
            pass
        print(str(sum(hoge)/len(hoge)))#一定時間での平均値
        result = str(sum(hoge)/len(hoge))
        file.close()
        GPIO.cleanup()

        return result

