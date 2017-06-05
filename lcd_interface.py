
class LCDInterface():

    #Method to check that the code is running in the hardware
    def __init__(self, operation_mode="software"):
        self.operation_mode = operation_mode
        if (self.operation_mode == "hardware"):
            import serial
            self.lcdCom = serial.Serial(
                    port="/dev/serial0",
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )
    #Creating variables and using them in this method to display text to the LCD Display
    def display(self, first_line, second_line):
        if len(first_line) > 16:
            raise ValueError("First line of text can not be more than 16 characters")
        if len(second_line) > 16:
            raise ValueError("Second line of text can not be more than 16 characters")

        self.clear()

        if (self.operation_mode=="hardware"):
            self.lcdCom.write(bytes(str(first_line), "ASCII"))
            self.lcdCom.write(b"\xFE\xC0")
            self.lcdCom.write(bytes(str(second_line), "ASCII"))
        else:
            print(first_line)
            print(second_line)

    #Creating a method to clear the text currently displaying on the screen
    def clear(self):
        if (self.operation_mode == "hardware"):
            self.lcdCom.write(b"\xFE\x01")
            self.lcdCom.write(bytes("                ", "ASCII"))
            self.lcdCom.write(bytes("                ", "ASCII"))

    #This is the method to exit the program and disconnect from the LCD
    def close(self):
        if (self.operation_mode == "hardware"):
            self.lcdCom.close()

