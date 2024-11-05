import time

from atsbindings import Board, Ats


# Blink LED is the "hello world" equivalent for hardware.
# Recommended using this as an initial test.

# Adjustable parameters
blink_period = 0.33 # seconds
blinking_duration = 5 # seconds

board = Board()

print(f"Blinking will continue for {blinking_duration:.1f} seconds. \nStarting...")

t0 = time.perf_counter()
while (time.perf_counter() - t0) < blinking_duration:
    board.set_led(Ats.LED.LED_ON)
    time.sleep(blink_period/2)
    board.set_led(Ats.LED.LED_OFF)
    time.sleep(blink_period/2)

print("Blinking finished.")