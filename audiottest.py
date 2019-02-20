import openal as al

for i in range(5):
    al.oalInit()
    source = al.oalOpen("audio.wav")

    source.play()
    while source.get_state() == al.AL_PLAYING:
        pass

    al.oalQuit()