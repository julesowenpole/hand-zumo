import libmapper as mpr
import serial
import time
import math

# --- Config ---
SERIAL_PORT = '/dev/tty.usbmodem14201'
BAUD_RATE = 9600
OPEN_THRESHOLD = 0.15  # tune this: average distance above = open hand, below = fist

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

# --- Shared landmark state ---
landmarks = {
    'Wrist':     [0.5, 0.5, 0.0],
    'IndexTIP':  [0.5, 0.5, 0.0],
    'MiddleTIP': [0.5, 0.5, 0.0],
    'RingTIP':   [0.5, 0.5, 0.0],
    'PinkyTIP':  [0.5, 0.5, 0.0],
}

def distance(a, b):
    return math.sqrt(sum((a[i] - b[i])**2 for i in range(3)))

def compute_openness():
    wrist = landmarks['Wrist']
    tips = ['IndexTIP', 'MiddleTIP', 'RingTIP', 'PinkyTIP']
    avg_dist = sum(distance(landmarks[t], wrist) for t in tips) / len(tips)
    return avg_dist

def send_command():
    openness = compute_openness()
    tilt = landmarks['Wrist'][0]  # x component: 0=left, 1=right

    if openness < OPEN_THRESHOLD:
        cmd = "S,0,0\n"  # fist = stop
    else:
        # open hand = forward, tilt controls steering
        base_speed = 200
        turn = int((tilt - 0.5) * 2 * base_speed)
        left  = max(-400, min(400, base_speed - turn))
        right = max(-400, min(400, base_speed + turn))
        cmd = f"F,{left},{right}\n"

    ser.write(cmd.encode())

# --- Generic handler factory ---
def make_handler(name):
    def handler(sig, event, inst, val, timetag):
        print(f"{name}: {val}, openness: {compute_openness():.3f}")  # temporary debug
        if isinstance(val, (list, tuple)):
            landmarks[name] = list(val)
        else:
            landmarks[name] = [val, val, val]
        send_command()
    return handler

# --- libmapper device ---
dev = mpr.Device("zumo_controller")

for name in landmarks:
    dev.add_signal(mpr.Signal.Direction.INCOMING, f"hand/{name}", 3,
                   mpr.Type.FLOAT, None, 0.0, 1.0, None, make_handler(name))

print("zumo_controller ready.")
print("tune OPEN_THRESHOLD if gesture detection feels off")

try:
    while True:
        dev.poll(50)
finally:
    dev.free()
    ser.close()