#Code modified from https://github.com/NVlabs/stylegan/blob/master/pretrained_example.py

# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for generating an image using pre-trained StyleGAN generator."""

import os
import pickle
import numpy as np
import PIL.Image
import tensorflow as tf
from tqdm import tqdm

import sys
sys.path.append('resource/stylegan')
import dnnlib
import dnnlib.tflib as tflib

import yaml
import argparse

def get_rmse_feature(feature_path):
    return np.load(feature_path)

def load_model(model_path):
    with open(model_path, 'rb') as pickle_file:
        _G, _D, Gs = pickle.load(pickle_file)
    Gs.print_layers()
    return Gs

def get_randn(shape, seed=None):
    if seed:
        rnd = np.random.RandomState(seed)
        return rnd.randn(*shape)
    else:
        return np.random.randn(*shape)

def get_length(vec):
    return np.linalg.norm(vec)

def normalize_vec(vec, unit_length, factor_length):
    orig_length = get_length(vec)
    return vec * (unit_length / orig_length) * factor_length

def get_noise_vars(Gs):
    noise_vars = [var for name, var in Gs.components.synthesis.vars.items() if name.startswith('noise')]
    noise_pairs = list(zip(noise_vars, tflib.run(noise_vars)))
    return noise_vars

def move_vec(vec, unit_length, factor_length):
    direction_vec = get_randn(vec.shape)
    direction_vec = normalize_vec(direction_vec, unit_length, factor_length)
    return vec + direction_vec

def init_latents(Gs):
    latents = get_randn((1, Gs.input_shape[1]))
    noise_vars = get_noise_vars(Gs)
    noise_vectors = []
    for i in range(len(noise_vars)):
        noise_vectors.append(get_randn(noise_vars[i].shape))
    return latents, noise_vectors

def gen_image(Gs, latents, noise_vectors, noise_vars, fmt, save_path="example.png"):
    for i in range(len(noise_vars)):
        tflib.set_vars({noise_vars[i]: noise_vectors[i]})
    images = Gs.run(latents, None, truncation_psi=0.7, randomize_noise=False, output_transform=fmt)

    PIL.Image.fromarray(images[0], 'RGB').save(save_path)

def gen_image_mix(Gs, latents_high, latents_band, latents_low, noise_vectors, noise_vars, fmt, lpf, hpf, bpf, save_path="example.png"):
    for i in range(len(noise_vars)):
        tflib.set_vars({noise_vars[i]: noise_vectors[i]})

    high_latents = np.stack(latents_high)
    band_latents = np.stack(latents_band)
    low_latents = np.stack(latents_low)
    high_dlatents = Gs.components.mapping.run(high_latents, None)
    band_dlatents = Gs.components.mapping.run(band_latents, None)
    low_dlatents = Gs.components.mapping.run(low_latents, None)

    combined_dlatents = low_dlatents

    for style in lpf:
        combined_dlatents[:, style] = low_dlatents[:, style]

    for style in hpf:
        combined_dlatents[:, style] = high_dlatents[:, style]

    for style in bpf:
        combined_dlatents[:, style] = band_dlatents[:, style]

    # combined_dlatents = low_dlatents
    # combined_dlatents[:, 3:6] = high_dlatents[:, 3:6]
    # combined_dlatents[:, 6:] = band_dlatents[:, 6:]

    synthesis_kwargs = dict(output_transform=dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True), minibatch_size=8)
    images = Gs.components.synthesis.run(combined_dlatents, randomize_noise=False, **synthesis_kwargs)
    PIL.Image.fromarray(images[0], 'RGB').save(save_path)

def main():
    feature_folder = './features/'
    save_folder = 'imgs'

    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    parser = argparse.ArgumentParser(description='Generate Audio Reactive Images')
    parser.add_argument('--model_path', type=str, help='Path to Pretrained StyleGAN')
    arguments = parser.parse_args()

    tflib.init_tf()
    fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
    unit_length = 15

    high_pass_features = get_rmse_feature(feature_folder + "hpf_y_rmse.npy")
    band_pass_features = get_rmse_feature(feature_folder + "bpf_y_rmse.npy")
    low_pass_features = get_rmse_feature(feature_folder + "lpf_y_rmse.npy")

    diff_high_pass = (high_pass_features[1:] - high_pass_features[:-1])
    diff_high_pass = diff_high_pass / np.amax(diff_high_pass, axis=0)

    diff_band_pass = (band_pass_features[1:] - band_pass_features[:-1])
    diff_band_pass = diff_band_pass / np.amax(diff_band_pass, axis=0)

    diff_low_pass = (low_pass_features[1:] - low_pass_features[:-1])
    diff_low_pass = diff_low_pass / np.amax(diff_low_pass, axis=0)

    Gs = load_model(arguments.model_path)

    noise_vars = get_noise_vars(Gs)
    latents, noise_vectors = init_latents(Gs)

    latents_high = latents
    latents_band = latents
    latents_low = latents

    length_high = 10
    length_mid = 3
    length_low = 10

    with open('./style.yaml') as file:
        documents = yaml.full_load(file)
        lpf = documents['lpf']
        hpf = documents['hpf']
        bpf = documents['bpf']

    gen_image_mix(Gs, latents_high, latents_band, latents_low, noise_vectors, noise_vars, fmt, lpf, hpf, bpf,
                  save_path="./{}/{}.png".format(save_folder, 0))
    for i in tqdm(range(diff_low_pass.shape[0])):
        latents_high = move_vec(latents_high, length_high, diff_high_pass[i])
        latents_band = move_vec(latents_band, length_mid, diff_band_pass[i])
        latents_low = move_vec(latents_low, length_low, diff_low_pass[i])

        gen_image_mix(Gs, latents_high, latents_band, latents_low, noise_vectors, noise_vars, fmt, lpf, hpf, bpf,
                      save_path="./{}/{}.png".format(save_folder, i))

if __name__ == "__main__":
    main()
