#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 13:38:41 2025

@author: snehasish
"""

import os
import sys
import glob
from astropy.io import fits
from astropy.stats import mad_std
import ccdproc
import numpy

# BIAS COMBINE FOR MISMATCH BIAS FILES RESOLUTIONS

# Change the working directory to the current script's directory
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

root_directory = os.getcwd()
combined_path = os.path.join(root_directory, "combined")

# Create the combined directory if it doesn't exist
if not os.path.isdir(combined_path):
    os.makedirs(combined_path)

# Find all files starting with 'Bias' in the current directory
bias_files = glob.glob(os.path.join(root_directory, "Bias*.fts"))
print("Found bias files:", bias_files)

# Filter the bias files to only include those with size (1024, 1024)
valid_bias_files = []

for bias_file in bias_files:
    with fits.open(bias_file) as hdul:
        data = hdul[0].data
        if data.shape == (1024, 1024):  # Check if the shape is (1024, 1024)
            valid_bias_files.append(bias_file)

print("Valid bias files (1024x1024):", valid_bias_files)

# Combine the selected bias files
if valid_bias_files:  # Check if there are valid files to combine
    combined_bias = ccdproc.combine(
        valid_bias_files,
        unit="adu",
        method='average',
        sigma_clip=True,
        sigma_clip_low_thresh=3,
        sigma_clip_high_thresh=3,
        sigma_clip_func=numpy.ma.median,
        sigma_clip_dev_func=mad_std,
        mem_limit=350e6,
        dtype="float32"
    )

    # Save the combined bias to a FITS file
    combined_bias_dir = os.path.join(combined_path, "combined_bias.fits")
    combined_bias.write(combined_bias_dir)
    print(f"Combined bias saved to: {combined_bias_dir}")
else:
    print("No valid bias files found with shape (1024, 1024).")
