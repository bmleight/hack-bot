# a module to support the candy catapult


class Catapult:

  def __init__(self, port="/dev/serial/by-id/usb-Silicon_Labs_CP2104_USB_to_UART_Bridge_Controller_014C1A61-if00-port0", baud=115200):
    # initializing the serial port
    import serial
    self.ser=serial.Serial(port,baud)


  def dispense(self):
    # send the dispense command
    self.ser.write(b"d")

  def fire(self):
    # send the fire command
    self.ser.write(b"f")


