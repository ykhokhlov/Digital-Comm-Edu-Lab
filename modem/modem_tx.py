import numpy as np
import sounddevice as sd

BIT_DURATION = 0.1
FREQ_0 = 1200
FREQ_1 = 2200
SAMPLE_RATE = 44100

def text_to_bits(text):
    bits = ""
    for char in text:
        bits += format(ord(char), '08b')
    return bits

def generate_tone(freq, duration):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), endpoint=False)
    return 0.5 * np.sin(2 * np.pi * freq * t)

def bits_to_audio(bits):
    audio = np.array([])
    for bit in bits:
        if bit == '0':
            tone = generate_tone(FREQ_0, BIT_DURATION)
        else:
            tone = generate_tone(FREQ_1, BIT_DURATION)
        audio = np.concatenate((audio, tone))
    return audio

text = input("Введите сообщение: ")
bits = text_to_bits(text)

print("Биты:", bits)
print("Передача...")

audio_signal = bits_to_audio(bits)
sd.play(audio_signal, SAMPLE_RATE)
sd.wait()

print("Готово.")