import serial


class Instrument:
    def __init__(self, port="COM7", baudrate=9600, timeout=1):
        self.conn = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
    
    def write(self, command):
        self.conn.write((command + '\n').encode())
    
    def read(self):
        return self.conn.readline()
    
    def close(self):
        self.conn.close()
        
    def test(self):
        return None

    def disable_output_trigger(self):
        self.write(":TRIG:OUTP NONE")

    def trigger_immediately(self):
        self.write(":ARM:SOUR IMM;:TRIG:SOUR IMM;")

    def sample_continuosly(self):
        self.disable_output_trigger()
        self.trigger_immediately()

    def set_timed_arm(self, interval):
        interval = round(interval, 3)
        if interval > 99999 or interval < 0.001:
            return "Interval can be in range 0.001 - 99999 s"
        else:
            self.write(f":ARM:SOUR TIM;:ARM:TIM {interval}")

    def set_trigger_counts(self, arm, trigger):
        if arm * trigger > 2500 or arm * trigger < 0:
            return "Total point cannot exeed 2500"
        elif arm < trigger:
            self.write(":ARM:COUN %d;:TRIG:COUN %d" % (arm, trigger))
        else:
            self.write(":TRIG:COUN %d;:ARM:COUN %d" % (trigger, arm))
        return "Set up arm and trigger counts"

    def setup(self):
        self.sample_continuosly()
        self.set_timed_arm(0.01)
        self.set_trigger_counts(10, 10)

    def source_enabled(self, enabled):
        if enabled:
            comamnd = "OUTP 1"
        elif not enabled:
            command = "OUTP 0"
        else:
            return "Failed to enable/disable source"
        self.write(command)
        response = self.read()
        return f"enabled/disabled source, response: {response}"

    def source_value(self, value):
        if self.source_mode == "V":
            self.write(f":SOUR:VOLT:LEV {value}")
        elif self.source_mode == "C":
            self.write(f":SOUR:CURR:LEV {value}")
    
    def source_mode(self, mode):
        if mode == "V":
            command = ":SOUR:FUNC VOLT"
            self.source_mode = "V"
        elif mode == "C":
            command = ":SOUR:FUNC CURR"
            self.source_mode = "C"
        else:
            return "Failed to change source mode"
        self.write(command)
        response = self.read()
        return f"changed mode to {mode}, response: {response}"
