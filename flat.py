#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 17:21:45 2025

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
combined_path = os.path.join(root_directory, "combined")

# Create the combined directory if it doesn't exist
if not os.path.isdir(combined_path):
    os.makedirs(combined_path)

# Find all files starting with 'AutoFlat' in the current directory
autoflat_files = glob.glob(os.path.join(root_directory, "AutoFlat*.fts"))
print("Found AutoFlat files:", autoflat_files)

# Define a function to scale the brightness of flats
def inv_median(a):
    return 20000 / numpy.median(a)  # Scale to 20000 ADU for ease of inspection

# Combine the selected AutoFlat files
combined_flat = ccdproc.combine(
    autoflat_files,
    unit="adu",
    method='median',
    scale=inv_median,
    sigma_clip=True,
    sigma_clip_low_thresh=3,
    sigma_clip_high_thresh=3,
    sigma_clip_func=numpy.ma.median,
    sigma_clip_dev_func=mad_std,
    mem_limit=350e6,
    dtype="float32"
)

# Clip flat values to prevent dividing by 0 or strange values
combined_flat.data = numpy.clip(combined_flat.data, 1, 65535)

# Save the combined flat to a FITS file
combined_flat_dir = os.path.join(
    combined_path,
    "combined_flat.fits"
)
combined_flat.write(combined_flat_dir)
