import numpy as np
import sounddevice as sd

BIT_DURATION = 0.1
FREQ_0 = 1200
FREQ_1 = 2200
SAMPLE_RATE = 44100

PREAMBLE = "10101010" * 4

BUFFER_SIZE = int(SAMPLE_RATE * BIT_DURATION)

def detect_frequency(chunk):
    fft = np.fft.fft(chunk)
    freqs = np.fft.fftfreq(len(fft), 1 / SAMPLE_RATE)
    idx = np.argmax(np.abs(fft[:len(fft)//2]))
    return abs(freqs[idx])

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

print("Waiting for transmission... Press Ctrl+C to stop.\n")

bits = ""
phy_line = "PHY: "
bit_line = "BIT: "

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1) as stream:
        while True:
            chunk, _ = stream.read(BUFFER_SIZE)
            chunk = chunk.flatten()

            freq = detect_frequency(chunk)

            # Chunk separator
            phy_line += "|"
            bit_line += " "

            if abs(freq - FREQ_0) < 200:
                phy_line += "----"
                bits += "0"
                bit_line += "0"
            elif abs(freq - FREQ_1) < 200:
                phy_line += "++++"
                bits += "1"
                bit_line += "1"
            else:
                phy_line += "...."
                bit_line += "."

            print(phy_line)
            print(bit_line)
            print()

except KeyboardInterrupt:
    print("\nReception stopped.\n")

print("Raw received bits:")
print(bits)

print("\nSearching for preamble...")

start_index = bits.find(PREAMBLE)

if start_index == -1:
    print("Preamble not found.")
else:
    print("Preamble found.")
    data_start = start_index + len(PREAMBLE)
    data_bits = bits[data_start:]

    print("\nBits after preamble:")
    print(data_bits)

    print("\nDecoded text:")
    print(bits_to_text(data_bits))