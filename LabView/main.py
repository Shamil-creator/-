import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from matplotlib.animation import FuncAnimation


SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
DURATION = 5  
LOWCUT = 300.0
HIGHCUT = 3000.0
ORDER = 4
OUTPUT_FILE = "filtered_audio.wav"


is_recording = False
audio_buffer = np.array([])
filtered_buffer = np.array([])
b, a = signal.butter(ORDER, [LOWCUT/(0.5*SAMPLE_RATE), HIGHCUT/(0.5*SAMPLE_RATE)], btype='band')

def audio_callback(indata, frames, time, status):
    global audio_buffer, filtered_buffer
    if status:
        print(status)
    
    if is_recording:
        filtered = signal.lfilter(b, a, indata[:, 0])
        
        audio_buffer = np.append(audio_buffer, indata[:, 0])[-SAMPLE_RATE*DURATION:]
        filtered_buffer = np.append(filtered_buffer, filtered)[-SAMPLE_RATE*DURATION:]

def update_plot(frame):
    plt.clf()
    
    if len(audio_buffer) > 0:
        plt.subplot(2, 2, 1)
        plt.title('Исходный сигнал')
        plt.plot(audio_buffer)
        plt.ylim(-1, 1)
        
        plt.subplot(2, 2, 3)
        plt.title('Отфильтрованный сигнал')
        plt.plot(filtered_buffer)
        plt.ylim(-1, 1)
        
        N = len(audio_buffer)
        spectrum = np.abs(np.fft.rfft(audio_buffer))
        freqs = np.fft.rfftfreq(N, 1/SAMPLE_RATE)
        
        plt.subplot(2, 2, 2)
        plt.title('Спектр исходного сигнала')
        plt.plot(freqs, spectrum)
        plt.xlim(0, 5000)
        
        N_filt = len(filtered_buffer)
        spectrum_filt = np.abs(np.fft.rfft(filtered_buffer))
        freqs_filt = np.fft.rfftfreq(N_filt, 1/SAMPLE_RATE)
        
        plt.subplot(2, 2, 4)
        plt.title('Спектр отфильтрованного сигнала')
        plt.plot(freqs_filt, spectrum_filt)
        plt.xlim(0, 5000)
    
    plt.tight_layout()

def main():
    global is_recording
    
    plt.figure(figsize=(12, 8))
    plt.suptitle('Анализатор аудиосигналов (режим реального времени)')
    
    stream = sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=SAMPLE_RATE,
        blocksize=CHUNK_SIZE
    )
    
    print("Начало записи... (для остановки закройте окно графиков)")
    is_recording = True
    stream.start()
    
    ani = FuncAnimation(plt.gcf(), update_plot, interval=50)
    plt.show()
    
    is_recording = False
    stream.stop()
    stream.close()
    
    if len(filtered_buffer) > 0:
        wavfile.write(OUTPUT_FILE, SAMPLE_RATE, 
                     (filtered_buffer * 32767).astype(np.int16))
        print(f"Файл сохранён: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()