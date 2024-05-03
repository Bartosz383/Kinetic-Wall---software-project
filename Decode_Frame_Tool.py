def decode_frame(frame):
    if len(frame) != 14:
        raise ValueError("Nieprawidłowa długość ramki")

    if frame[0:2] != "55":
        raise ValueError("Nieprawidłowy znacznik początkowy")

    if frame[12:] != "AA":
        raise ValueError("Nieprawidłowy znacznik końcowy")

    # Zdekoduj adres segmentu
    segment_address = int(frame[2:4], 16)

    # Zdekoduj adres silnika
    motor_address = int(frame[4:6], 16)

    # Zdekoduj żądany kąt
    angle = int(frame[6:8], 16)

    # Zdekoduj prędkość silnika
    motor_speed = int(frame[8:10], 16)

    # Oblicz sumę kontrolną
    checksum = int(frame[10:12], 16)
    checksum_check = segment_address ^ motor_address ^ angle ^ motor_speed

    if checksum_check != checksum:
        print("Błąd sumy kontrolnej")
    else:
        print("Suma kontrolna poprawna")

    print("Adres segmentu", segment_address)
    print("Adres silnika", motor_address)
    print("Kąt silnika", angle)
    print("Prędkość silnika", motor_speed)

    # return {
    #     "segment_address": segment_address,
    #     "engine_address": motor_address,
    #     "desired_angle": angle,
    #     "engine_speed": motor_speed,
    #     "checksum": checksum,
    #  }

def calculate_xor_checksum(bit2, bit3, bit4, bit5):
    print(bit2 ^ bit3 ^ bit4 ^ bit5)
    return bit2 ^ bit3 ^ bit4 ^ bit5

def prepare_frame(bit2, bit3, bit4, bit5):
    checksum = calculate_xor_checksum(bit2, bit3, bit4, bit5)
    frame = bytearray([
        0x55,  # Start
        bit2,  # segment address
        bit3,  # motor address (wartości od 0 do 15, iterowane w kółko)
        bit4,  # requested motor angle; value (segment)
        bit5,  # motor speed
        checksum,  # XOR checksum
        0xAA  # Stop
    ])

    print(frame)
    return frame

frame = "551F0FFF02EDAA"

decode_frame(frame)



# def decode_frame(frame):
#   """
#   Funkcja dekoduje ramkę hexadecymalną.
#
#   Argumenty:
#     frame: Ciąg znaków zawierający ramkę hexadecymalną.
#
#   Zwraca:
#     Słownik zawierający zdekodowane wartości pól ramki.
#   """
#
#   if len(frame) != 14:
#     raise ValueError("Nieprawidłowa długość ramki")
#
#   # Sprawdź znacznik początkowy
#   if frame[0:2] != "55":
#     raise ValueError("Nieprawidłowy znacznik początkowy")
#
#   # Zdekoduj adres segmentu
#   segment_address = int(frame[2:4], 16)
#
#   # Zdekoduj adres silnika
#   engine_address = int(frame[4:6], 16)
#
#   # Zdekoduj żądany kąt
#   desired_angle = int(frame[6:8], 16)
#
#   # Zdekoduj prędkość silnika
#   engine_speed = int(frame[8:10], 16)
#
#   # Oblicz sumę kontrolną
#   checksum = frame[10:12]
#   checksum_check = frame[2:4] ^ frame[4:6] ^ frame[6:8] ^ frame[8:10]
#
#   # Sprawdź sumę kontrolną
#   if checksum != int(frame[8:10], 16):
#     raise ValueError("Nieprawidłowa suma kontrolna")
#
#   # Sprawdź znacznik końcowy
#   if frame[10:] != "AA":
#     raise ValueError("Nieprawidłowy znacznik końcowy")
#
#   # Zwróć zdekodowane wartości
#   return {
#       "segment_address": segment_address,
#       "engine_address": engine_address,
#       "desired_angle": desired_angle,
#       "engine_speed": engine_speed,
#       "checksum": checksum,
#   }
#
# # Przykład użycia
# frame = "551F0FFF02EDAA"
#
# try:
#   decoded_frame = decode_frame(frame)
#   print(f"Zdekodowana ramka: {decoded_frame}")
# except ValueError as e:
#   print(f"Błąd: {e}")
