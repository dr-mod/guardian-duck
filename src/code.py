import digitalio
import time, board
from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut
import alarm

amp = digitalio.DigitalInOut(board.GP2)
amp.direction = digitalio.Direction.OUTPUT

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


def play_quack():
    amp.value = False
    wave_file = open("quack.wav", "rb")
    wave = WaveFile(wave_file)
    audio = AudioOut(board.GP1)
    audio.play(wave)
    led.value = True
    time.sleep(0.2)
    amp.value = True
    time.sleep(0.4)
    amp.value = False
    led.value = False
    audio.deinit()


sensor = digitalio.DigitalInOut(board.GP0)
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.DOWN
last_state = False

while True:
    value = sensor.value
    if value != last_state:
        last_state = value
        if value:
            play_quack()
    time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + 5)
    alarm.light_sleep_until_alarms(time_alarm)