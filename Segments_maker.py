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
            [108, 100, 137, 59, 4, 201, 71, 78, 107, 2, 117, 71, 26, 224, 10, 23, 45, 194, 70, 34, 187, 46, 176, 11, 44, 75, 73, 108, 62, 70, 253, 174]
        ]


def create_segment_matrix(matrix_name, start_i, end_i, start_j, end_j, segment_name):
    segment = []

    for i in range(start_i, end_i):
        row = []
        for j in range(start_j, end_j):
            row.append(matrix_name[i][j])
        segment.append(row)

    # Wyświetlenie nowej macierzy segmentu
    print(f"Segment matrix {segment_name}:")
    for row in segment:
        print(row)

    return segment

def create_segment_vector(matrix_name, start_i, end_i, start_j, end_j, segment_name):
    segment = []

    for i in range(start_i, end_i):
        for j in range(start_j, end_j):
            segment.append(matrix_name[i][j])

    # Wyświetlenie nowego wektora segmentu
    # print(f"Segment {segment_name}:")
    # print(segment)

    return segment

# segment_0 = create_segment_matrix(pattern, 0, 4, 0, 4, "segment_0")
# segment_1 = create_segment_matrix(pattern, 0, 4, 4, 8, "segment_1")
# segment_2 = create_segment_matrix(pattern, 0, 4, 8, 12, "segment_2")
# segment_3 = create_segment_matrix(pattern, 0, 4, 12, 16, "segment_3")
# segment_4 = create_segment_matrix(pattern, 0, 4, 16, 20, "segment_4")
# segment_5 = create_segment_matrix(pattern, 0, 4, 20, 24, "segment_5")
# segment_6 = create_segment_matrix(pattern, 0, 4, 24, 28, "segment_6")
# segment_7 = create_segment_matrix(pattern, 0, 4, 28, 32, "segment_7")
# segment_8 = create_segment_matrix(pattern, 4, 8, 0, 4, "segment_8")
# segment_9 = create_segment_matrix(pattern, 4, 8, 4, 8, "segment_9")
# segment_10 = create_segment_matrix(pattern, 4, 8, 8, 12, "segment_10")
# segment_11 = create_segment_matrix(pattern, 4, 8, 12, 16, "segment_11")
# segment_12 = create_segment_matrix(pattern, 4, 8, 16, 20, "segment_12")
# segment_13 = create_segment_matrix(pattern, 4, 8, 20, 24, "segment_13")
# segment_14 = create_segment_matrix(pattern, 4, 8, 24, 28, "segment_14")
# segment_15 = create_segment_matrix(pattern, 4, 8, 28, 32, "segment_15")
# segment_16 = create_segment_matrix(pattern, 8, 12, 0, 4, "segment_16")
# segment_17 = create_segment_matrix(pattern, 8, 12, 4, 8, "segment_17")
# segment_18 = create_segment_matrix(pattern, 8, 12, 8, 12, "segment_18")
# segment_19 = create_segment_matrix(pattern, 8, 12, 12, 16, "segment_19")
# segment_20 = create_segment_matrix(pattern, 8, 12, 16, 20, "segment_20")
# segment_21 = create_segment_matrix(pattern, 8, 12, 20, 24, "segment_21")
# segment_22 = create_segment_matrix(pattern, 8, 12, 24, 28, "segment_22")
# segment_23 = create_segment_matrix(pattern, 8, 12, 28, 32, "segment_23")
# segment_24 = create_segment_matrix(pattern, 12, 16, 0, 4, "segment_24")
# segment_25 = create_segment_matrix(pattern, 12, 16, 4, 8, "segment_25")
# segment_26 = create_segment_matrix(pattern, 12, 16, 8, 12, "segment_26")
# segment_27 = create_segment_matrix(pattern, 12, 16, 12, 16, "segment_27")
# segment_28 = create_segment_matrix(pattern, 12, 16, 16, 20, "segment_28")
# segment_29 = create_segment_matrix(pattern, 12, 16, 20, 24, "segment_29")
# segment_30 = create_segment_matrix(pattern, 12, 16, 24, 28, "segment_30")
# segment_31 = create_segment_matrix(pattern, 12, 16, 28, 32, "segment_31")

v_segment_0 = create_segment_vector(pattern, 0, 4, 0, 4, 0)
v_segment_1 = create_segment_vector(pattern, 0, 4, 4, 8, 1)
v_segment_2 = create_segment_vector(pattern, 0, 4, 8, 12, 2)
v_segment_3 = create_segment_vector(pattern, 0, 4, 12, 16, 3)
v_segment_4 = create_segment_vector(pattern, 0, 4, 16, 20, 4)
v_segment_5 = create_segment_vector(pattern, 0, 4, 20, 24, 5)
v_segment_6 = create_segment_vector(pattern, 0, 4, 24, 28, 6)
v_segment_7 = create_segment_vector(pattern, 0, 4, 28, 32, 7)
v_segment_8 = create_segment_vector(pattern, 4, 8, 0, 4, 8)
v_segment_9 = create_segment_vector(pattern, 4, 8, 4, 8, 9)
v_segment_10 = create_segment_vector(pattern, 4, 8, 8, 12, 10)
v_segment_11 = create_segment_vector(pattern, 4, 8, 12, 16, 11)
v_segment_12 = create_segment_vector(pattern, 4, 8, 16, 20, 12)
v_segment_13 = create_segment_vector(pattern, 4, 8, 20, 24, 13)
v_segment_14 = create_segment_vector(pattern, 4, 8, 24, 28, 14)
v_segment_15 = create_segment_vector(pattern, 4, 8, 28, 32, 15)
v_segment_16 = create_segment_vector(pattern, 8, 12, 0, 4, 16)
v_segment_17 = create_segment_vector(pattern, 8, 12, 4, 8, 17)
v_segment_18 = create_segment_vector(pattern, 8, 12, 8, 12, 18)
v_segment_19 = create_segment_vector(pattern, 8, 12, 12, 16, 9)
v_segment_20 = create_segment_vector(pattern, 8, 12, 16, 20, 20)
v_segment_21 = create_segment_vector(pattern, 8, 12, 20, 24, 21)
v_segment_22 = create_segment_vector(pattern, 8, 12, 24, 28, 22)
v_segment_23 = create_segment_vector(pattern, 8, 12, 28, 32, 23)
v_segment_24 = create_segment_vector(pattern, 12, 16, 0, 4, 24)
v_segment_25 = create_segment_vector(pattern, 12, 16, 4, 8, 25)
v_segment_26 = create_segment_vector(pattern, 12, 16, 8, 12, 26)
v_segment_27 = create_segment_vector(pattern, 12, 16, 12, 16, 27)
v_segment_28 = create_segment_vector(pattern, 12, 16, 16, 20, 28)
v_segment_29 = create_segment_vector(pattern, 12, 16, 20, 24, 29)
v_segment_30 = create_segment_vector(pattern, 12, 16, 24, 28, 30)
v_segment_31 = create_segment_vector(pattern, 12, 16, 28, 32, 31)

# segments_vectors = [
#     create_segment_vector(pattern, 0, 4, j*4, (j+1)*4, f"segment_{i*8+j}") for i in range(4) for j in range(8)
# ]
#
# segments_vectors.append(create_segment_vector(pattern, 12, 16, 28, 32, "segment_31"))

# print(hex(v_segment_0[13]))


        # 0x55,  # Start
        # bit2,  # segment address
        # bit3,  # motor address
        # bit4,  # requested motor angle
        # bit5,  # motor speed
        # calculate_xor_checksum(bit2, bit3, bit4, bit5),  # XOR checksum
        # 0xAA  # Stop
# zrób ramkę z tego


motor_angle = 45
motor_speed = 150

def calculate_xor_checksum(bit2, bit3, bit4, bit5):
    bit6 = bit2 ^ bit3 ^ bit4 ^ bit5
    return bit6

def prepare_frame(bit2, bit3, bit4, bit5, bit6):
    # Sprawdzenie czy wartości mieszczą się w odpowiednich zakresach
    if not (0 <= bit2 <= 15):
        raise ValueError("bit2 must be in range 0-15")
    if not (0 <= bit3 <= 32):
        raise ValueError("bit3 must be in range 0-32")
    if not (-45 <= bit4 <= 45):
        raise ValueError("bit4 must be in range -45 to 45")
    if not (0 <= bit5 <= 255):
        raise ValueError("bit5 must be in range 0-255")

    # Przygotowanie ramki danych
    frame = bytearray([
        0x55,  # Start
        bit2,  # segment address
        bit3,  # motor address
        bit4,  # requested motor angle
        bit5,  # motor speed
        calculate_xor_checksum(bit2, bit3, bit4, bit5),  # XOR checksum
        0xAA  # Stop
    ])
    return frame

for value in range(16):  # od 0 do 16
    try:
        bit2 = 0
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_0[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 1
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_1[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 2
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_2[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 3
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_3[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 4
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_4[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 5
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_5[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 6
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_6[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 7
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_7[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 8
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_8[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 9
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_9[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 10
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_10[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 11
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_11[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 12
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_12[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 13
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_13[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 14
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_14[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)

for value in range(16):  # od 0 do 16
    try:
        bit2 = 15
        bit3 = value
        bit4 = motor_angle
        bit5 = motor_speed
        bit6 = calculate_xor_checksum
        frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
        print(f"Prepared frame for v_segment_15[0] = {value}:", frame.hex().upper())
    except ValueError as e:
        print("Error:", e)