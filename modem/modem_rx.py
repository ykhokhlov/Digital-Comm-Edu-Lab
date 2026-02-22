import numpy as np
import sounddevice as sd

BIT_DURATION = 0.1
FREQ_0 = 1200
FREQ_1 = 2200
SAMPLE_RATE = 44100

BUFFER_SIZE = int(SAMPLE_RATE * BIT_DURATION)

def detect_frequency(chunk):
    fft = np.fft.fft(chunk)
    freqs = np.fft.fftfreq(len(fft), 1/SAMPLE_RATE)
    idx = np.argmax(np.abs(fft[:len(fft)//2]))
    return abs(freqs[idx])

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

print("Ожидание передачи... Нажмите Ctrl+C для остановки.")

bits = ""

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1) as stream:
        while True:
            chunk, _ = stream.read(BUFFER_SIZE)
            chunk = chunk.flatten()

            freq = detect_frequency(chunk)

            if abs(freq - FREQ_0) < 200:
                bits += "0"
                print("0", end="", flush=True)
            elif abs(freq - FREQ_1) < 200:
                bits += "1"
                print("1", end="", flush=True)
            else:
                print(".", end="", flush=True)

except KeyboardInterrupt:
    print("\n\nПриём остановлен.")

print("\nПолученные биты:")
print(bits)

print("\nДекодированный текст:")
print(bits_to_text(bits))