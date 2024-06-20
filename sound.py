import wave
import pyaudio
import numpy as np

from numpy import asanyarray

CHUNK = 1024


def play(file_name):
    """
    Format - poziom kwantyzajcji
    Channels - ilość kanałów
    Rate -
    """
    with (wave.open(file_name, 'rb')) as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        while len(data := wf.readframes(CHUNK)):
            stream.write(data)

        # print(snr(stream))

        stream.close()

        p.terminate()


def record(rate, format_size, length):
    rec_format = pyaudio.paInt16
    if format_size == '8':
        rec_format = pyaudio.paInt8

    with wave.open('music/record.wav', 'wb') as wb:
        p = pyaudio.PyAudio()

        stream = p.open(format=rec_format,
                        channels=2,
                        rate=rate,
                        frames_per_buffer=CHUNK,
                        input=True)

        frames = []
        print('recording...')
        for _ in range(0, int(rate/CHUNK * length)):
            data = stream.read(CHUNK)
            frames.append(data)


        stream.stop_stream()
        stream.close()

        p.terminate()

        print('recorded')

        wb.setnchannels(2)
        wb.setsampwidth(p.get_sample_size(rec_format))
        wb.setframerate(rate)
        wb.writeframes(b''.join(frames))
        wb.close()

        print('file written')
        print('snr value:')
        print(snr(b''.join(frames)))


def snr(data):
    data = np.frombuffer(data, dtype=np.int16)
    signal = np.mean(data**2)
    noise = np.var(data)

    if noise == 0:
        return float('inf')

    snr_value = 20 * np.log10(np.sqrt(signal / noise))
    return abs(snr_value)
