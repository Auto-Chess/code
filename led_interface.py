import collections
import time
import RPi.GPIO as GPIO
from chess_position import ChessPosition
from chess_move import ChessMove

class LedInterface():

    def __init__(self, operation_mode="hardware", lows, highs):
        self.operation_mode = operation_mode

        if self.operation_mode == "hardware":
            import RPi.GPIO as GPIO
        else:
            from fake_gpio import GPIO


        self.lows = lows
        self.highs = highs

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
        for pin in self.lows:
            GPIO.output(pin, 0)

        for pin in self.highs:
            GPIO.output(pin, 0)

    def turn_all_to_except(self, value, pin_list, exception_i):
        if exception_i > len(pin_list) - 1:
            raise ValueError(
                "exception_i can not be bigger than pin_list size: exception_i: {}, size: {}".format(exception_i,
                                                                                                     len(pin_list) - 1))

        i = 0
        for pin in pin_list:
            if i != exception_i:
                GPIO.output(pin, value)
            i += 1

    def cleanup(self):
        self.reset()
        GPIO.cleanup()

    def add_on(self, x, y):
        # Check if x and y in bounds
        if x > len(self.highs) - 1:
            raise ValueError("x can not be bigger than high length")
        if y > len(self.lows) - 1:
            raise ValueError("y can not be bigger than lows length")

        # Check if already on
        if [x, y] in self.on:
            raise ValueError("Already added to on")

        # Otherwise add
        self.on.append([x, y])

    def remove_on(self, x, y):
        # Check if in on list
        if [x, y] in self.on:
            self.on.remove([x, y])
        else:
            raise IndexError("Not in ons")

    def run(self, run_max=None):
        run_count = 1
        while run_max is None or run_count < run_max:
            try:
                # For each coordinate to turn on
                print("Running Matrix for the {}th time".format(run_count))
                for coord in self.on:
                    x = coord[0]
                    y = coord[1]

                    high_pin = self.highs[x]
                    low_pin = self.lows[y]

                    print("    ({}, {}) => pins: (high_pin, low_pin) = ({}, {})".format(x, y, high_pin, low_pin))

                    GPIO.output(high_pin, 1)
                    self.turn_all_to_except(0, self.highs, x)

                    GPIO.output(low_pin, 0)
                    self.turn_all_to_except(1, self.lows, y)

                    run_count += 1
                    time.sleep(0.1 / len(self.on))

            except KeyboardInterrupt as e:
                print("Stopping")
                return;

    def turn_on_led(self, position):
        if self.operation_mode == "hardware":
            GPIO.output(12, 1)
        else:
            print("LED was turned on")

    def turn_off_led(self, position):
        if self.operation_mode == "hardware":
            GPIO.output(12, 0)
        else:
            print("LED was turned off")

    def start_blinking_led(self, position, blink_interval):
        if self.operation_mode == "hardware":
            for i in range(5)
            GPIO.output(12, 1)
            time.sleep(1)
            GPIO.output(12, 0)
            time.sleep(1)
        else:
            print("LED started blinking")

    def stop_blinking_led(self, position, blink_interval):
        if self.operation_mode == "hardware":
            GPIO.output(12, 0)
        else:
            print("LED stopped blinking")

    def stop_all(self, position):
        if self.operation_mode == "hardware":
            GPIO.output(12, 0)
        else:
            print("All LEDs were turned off")

matrix = LEDMatrix(lows=[26, 16], highs=[20, 21])
matrix.setup()