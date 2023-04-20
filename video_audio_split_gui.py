import sys
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import *
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def split_audio_on_middle_silence(audio_file):
    audio = AudioSegment.from_file(audio_file)
    half_duration = len(audio) // 2
    search_duration = len(audio) // 10  # 以音频长度的10%作为搜索范围

    nonsilent_parts = detect_nonsilent(audio[half_duration - search_duration : half_duration + search_duration], 
                                       min_silence_len=500, silence_thresh=-40)

    if nonsilent_parts:
        middle_silence_start = nonsilent_parts[0][1] + half_duration - search_duration
        audio_part1 = audio[:middle_silence_start]
        audio_part2 = audio[middle_silence_start:]
    else:
        # 如果未检测到静音部分，将音频直接从中间分割
        audio_part1 = audio[:half_duration]
        audio_part2 = audio[half_duration:]

    return audio_part1, audio_part2

def main(file_path):
    if file_path.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
        audio_file = file_path
    else:
        video = VideoFileClip(file_path)
        audio = video.audio
        audio.write_audiofile("audio.wav")
        audio_file = "audio.wav"

    audio_part1, audio_part2 = split_audio_on_middle_silence(audio_file)
    audio_part1.export("audio_part1.wav", format="wav")
    audio_part2.export("audio_part2.wav", format="wav")
    
def open_file_dialog():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("Audio and Video files", "*.mp3;*.wav;*.m4a;*.flac;*.ogg;*.mp4;*.avi;*.mkv;*.mov;*.flv;*.wmv")])
    return file_path

if __name__ == "__main__":
    file_path = open_file_dialog()
    if file_path:
        main(file_path)
    else:
        print("No file selected.")
