from typing import Optional
from dotenv import dotenv_values
from utils import spotify
import threading
import queue
import RPi.GPIO as GPIO
import time
import serial


config = dotenv_values(".env")

GPIO.setmode(GPIO.BOARD)

pause_btn_gpio = 36
prev_btn_gpio = 38
next_btn_gpio = 40

GPIO.setup(pause_btn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(prev_btn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(next_btn_gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)


client_id: Optional[str] = config["SPOTIFY_CLIENT_ID"]
client_secret: Optional[str] = config["SPOTIFY_CLIENT_ID"]

# TODO: store data in sqlite
access_token: str = config["SPOTIFY_ACCESS_TOKEN"] or ""
current_volume: Optional[int] = None

if client_id is None:
    print("Missing Spotify client id")

if client_secret is None:
    print("Missing Spotify client secret")


class Jukebox:
    def __init__(self):
        self.queue = queue.Queue()
        self.event = threading.Event()
        self.serial_thread = threading.Thread(target=self.read_rfid, args=())
        self.serial_thread.start()
        self.gpio_thread = threading.Thread(target=self.read_gpio, args=())
        self.gpio_thread.start()
        self.periodicCall()

    def periodicCall(self):
        print("periodicCall")
        self.processIncoming()
        self.event.wait(0.5)
        self.periodicCall()

    def processIncoming(self):
        print("processIncoming")
        print(self.queue.qsize())
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                if len(msg) == 12:
                    print("msg", msg)
                    spotify.change_playlist(access_token)

            except Queue.Empty:
                pass

    def read_rfid(self):
        print("read_rfid")
        ser = serial.Serial("/dev/ttyS0")
        ser.baudrate = 9600
        ser.flushInput()

        msg = ""
        while True:
            while ser.inWaiting() > 0:
                print("while ser > 0")
                msg = ser.read(12)

            if msg != "":
                msg = msg.decode("utf-8")
                print(msg)
                self.queue.put(msg)
                msg = ""

    def read_gpio(self):
        print("read_gpio")
        while True:
            pause_btn_state = GPIO.input(pause_btn_gpio)
            prev_btn_state = GPIO.input(prev_btn_gpio)
            next_btn_state = GPIO.input(next_btn_gpio)

            if pause_btn_state == 0:
                print("pause_btn_state == 0")
                spotify.switch_playback(access_token)
                time.sleep(1)

            if prev_btn_state == 0:
                print("pause_btn_state == 0")
                spotify.previous_song(access_token)
                time.sleep(1)

            if next_btn_state == 0:
                print("next_btn_state")
                spotify.next_song(access_token)
                time.sleep(1)


jukebox = Jukebox()
