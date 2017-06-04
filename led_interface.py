import collections
from chess_position import ChessPosition
from chess_move import ChessMove
from multiprocessing import Process

import time
import RPi.GPIO as GPIO
import threading

class LedInterface():

    def __init__(self, lows, highs):
       self.lows = lows
       self.highs = highs

       self.on = []
       self.blinking = []
       self.intervals = {}

       self.on_lock = threading.Lock()


    def setup(self):
        GPIO.setmode(GPIO.BCM)

        # Init all pins
        for pin in self.lows:
            GPIO.setup(pin, GPIO.OUT)

        for pin in self.highs:
            GPIO.setup(pin, GPIO.OUT)

    def reset(self):
        # Set all to low
        for pin in self.lows:
            GPIO.output(pin, 0)

        for pin in self.highs:
            GPIO.output(pin, 0)

    def turn_all_to_except(self, value, pin_list, exception_i):
        i = 0
        for pin in pin_list:
            if i != exception_i:
                GPIO.output(pin, value)
            i += 1

    def cleanup(self):
        self.reset()
        GPIO.cleanup()

    def turn_on_led(self, position):
        x = position.col_to_int()
        y = position.row - 1

        # Check if x and y in bounds
        if x > len(self.highs) - 1:
            raise ValueError("x can not be bigger than high length")
        if y > len(self.lows) - 1:
            raise ValueError("y can not be bigger than lows length")

        # Check if already on
        if [x, y] in self.on:
            raise ValueError("Already added to on")

        # Otherwise add
        with self.on_lock:
            self.on.append([x, y])

    def turn_off_led(self, position):
        x = position.col_to_int()
        y = position.row - 1


        if [x, y] in self.on:
            self.on.remove([x, y])

    def start_blinking_led(self, position, blink_interval):
        x = position.col_to_int()
        y = position.row - 1
        self.blinking.append({
            'x': x,
            'y': y
        })
        self.intervals["{}{}".format(x, y)] = {
            'interval': blink_interval,
            'last_blink': time.time()
        }

    def stop_blinking_led(self, position):
        x = position.col_to_int()
        y = position.row - 1

        if [x, y] in self.blinking:
            self.blinking.remove([x, y])

    def stop_all(self):
        self.on = []
        self.blinking = []
        self.intervals = {}

    """Turn on LEDs until keyboard interupted
    Args:
        - run_max (int): Optional maximum number of runs
    """
    def run(self, run_max=None):
        run_count = 1
        while run_max is None or run_count < run_max:
            try:
                # For each coordinate to turn on
                for coord in self.blinking:
                    t = "{}{}".format(coord['x'], coord['y'])
                    timing = self.intervals[t]

                    c = ChessPosition(["a", "b", "c", "d", "e", "f", "g", "h"][coord['x']], coord['y'] + 1)
                    dt = time.time() - timing['last_blink']

                    if dt >= 0 and dt < timing['interval']:
                        try:
                            self.turn_on_led(c)
                        except Exception:
                            pass
                    elif dt >= timing['interval'] and dt < timing['interval'] * 2:
                        try:
                            self.turn_off_led(c)
                        except Exception:
                            pass
                    elif dt >= timing['interval'] * 2:
                        self.intervals[t]['last_blink'] = time.time()

                with self.on_lock:
                    for coord in self.on:
                        x = coord[0]
                        y = coord[1]

                        high_pin = self.highs[x]
                        low_pin = self.lows[y]

                        GPIO.output(high_pin, 1)
                        self.turn_all_to_except(0, self.highs, x)

                        GPIO.output(low_pin, 0)
                        self.turn_all_to_except(1, self.lows, y)

                        run_count += 1
                        divisor = len(self.on)
                        if (divisor == 0):
                            divisor = 1

                        time.sleep(0.01 / divisor)

            except KeyboardInterrupt as e:
                print("Stopping")
                self.cleanup()
                exit()
                return

    def start_run_in_thread(self):
        self.process = threading.Thread(target=self.run)
        self.process.start()