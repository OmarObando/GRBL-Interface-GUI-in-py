import serial
import time

def connect_to_grbl(port, baud_rate):
    _interface = None
    try:
        _interface = serial.Serial(port,baud_rate, timeout = 1)
        _interface.flush()
        time.sleep(1) #Need wait to initialize the grbl
    except Exception as exception:
        _interface = None
    finally:
        return _interface

def send_gcode(interface, gcode):
    if interface:
        try:
            _encode_gcode = (gcode + '\n').encode('utf-8')
            interface.write((_encode_gcode))
            time.sleep(1) #Need wait to process
            #_response = interface.readline().decode('utf-8').strip()
            return gcode#_response
        except Exception as exception:
            return 'Error sending GCode'
        
def disconnect_from_grbl(interface):
    if interface:
        interface.close
        
