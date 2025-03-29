#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 17:52:35 2025

@author: snehasish
"""

import os, sys
from astropy import units
from astropy.io import fits
from astropy.nddata import CCDData
import ccdproc
import numpy as np
import glob

# Set the working directory to the current directory
os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))

# Root directory
root_directory = os.path.dirname(os.path.realpath(sys.argv[0]))

# Path to the combined directory
combined_directory = os.path.join(root_directory, "combined")

# Path to the final directory where calibrated science frames will be stored
final_directory = os.path.join(root_directory, "final")
if not os.path.isdir(final_directory):  # Check if 'final' directory exists, if not, create it
    os.makedirs(final_directory)

# Read combined calibration frames
combined_bias_dir = os.path.join(combined_directory, "combined_bias.fits")
combined_dark_150s_dir = os.path.join(combined_directory, "combined_dark_150s.fits")
combined_dark_30s_dir = os.path.join(combined_directory, "combined_dark_030s.fits")
combined_flat_dir = os.path.join(combined_directory, "combined_flat.fits")

bias_combined = CCDData.read(combined_bias_dir, unit="adu")
dark_combined_150s = CCDData.read(combined_dark_150s_dir, unit="adu")
dark_combined_30s = CCDData.read(combined_dark_30s_dir, unit="adu")
flat_combined = CCDData.read(combined_flat_dir, unit="adu")

# Find all science frames starting with "SN2024xal" in the current directory
science_files = glob.glob(os.path.join(root_directory, "SN2024ggi*.fts"))

# Loop through each science file
for science_file_name in science_files:
    print(f"Processing {science_file_name}...")

    # Extract filter type from the file name (assumes the format: *-up_*, *-gp_*, etc.)
    filter_type = science_file_name.split('-')[2].split('_')[0]

    # Read the science image
    science = CCDData.read(science_file_name, unit="adu")

    # Get exposure time from the header (assuming the keyword is 'EXPTIME')
    exposure_time = science.header['EXPTIME']

    # Select the appropriate dark frame based on exposure time
    if exposure_time == 150:
        dark_combined = dark_combined_150s
    elif exposure_time == 30:
        dark_combined = dark_combined_30s
    else:
        raise ValueError(f"Unsupported exposure time: {exposure_time} seconds")

    # Apply calibration steps
    science_sub_bias = ccdproc.subtract_bias(science, bias_combined)
    science_sub_dark = ccdproc.subtract_dark(science_sub_bias, dark_combined, exposure_time='exptime', exposure_unit=units.second, scale=True)
    science_calibrated = ccdproc.flat_correct(science_sub_dark, flat_combined)

    # Convert data type to float32
    science_calibrated.data = science_calibrated.data.astype("float32")

    # Create a subdirectory for each filter in the 'final' directory if it doesn't exist
    filter_directory = os.path.join(final_directory, filter_type)
    if not os.path.isdir(filter_directory):
        os.makedirs(filter_directory)

    # Save the calibrated science image in the appropriate filter subdirectory
    final_science_file_name = "calibrated_" + os.path.basename(science_file_name)
    final_science_path = os.path.join(filter_directory, final_science_file_name)

    science_calibrated.write(final_science_path)

    # Optional: print confirmation message
    print(f"Calibrated science frame for filter {filter_type} saved to: {final_science_path}")
