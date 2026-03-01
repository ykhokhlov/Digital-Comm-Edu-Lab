import numpy as np
import sounddevice as sd

BIT_DURATION = 0.1
FREQ_0 = 1200
FREQ_1 = 2200
SAMPLE_RATE = 44100

PREAMBLE = "10101010" * 4

BUFFER_SIZE = int(SAMPLE_RATE * BIT_DURATION)

SYMBOLS_PER_CHUNK = 4

def detect_frequency(chunk):
    fft = np.fft.fft(chunk)
    freqs = np.fft.fftfreq(len(fft), 1 / SAMPLE_RATE)
    idx = np.argmax(np.abs(fft[:len(fft)//2]))
    return abs(freqs[idx])

def classify_freq(freq):
    if abs(freq - FREQ_0) < 200:
        return '-', '0'
    elif abs(freq - FREQ_1) < 200:
        return '+', '1'
    else:
        return '.', None

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

            # PHY: split chunk into sub-parts, classify each independently
            sub_size = len(chunk) // SYMBOLS_PER_CHUNK
            phy_chars = []
            for i in range(SYMBOLS_PER_CHUNK):
                sub = chunk[i * sub_size:(i + 1) * sub_size]
                sym, _ = classify_freq(detect_frequency(sub))
                phy_chars.append(sym)
            phy_line += "|" + "".join(phy_chars)

            # BIT: decision from full chunk; 5 chars wide to match PHY slot
            _, bit = classify_freq(detect_frequency(chunk))
            bit_label = bit if bit else "."
            bit_line += "  " + bit_label + "  "

            if bit:
                bits += bit

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