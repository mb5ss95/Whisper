import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
sys.path.append('/usr/local/lib/python3.7/dist-packages')

from Utility.BleConnection import Ble
from Utility.AudioPlayer import audioPlayer
from Utility.Gpio import myGpio

import time
import Adafruit_ADS1x15

def divide_Level(value):
    if 19632 <= value and 19760 > value:
        return 0
    elif 18900 <= value and 19632> value:
        return 1
    elif 17520 <= value and 18900 > value:
        return 2
    elif 16500 <= value and 17520 > value:
        return 3
    else:
        return -1

if __name__ == "__main__":
    adc = Adafruit_ADS1x15.ADS1115()
    player = audioPlayer()
    gpio = myGpio()
    gpio.start()
    ble = Ble()
    ble.start()

    pre_level = -1
    valueList = list()
    while True:
        try:
            value = adc.read_adc(1, gain=2/3)
            valueList.append(value)
            time.sleep(0.1)
            print(value)

            if len(valueList) >= 3:
                cur_level = divide_Level(value)
            
                print("value : {0}, Level : {1}".format(value, cur_level+1))
                
                if pre_level != cur_level:
                    player.set_Level(cur_level)
                    gpio.set_PlayList(cur_level)
                    player.start_Audio()
                    
                    pre_level = cur_level
                elif cur_level == -1:
                    player.stop_Audio()
                valueList.clear()

            
        except KeyboardInterrupt:
            gpio.DeadOrAlive()
            ble.DeadOrAlive()
            break;