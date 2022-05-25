import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import datetime
import threading
import smtplib
from timeit import default_timer as timer

DHT_SENSOR = Adafruit_DHT.DHT11

#sensors
DHT_PIN = 4
MIC_PIN = 14
LIGHT_PIN = 15
PIR_PIN = 27

#leds
MIC_LED_PIN = 23
LIGHT_LED_PIN = 21
PIR_LED_PIN = 25

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#setup sensors
GPIO.setup(DHT_PIN, GPIO.IN)
GPIO.setup(MIC_PIN, GPIO.IN)
GPIO.setup(LIGHT_PIN, GPIO.IN)
GPIO.setup(PIR_PIN, GPIO.IN)

#setup leds
GPIO.setup(MIC_LED_PIN, GPIO.OUT)
GPIO.setup(LIGHT_LED_PIN, GPIO.OUT)
GPIO.setup(PIR_LED_PIN, GPIO.OUT)

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("proiect.sm.1307A@gmail.com","amadeus123!")

mutex = threading.Lock()

def sendMail(msg):
    mutex.acquire()
    server.sendmail("proiect.sm.1307A@gmail.com","proiect.sm.1307A@gmail.com",msg)
    mutex.release()

def readDHT():
    
    currentHumidity, currentTemperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    while currentHumidity is None or currentTemperature is None:
        currentHumidity, currentTemperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(currentTemperature, currentHumidity))
    try:
        file = open('/home/pi/website/resources/data.csv','a')
        now = datetime.datetime.now()
        file.write("{:02d}/{:02d}/{:04d} {:02d}:{:02d}:{:02d},{},{}\n".format(now.day, now.month, now.year, now.hour, now.minute, now.second, currentTemperature, currentHumidity))
        file.close()
    except Exception as e:
        print(e)
    threading.Timer(10, readDHT).start()

def readPIR(PIR_PIN):
    print("Motion Detected!")
    GPIO.output(PIR_LED_PIN, GPIO.HIGH)

    time.sleep(2)
    
    msg="Sensorul spune ca a fost detectata miscare"
    sendMail(msg)

    print("S-a trimis mail , la " + str(datetime.datetime.now()))

    GPIO.output(PIR_LED_PIN, GPIO.LOW)
    
lightDetected = False
firstLightDetection = -999

def detectLigh():
    global lightDetected
    global firstLightDetection
    while True:
      #de schimbat pe false
      if GPIO.input(LIGHT_PIN) == True:
          GPIO.output(LIGHT_LED_PIN, GPIO.HIGH)
          if lightDetected == False:
              lightDetected = True
              firstLightDetection = timer()
          elif lightDetected == True and timer() - firstLightDetection > 2:
              print("lumina mai mult de 2 sec detectata")
              
              msg="Sensorul spune ca a fost detectata lumina"
              sendMail(msg)
          
              print("S-a trimis mail , la " + str(datetime.datetime.now()))
              time.sleep(2)
      else:
          GPIO.output(LIGHT_LED_PIN, GPIO.LOW)
          lightDetected = False

soundDetected = False
firstSoundDetection = -999

def detectSound():
    global soundDetected
    global firstSoundDetection
    while True:
      if GPIO.input(MIC_PIN) == True:
          GPIO.output(MIC_LED_PIN, GPIO.HIGH)
          
          if soundDetected == False:
              soundDetected = True
              firstSoundDetection = timer()
          elif soundDetected == True and timer() - firstSoundDetection < 1:
              soundDetected = False
              print("Sunet detectat")
              
              msg="Sensorul spune ca a fost detectat sunet"
              sendMail(msg)
          
              print("S-a trimis mail , la " + str(datetime.datetime.now()))
              time.sleep(2)
          else:
              soundDetected = False
                 
      else:
          GPIO.output(MIC_LED_PIN, GPIO.LOW)

#readDHT()
GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=readPIR, bouncetime=2000)

DHTThread = threading.Thread(target=readDHT)
detectLighThread = threading.Thread(target=detectLigh)
detectSoundThread = threading.Thread(target=detectSound)

DHTThread.start()
detectLighThread.start()
detectSoundThread.start()
while True:
    time.sleep(1)


