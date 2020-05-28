from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, send, emit
from led import Led
from buzzer import Buzzer
from temperature import TemperatureSensor
from light import LightSensor
from movement import MovementSensor
import RPi.GPIO as GPIO
from threading import Thread
app = Flask(__name__)
socketio = SocketIO(app)
#Utilisation d'une norme de nommage pour les broches
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

redLed = Led(14)
greenLed = Led(15)
buzzer = Buzzer(18)

tempSensor = TemperatureSensor('28-01131a4f0da1')

lightSensor = LightSensor(27)

@app.route('/')
def home():
    temp = tempSensor.read_temp()
    return render_template('home.html', temp=temp)

@app.route('/temp')
def temp():
    temp = tempSensor.read_temp()
    return str(temp)

@app.route('/light')
def light():
    light = lightSensor.read_light()
    if light < 300:
        return 'Il fait jour'
    else:
        return 'Il fait nuit'

@app.route('/beep')
def beep():
    buzzer.beep(0.5)
    return redirect(url_for('home'))

@app.route('/on/<color>')
def on(color):
    if color == "red":
        redLed.on()
    elif color == "green":
        greenLed.on()
    return redirect(url_for('home'))

@app.route('/off/<color>')
def off(color):
    if color == "red":
        redLed.off()
        redLed.cancel()
    elif color == "green":
        greenLed.off()
        greenLed.cancel()
    return redirect(url_for('home'))

@app.route('/blink', methods=['POST'])
def blink():
    color = request.form['color']
    numBlink = int(request.form['numBlink'])
    sleepTime = float(request.form['sleepTime'])
    led = None
    if color == "red":
        led = redLed
    elif color == "green":
        led = greenLed
    thread = Thread(target=led.blink, args=(numBlink, sleepTime, ))
    thread.start()
    return redirect(url_for('home'))

def detect():
    redLed.on()
    greenLed.off()
    print("Mouvement détecté")
    socketio.emit('alert', 'Mouvement détecté', Broadcast=True)

def ready():
    redLed.off()
    greenLed.on()
    print("Prêt")
    socketio.emit('alert', 'Prêt', Broadcast=True)

movement = MovementSensor(17, detect, ready)
# movement.startDetection()
