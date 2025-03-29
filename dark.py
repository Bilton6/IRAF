#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 17:27:59 2025

@author: snehasish
"""

import os
import sys
import glob
from astropy.io import fits
from astropy.stats import mad_std
import ccdproc
import numpy

# Change the working directory to the current script's directory
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

root_directory = os.getcwd()
combined_dir = os.path.join(root_directory, "combined")

# Create the combined directory if it doesn't exist
if not os.path.isdir(combined_dir):
    os.makedirs(combined_dir)

# Find all files starting with 'Dark' in the current directory
dark_files = glob.glob(os.path.join(root_directory, "Dark*.fts"))
print("Found Dark files:", dark_files)

# Separate files by exposure time based on the filename
# Assuming the exposure time is indicated in the filename as '-150S' or '-300S'
dark_files_30 = [f for f in dark_files if "-030S" in os.path.basename(f)]
dark_files_150 = [f for f in dark_files if "-150S" in os.path.basename(f)]

print("Dark files with 30s exposure:", dark_files_30)
print("Dark files with 150s exposure:", dark_files_150)

# Combine Dark files with 300s exposure
if dark_files_30:
    combined_dark_30 = ccdproc.combine(
        dark_files_30,
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
    combined_dark_30_dir = os.path.join(combined_dir, "combined_dark_030s.fits")
    combined_dark_30.write(combined_dark_30_dir)

# Combine Dark files with 150s exposure
if dark_files_150:
    combined_dark_150 = ccdproc.combine(
        dark_files_150,
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
    combined_dark_150_dir = os.path.join(combined_dir, "combined_dark_150s.fits")
    combined_dark_150.write(combined_dark_150_dir)
