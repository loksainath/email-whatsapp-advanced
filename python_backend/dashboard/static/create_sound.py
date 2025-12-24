import wave
import struct
import math

sample_rate = 44100
duration = 0.3
frequency = 880
volume = 0.5

wav_file = wave.open("dashboard/sound.wav", "w")
wav_file.setnchannels(1)
wav_file.setsampwidth(2)
wav_file.setframerate(sample_rate)

for i in range(int(sample_rate * duration)):
    value = int(volume * 32767.0 * math.sin(2 * math.pi * frequency * i / sample_rate))
    data = struct.pack('<h', value)
    wav_file.writeframesraw(data)

wav_file.close()

print("sound.wav created")
