import serial

class LCDInterface():

    def __init__(self, operation_mode="hardware"):
        self.operation_mode = operation_mode
        self.lcdCom = serial.Serial
            (
             port="/dev/serial0",
             baudrate=9600,
             parity=serial.PARITY_NONE,
             stopbits=serial.STOPBITS_ONE,
             bytesize=serial.EIGHTBITS,
             timeout=1
            )
    
    def display(self, first_line, second_line):
        if (self.operation_mode=="hardware"):
            print("To hardware: {}".format(first_line))
            print("To hardware: {}".format(second_line))
        else:
            print(first_line)
            print(second_line)

    def clear():
        self.lcdCom.write(b"\xFE\x01")
        self.lcdCom.write(bytes("                ", "ASCII"))
        self.lcdCom.write(bytes("                ", "ASCII"))

    def dPrint():
        self.lcdCom.write(b"\xFE\x01")
        self.lcdCom.write(bytes("Line 1", "ASCII"))
        self.lcdCom.write(bytes("Line 2", "ASCII"))

    def close():
        self.lcdCom.close()
