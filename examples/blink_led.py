import time

from atsbindings import Board, At


# Blink LED is the "hello world" equivalent for hardware
# recommended initial test

# Adjustable parameters
blink_period = 0.33 # seconds
blinking_duration = 7 # seconds


board = Board()
t0 = time.perf_counter()

while (time.perf_counter() - t0) < blinking_duration:
    board.set_led(At.LED.LED_ON)
    time.sleep(blink_period/2)
    board.set_led(At.LED.LED_OFF)
    time.sleep(blink_period/2)
