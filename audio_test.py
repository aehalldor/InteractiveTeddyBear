import numpy as np
import time
import sounddevice as sd

#duration = 10

def audio_callback (indata, frames, time, status):
	volume_norm = np.linalg.norm(indata) * 10
	vol = int(volume_norm)
	if vol > 50:
		print(volume_norm,"|" * int(volume_norm))
		#include interrupt
	
stream = sd.InputStream(callback=audio_callback)
with stream:
	while True:
		#sd.sleep(duration * 1000)
		time.sleep(1)
		
