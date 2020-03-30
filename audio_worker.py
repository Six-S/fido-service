import os
import wave
import pyaudio

class Audio():
	
	def __init__(self):
		print('[INFO] We are spinning up our audio worker')
		self.chunk = 1024
		self.sample_format = pyaudio.paInt16
		self.channels = 1
		self.fs = 44100
		self.seconds = 3
		self.filename = "tmp/output.ogg"
		self.p = pyaudio.PyAudio()
		
		print(self.p.get_default_input_device_info())
	
	def handle_tmp(self):
		path = 'tmp'
		if not os.path.exists(path):
			print('[INFO] /tmp does not exist. Handling.')
			os.makedirs(path)
		else:
			print('[INFO] /tmp exists. Handling.')
			os.removedirs(path)
	
	def record(self):
		print('[INFO] Recording...')
		
		stream = self.p.open(
			format=self.sample_format,
			channels=self.channels,
			rate=self.fs,
			frames_per_buffer=self.chunk,
			input=True
		)
		
		audio_frames = []
		
		for i in range(0, int(self.fs / self.chunk * self.seconds)):
			data = stream.read(self.chunk, exception_on_overflow = False)
			audio_frames.append(data)
		
		stream.stop_stream()
		stream.close()
		
		self.save(audio_frames)
		
		self.kill_audio()
	
	def kill_audio(self):
		try:
			self.p.terminate()
			return True
		except:
			print('[WARN] An error occured attempting to kill our PortAudio Interface.')
			return False
	
	def save(self, audio_frames):
		print('[INFO] Saving recorded audio to file.')
		#self.handle_tmp()
		
		wf = wave.open(self.filename, 'wb')
		wf.setnchannels(self.channels)
		wf.setsampwidth(self.p.get_sample_size(self.sample_format))
		wf.setframerate(self.fs)
		wf.writeframes(b''.join(audio_frames))
		
if __name__ in "__main__":
	audio = Audio()
	audio.record()
