import collections
import time
import threading
from chess_position import ChessPosition

GPIO = None

class LedInterface():
    def __init__(self, lows, highs, operation_mode="software"):
        global GPIO
        self.operation_mode = operation_mode

        if self.operation_mode == "hardware":
            import RPi.GPIO as _GPIO
            GPIO = _GPIO
        else:
            from fake_gpio import GPIO as _GPIO
            GPIO = _GPIO

        self.lows = lows
        self.highs = highs

        self.on = []
        self.on_lock = threading.Lock()

        self.blinking = []
        self.last_blinks = {}
        self.blink_intervals = {}
        self.blinking_lock = threading.Lock()

        self.running = True

    def all_off(self):
        self.on = []

    def setup(self):
        GPIO.setmode(GPIO.BCM)

        # Init all pins
        for pin in self.lows:
            GPIO.setup(pin, GPIO.OUT)

        for pin in self.highs:
            GPIO.setup(pin, GPIO.OUT)

    def reset(self):
        # Set all to low
        if self.operation_mode == "hardware":
            for pin in self.lows:
                GPIO.output(pin, 1)

            for pin in self.highs:
                GPIO.output(pin, 0)


    def cleanup(self):
        self.reset()

        if self.operation_mode == "hardware":
            GPIO.cleanup()

    def turn_all_to_except(self, value, pin_list, exception_i):
        i = 0
        for pin in pin_list:
            if i != exception_i:
                if self.operation_mode == "hardware":
                    GPIO.output(pin, value)
            i += 1

    def turn_on_led(self, position):
        # Check if x and y in bounds
        x = position.col_to_int()
        y = position.row-1

        if x > len(self.highs) - 1:
            raise ValueError("x can not be bigger than high length")
        if y > len(self.lows) - 1:
            raise ValueError("y can not be bigger than lows length")

        # Otherwise add
        with self.on_lock:
            self.on.append([x, y])

    def turn_off_led(self, position):
        # Check if in on list
        x = position.col_to_int()
        y = position.row - 1

        if [x, y] in self.on:
            with self.on_lock:
                self.on.remove([x, y])
        else:
            raise IndexError("Not in ons")

    def start_blinking_led(self, position, interval):
        x = position.col_to_int()
        y = position.row - 1

        with self.blinking_lock:
            self.blinking.append([x,y])
            k = "{}{}".format(x,y)
            self.last_blinks[k] = time.time()
            self.blink_intervals[k] = interval

    def stop_all(self):
        with self.blinking_lock:
            self.blinking = []
            self.last_blinks = {}
            self.blink_intervals = {}

        with self.on_lock:
            self.on = []

    def run(self):
        self.running = True
        while self.running:
            with self.blinking_lock:
                for pos in self.blinking:
                    x = pos[0]
                    y = pos[1]
                    k = "{}{}".format(x, y)
                    dt = time.time()-self.last_blinks[k]
                    i = self.blink_intervals[k]


                    if dt >= 0 and dt < i:
                        with self.on_lock:
                            if [x, y] not in self.on:
                                self.on.append([x, y])
                    elif dt >= i and dt < i*2:
                        with self.on_lock:
                            if [x, y] in self.on:
                                self.on.remove([x, y])
                    elif dt >= i*2:
                        self.last_blinks[k] = time.time()

            self.reset()
            with self.on_lock:
                for pos in self.on:
                    x = pos[0]
                    y = pos[1]

                    high_pin = self.highs[x]
                    low_pin = self.lows[y]

                    if self.operation_mode == "hardware":
                        GPIO.output(high_pin, 1)
                        self.turn_all_to_except(0, self.highs, x)

                    if self.operation_mode == "hardware":
                        GPIO.output(low_pin, 0)
                        self.turn_all_to_except(1, self.lows, y)

                    divisor = len(self.on)
                    if divisor == 0:
                        divisor = 1

                    time.sleep(0.01 / divisor)

    def start_run_in_thread(self):
        self.thread = threading.Thread(target= self.run)
        self.thread.start()
