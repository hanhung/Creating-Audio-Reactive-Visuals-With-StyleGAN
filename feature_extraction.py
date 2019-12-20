#Feature Extraction From MP3 File
import cv2
import numpy as np
import os
from os.path import isfile, join
from tqdm import tqdm
import argparse
import librosa
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

import argparse

parser = argparse.ArgumentParser(description='Feature Extraction From MP3')
parser.add_argument('--bpm', default=150, type=int, help='Input dir for videos')
parser.add_argument('--path', type=str, help='Output dir for image')
arguments = parser.parse_args()

out_dir = "./features/"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

y, sr = librosa.load(arguments.path)
set_frame_track = 1/(arguments.bpm*16/60)
frame_length = sr * set_frame_track

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#Low Pass Filter
fc = 150
w = fc / (sr / 2)
b, a = signal.butter(5, w, 'low')
lpf_y = signal.filtfilt(b, a, y)

librosa.output.write_wav(out_dir + 'lpf_y.wav', lpf_y, sr)
lpf_y, sr = librosa.load(out_dir + 'lpf_y.wav')

lpf_slice_track=librosa.util.frame(lpf_y, frame_length=int(frame_length), hop_length=int(frame_length))
lpf_y_rmse = librosa.feature.rms(lpf_y, frame_length=int(frame_length), hop_length=int(frame_length), center=True)
lpf_y_rmse = lpf_y_rmse[0,:]

np.save(out_dir + 'lpf_y_rmse.npy', lpf_y_rmse)
#------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#Band Pass Filter
fc = 350
w = fc / (sr / 2)
b, a = signal.butter(5, w, 'low')
bpf_y = signal.filtfilt(b, a, y)

fc = 200
w = fc / (sr / 2)
b, a = signal.butter(5, w, 'high')
bpf_y = signal.filtfilt(b, a, bpf_y)

librosa.output.write_wav(out_dir + 'bpf_y.wav', bpf_y, sr)
bpf_y, sr = librosa.load(out_dir + 'bpf_y.wav')

bpf_slice_track = librosa.util.frame(bpf_y, frame_length=int(frame_length), hop_length=int(frame_length))
bpf_y_rmse = librosa.feature.rms(bpf_y, frame_length=int(frame_length), hop_length=int(frame_length), center=True)
bpf_y_rmse=bpf_y_rmse[0,:]

np.save(out_dir + 'bpf_y_rmse.npy', bpf_y_rmse)
#------------------------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#High Pass Filter
fc = 5000
w = fc / (sr / 2)
b, a = signal.butter(5, w, 'low')
hpf_y = signal.filtfilt(b, a, y)

fc = 500
w = fc / (22050 / 2)
b, a = signal.butter(5, w, 'high')
hpf_y = signal.filtfilt(b, a, hpf_y)

librosa.output.write_wav(out_dir + 'hpf_y.wav', hpf_y, sr)
hpf_y, sr = librosa.load(out_dir + 'hpf_y.wav')

hpf_slice_track = librosa.util.frame(hpf_y, frame_length=int(frame_length), hop_length=int(frame_length))
hpf_y_rmse = librosa.feature.rms(hpf_y, frame_length=int(frame_length), hop_length=int(frame_length), center=True)
hpf_y_rmse = hpf_y_rmse[0,:]

np.save(out_dir + 'hpf_y_rmse.npy', hpf_y_rmse)
#------------------------------------------------------------------------------------------------------------------------------------------------------------
