import serial

class LCDInterface():

    def __init__(self, operation_mode="hardware"):
        self.operation_mode = operation_mode
        if (self.operation_mode == "hardware"):
            self.lcdCom = serial.Serial(
                    port="/dev/serial0",
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    timeout=1
                )
    
    def display(self, first_line, second_line):
        if len(first_line) > 16:
            raise ValueError("First line of text can not be more than 16 characters")
        if len(second_line) > 16:
            raise ValueError("Second line of text can not be more than 16 characters")

        if (self.operation_mode=="hardware"):
            self.lcdCom.write(b"\xFE\x01")
            self.lcdCom.write(bytes(str(first_line), "ASCII"))
            self.lcdCom.write(b"\xFE\xC0")
            self.lcdCom.write(bytes(str(second_line), "ASCII"))
        else:
            print(first_line)
            print(second_line)

    def clear(self):
        if (self.operation_mode == "hardware"):
            self.lcdCom.write(b"\xFE\x01")
            self.lcdCom.write(bytes("                ", "ASCII"))
            self.lcdCom.write(bytes("                ", "ASCII"))


    def close(self):
        if (self.operation_mode == "hardware"):
            self.lcdCom.close()
