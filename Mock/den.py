# Mock GPIO khi chạy trên máy tính
class MockGPIO:
    OUT = 'out'
    IN = 'in'
    BCM = 'BCM'  # Thêm giá trị BCM giả lập
    
    @staticmethod
    def setwarnings(warnings):
        pass  # Giả lập phương thức setwarnings, không làm gì cả
    
    @staticmethod
    def setmode(mode):
        pass
    
    @staticmethod
    def setup(pin, mode):
        pass
    
    @staticmethod
    def output(pin, state):
        pass
    
    @staticmethod
    def cleanup():
        pass

GPIO = MockGPIO()  # Thay thế RPi.GPIO bằng MockGPIO khi thử nghiệm trên máy tính
