## 1.Introduction

This is the repo for the paper [Stylizing Audio Reactive Visuals](https://neurips2019creativity.github.io/doc/Stylizing%20Audio%20Reactive%20Visuals.pdf). Some of the code is modified from the official [StyleGAN](https://github.com/NVlabs/stylegan) repo.

## 2.Usage

### 2.1 Feature Extraction
```
python feature_extraction.py --bpm $bpm_of_music --path $path_to_mp3
```
This file extracts the low pass, band pass and high pass features from the song using filters.

### 2.2 Generating Images
```
cd resource
sh download.sh
```
Download the StyleGAN repo using the sh file located in the resource folder.
```
python gen_images.py --model_path $path_to_pretrained_model
```
Run the script and specify the pretrained model of StyleGAN you downloaded to generate the image files for the song. Modify the [style.yaml](style.yaml) file to change the mixing of style layers.

StyleGan Code, LSUN bedroom and celeba pretrained models:　
https://github.com/NVlabs/stylegan

Painting Pretrained Model:
https://www.reddit.com/r/MachineLearning/comments/bagnq6/p_stylegan_trained_on_paintings_512x512/
