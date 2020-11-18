import wave

filename = 'contoh.wav'

# Set chunk size of 1024 samples per data frame
chunk = 1024  

# Open the sound file 
wf = wave.open(filename, 'rb')

g = wf.getnframes()
fr = wf.getframerate()
print(g / fr)
