import time
import RPi.GPIO as GPIO

class LEDMatrix():
    """LED Matrix contructor
    Args:
        - lows (int[]): GPIO pin numbers of pins which will act as voltage sinks
        - highs (int[]): GPIO pin numbers of pins which will provide voltage
    """
    def __init__(self, lows, highs):
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

    """Turn all GPIO pins to low except for the pin with the index specified
    Args:
        - value (int): Value to set all other pins to
        - pin_list (int[]): List of pins to turn to low
        - exception_i (int): Index to leave alone
    """
    def turn_all_to_except(self, value, pin_list, exception_i):
        if exception_i > len(pin_list) - 1:
            raise ValueError("exception_i can not be bigger than pin_list size: exception_i: {}, size: {}".format(exception_i, len(pin_list) - 1))

        i = 0
        for pin in pin_list:
            if i != exception_i:
                GPIO.output(pin, value)
            i += 1

    def cleanup(self):
        self.reset()
        GPIO.cleanup()

    """Add LED Matrix coordinate to list of LEDs to turn on during run
    Args:
        - x (int): X coordinate of LED to turn on
        - y (int): Y coordinate of LED to turn on
    """
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

    """Remove LED Matrix coordinate from list of LEDs to turn on during run
    Args:
        - x (int): X coordinate to remove from on list
        - y (int): Y coordinate to remove from on list
    """
    def remove_on(self, x, y):
        # Check if in on list
        if [x, y] in self.on:
            self.on.remove([x, y])
        else:
            raise IndexError("Not in ons")

    """Turn on LEDs until keyboard interupted
    Args:
        - run_max (int): Optional maximum number of runs
    """
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

matrix = LEDMatrix(lows=[26, 16], highs=[20, 21])
matrix.setup()

matrix.add_on(0, 0)
matrix.add_on(1, 0)
matrix.add_on(0, 1)
matrix.add_on(1, 1)
matrix.run()

for i in range(20):
    matrix.remove_on(0, 1)
    matrix.remove_on(1, 0)
    try:
        matrix.add_on(0, 0)
        matrix.add_on(1, 1)
    except ValueError as e:
        pass
    matrix.run(run_max=100)

    matrix.remove_on(0, 0)
    matrix.remove_on(1, 1)
    try:
        matrix.add_on(0, 1)
        matrix.add_on(1, 0)
    except ValueError as e:
        pass
    matrix.run(run_max=100)

matrix.cleanup()
