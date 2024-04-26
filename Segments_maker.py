import serial
import time


pattern = [
            [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248],
            [45, 12, 182, 77, 99, 94, 135, 158, 223, 42, 162, 158, 67, 238, 32, 150, 143, 2, 149, 169, 150, 149, 59, 119, 77, 154, 144, 228, 71, 111, 236, 55],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [50, 42, 9, 8, 211, 138, 84, 0, 29, 122, 43, 190, 242, 86, 151, 165, 116, 75, 34, 67, 236, 249, 69, 61, 169, 195, 239, 22, 217, 185, 226, 59],
            [92, 242, 8, 132, 173, 5, 244, 59, 41, 69, 154, 40, 50, 248, 176, 89, 73, 139, 180, 186, 157, 77, 22, 184, 58, 93, 20, 57, 21, 234, 166, 78],
            [43, 233, 33, 244, 242, 73, 60, 138, 67, 156, 225, 75, 231, 227, 136, 20, 71, 78, 239, 212, 217, 34, 132, 124, 200, 53, 210, 124, 223, 210, 179, 222],
            [231, 186, 173, 182, 98, 105, 3, 19, 244, 62, 153, 192, 141, 108, 79, 150, 25, 219, 233, 216, 143, 247, 198, 83, 95, 231, 113, 60, 196, 207, 43, 223],
            [126, 3, 40, 136, 117, 88, 39, 72, 106, 34, 159, 172, 11, 194, 98, 38, 252, 32, 122, 88, 18, 132, 157, 187, 120, 244, 215, 58, 117, 198, 188, 232],
            [ 179, 254, 97, 241, 118, 108, 212, 133, 240, 73, 125, 129, 211, 58, 201, 31, 35, 241, 101, 154, 93, 184, 188, 36, 96, 194, 49, 239, 37, 178, 94, 47],
            [41, 185, 61, 223, 151, 151, 3, 247, 165, 156, 24, 17, 120, 120, 10, 5, 117, 67, 11, 214, 123, 42, 250, 161, 83, 212, 9, 84, 191, 89, 239, 34],
            [45, 200, 36, 251, 142, 79, 237, 233, 54, 46, 77, 138, 59, 208, 247, 222, 105, 218, 24, 34, 226, 113, 178, 208, 107, 179, 129, 32, 169, 126, 20, 130],
            [192, 207, 164, 226, 68, 163, 234, 238, 63, 62, 190, 127, 22, 11, 60, 17, 172, 253, 184, 141, 20, 217, 116, 10, 191, 37, 17, 204, 170, 133, 209, 160],
            [108, 100, 137, 59, 4, 201, 71, 78, 107, 2, 117, 71, 26, 224, 10, 23, 45, 194, 70, 34, 187, 46, 176, 11, 44, 75, 73, 108, 62, 70, 253, 174]]

def create_segment_vector(pattern, start_i, end_i, start_j, end_j, segment_name):
    segment = []
    for i in range(start_i, end_i):
        for j in range(start_j, end_j):
            segment.append(pattern[i][j])
    return segment

# Create segment vectors
segment_vectors = [
    create_segment_vector(pattern, i*4, (i+1)*4, j*4, (j+1)*4, f"segment_{i*8+j}")
    for i in range(4)
    for j in range(8)
]


motor_angle = 45
motor_speed = 150

def calculate_xor_checksum(bit2, bit3, bit4, bit5):
    return bit2 ^ bit3 ^ bit4 ^ bit5

def prepare_frame(bit2, bit3, bit4, bit5):
    checksum = calculate_xor_checksum(bit2, bit3, bit4, bit5)
    frame = bytearray([
        0x55,  # Start
        bit2,  # segment address
        bit3,  # motor address
        bit4,  # requested motor angle
        bit5,  # motor speed
        checksum,  # XOR checksum
        0xAA  # Stop
    ])
    return frame

def send_frames(segment_vectors, motor_angle, motor_speed):
    # Serial port configuration
    port = 'COM4'  # Change this to your serial port
    baudrate = 9600  # Change this to your baudrate

    # Initialize serial connection
    ser = serial.Serial(port, baudrate)
    time.sleep(2)  # Wait for the serial connection to initialize

    for i, segment in enumerate(segment_vectors):
        for value in segment:
            try:
                frame = prepare_frame(i, value, motor_angle, motor_speed)
                ser.write(frame)
                print(f"Sent frame for segment {i}, value {value}: {frame.hex().upper()}")
                time.sleep(0.001)  # Delay between sending frames
            except ValueError as e:
                print(f"Error preparing frame for segment {i}, value {value}: {e}")

    # Close serial connection
    ser.close()

# Send frames
send_frames(segment_vectors, motor_angle, motor_speed)