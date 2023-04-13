from tactisoft.threadedserial import ThreadedSerial


class Servos:
    def __init__(self, arduino: ThreadedSerial):
        self.arduino = arduino

    def set_servo_angle(self, servo_id: int, angle: int):
        self.arduino.send("R2+set_servo_angle=%s,%s" % (servo_id, angle))
