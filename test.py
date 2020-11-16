import pyaudio
import wave

filename = 'helicopter.wav'

# Set chunk size of 1024 samples per data frame
chunk = 1024  

# Open the sound file 
wf = wave.open(filename, 'rb')

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)


data = wf.readframes(chunk)
# while data != b'':
#     stream.write(data)
#     data = wf.readframes(chunk)


# stream.close()
# p.terminate()