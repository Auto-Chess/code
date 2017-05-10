
class LCDInterface():
    def __init__(self, operation_mode="hardware"):
        self.operation_mode = operation_mode
    
    def display(self, first_line, second_line):
        if (self.operation_mode=="hardware"):
            print("To hardware: {}".format(first_line))
            print("To hardware: {}".format(second_line))
        else:
            print(first_line)
            print(second_line)
        

 


