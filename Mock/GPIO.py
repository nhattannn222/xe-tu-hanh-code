# Mock.GPIO.py
def setwarnings(flag):
    print(f"Set warnings to: {flag}")

def setmode(mode):
    print(f"Set mode to: {mode}")

def setup(pin, mode):
    print(f"Set up pin {pin} as {mode}")

def output(pin, state):
    print(f"Set output on pin {pin} to {state}")

def input(pin):
    return 0  # Mô phỏng trạng thái input, có thể là 0 hoặc 1

def cleanup():
    print("Cleaned up all GPIO pins.")

# Các hằng số giả lập
OUT = "OUT"
IN = "IN"
BCM = "BCM"
