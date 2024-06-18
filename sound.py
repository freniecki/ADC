import wave
import pyaudio

CHUNK = 1024


def play(file_name):
    with (wave.open(file_name, 'rb')) as wf:
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        while len(data := wf.readframes(CHUNK)):
            stream.write(data)

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
