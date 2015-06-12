# -*- coding:utf-8 -*-

import time
import webiopi
#import MotorDrive

webiopi.setDebug()

GPIO = webiopi.GPIO

Pin1 = 22
Pin2 = 27

pulltime = 3
waittime = 1
releasetime = 3

PIN1 = None
PIN2 = None

def setup():
    # GPIO.setmode(GPIO.BCM)
    setpin(Pin1,Pin2)

# def loop():
## Describe code which you want to looped while running

@webiopi.macro
def fireExtinguish():
    webiopi.debug( "fireExtinguish")
    webiopi.debug("FireFight!")
    positive_rotation()
    webiopi.debug("Pulling")
    webiopi.sleep(pulltime)
    stop()
    webiopi.debug("Waiting")
    webiopi.sleep(waittime)
    negative_rotation()
    webiopi.debug("Releasing")
    webiopi.sleep(releasetime)
    webiopi.debug("Finished")
    stop()
    webiopi.sleep(2)


def setpin(Pin1, Pin2) :
# 引数で受け取ったピン番号を出力端子として設定
    global PIN1,PIN2
        # GPIOの初期化
        # GPIO.setmode(GPIO.BCM)
    GPIO.setFunction(Pin1, GPIO.OUT);	PIN1 = Pin1
    GPIO.setFunction(Pin2, GPIO.OUT);	PIN2 = Pin2

def positive_rotation() :
# モーターを正回転させる
    if(PIN1 and PIN2) :
        webiopi.debug("positive rotation")
        GPIO.digitalWrite(PIN1,True)
        GPIO.digitalWrite(PIN2,False)

def negative_rotation() :
# モーターを逆回転させる
    if(PIN1 and PIN2) :
        webiopi.debug("negative rotation")
        GPIO.digitalWrite(PIN1,False)
        GPIO.digitalWrite(PIN2,True)

def stop() :
# モーターの回転を止める
    if(PIN1 and PIN2) :
        GPIO.digitalWrite(PIN1,False)
        GPIO.digitalWrite(PIN2,False)

# def clean():
# 	# GPIOの使用終了を宣言
# 	GPIO.cleanup()