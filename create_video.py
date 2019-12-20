import cv2
import numpy as np
import os
from os.path import isfile, join
from tqdm import tqdm
import argparse
import subprocess

import argparse

parser = argparse.ArgumentParser(description='Create Video from MP3 and Images')
parser.add_argument('--fps', default=40, type=int, help='Fps for video')
parser.add_argument('--path', default="./imgs", type=str, help='Image Folder')
parser.add_argument('--music', type=str, help='Music MP3 Location')
parser.add_argument('--output', default="output.mp4", type=str, help='Output File Name')
parser.add_argument('--resolution', default=512, type=int, help='Resolution of Video')
arguments = parser.parse_args()

pathIn = arguments.path
pathOut = 'video.avi'
fps = arguments.fps
frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

frame_array = []
files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f))]

files.sort(key = lambda x: x[5:-4])
for i in tqdm(range(len(files))):
    filename=pathIn + "{}.png".format(i)
    img = cv2.imread(filename)
    img = cv2.resize(img, (arguments.resolution, arguments.resolution))

    height, width, layers = img.shape
    size = (width,height)

    frame_array.append(img)
out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
for i in tqdm(range(len(frame_array))):
    out.write(frame_array[i])
out.release()

subprocess.call(['ffmpeg', '-i', pathOut, '-i', arguments.music, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', arguments.output])
