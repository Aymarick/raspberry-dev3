from flask import Flask, render_template, redirect, url_for
from led import Led
import RPi.GPIO as GPIO
app = Flask(__name__)

#Utilisation d'une norme de nommage pour les broches
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

redLed = Led(14)
greenLed = Led(15)

@app.route('/')
def home():
    return render_template('home.html')

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
    elif color == "green":
        greenLed.off()
    return redirect(url_for('home'))

@app.route('/blink/<color>')
def blink(color):
    if color == "red":
        redLed.blink(10, 0.05)
    elif color == "green":
        greenLed.blink(10, 0.05)
    return redirect(url_for('home'))

