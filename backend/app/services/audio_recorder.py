import sounddevice as sd
from scipy.io.wavfile import write


def record_audio(filename="patient_voice.wav", duration=5, sample_rate=16000):

    print("Recording...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='int16'
    )

    sd.wait()
    

    write(filename, sample_rate, audio)

    # print("Audio saved!")

    return filename

record_audio()