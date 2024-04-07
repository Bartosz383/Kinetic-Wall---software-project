# Szkielet do przygotowywania ramek dla Arduino

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
        bit2,  # bit2
        bit3,  # bit3
        bit4,  # bit4
        bit5,  # bit5
        calculate_xor_checksum(bit2, bit3, bit4, bit5),  # XOR checksum
        0xAA  # Stop
    ])
    return frame

# Przykład użycia
try:
    bit2 = 10
    bit3 = 20
    bit4 = 30
    bit5 = 150
    bit6 = 100
    frame = prepare_frame(bit2, bit3, bit4, bit5, bit6)
    print("Prepared frame:", frame.hex().upper())
except ValueError as e:
    print("Error:", e)
