from scipy.io import wavfile
import numpy as np
fs, data = wavfile.read('audio.wav')
blankAudioLength = 10
blankAudio = np.zeros(int(blankAudioLength*fs),dtype=np.int16)
newAudio = np.hstack([blankAudio,data])
print(data.shape)
print(newAudio.shape)
wavfile.write("audio.wav",fs,newAudio)