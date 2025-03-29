#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 13:49:24 2025

@author: snehasish
"""

import os
import glob
from astropy.io import fits
import matplotlib.pyplot as plt
from astropy.nddata import CCDData
from astropy.visualization import ZScaleInterval
import matplotlib


matplotlib.rc('xtick', labelsize=40)
matplotlib.rc('ytick', labelsize=40)
plt.rc('font', size=30)
plt.rc('axes', labelsize=55)

# Define the root directory and search pattern
root_directory = "."
sn_name = "SN2024ggi"  # Define the base name as a variable
science_files = glob.glob(os.path.join(root_directory, f"{sn_name}*.fts"))

# Loop through each science file
for science_file_name in science_files:
    print(f"Processing {science_file_name}...")

    try:
        # Extract the base name and filter type from the file name
        base_name = os.path.basename(science_file_name)
        filter_type = base_name.split('-')[2]  # Extract the filter type (e.g., 'ip')

        # Read the science image, specify the format explicitly as 'fits', and use ignore_missing_simple
        science = CCDData.read(science_file_name, unit="adu", format='fits', ignore_missing_simple=True)
        data = science.data

        # Get exposure time from the header
        exposure_time = science.header.get('EXPTIME', 'N/A')

        # Apply ZScaleInterval for better contrast
        interval = ZScaleInterval()
        vmin, vmax = interval.get_limits(data)

        # Plot the FITS data with adjusted contrast
        plt.figure(figsize=(20, 16))
        plt.imshow(data, cmap='gray', origin='lower', aspect='auto', vmin=vmin, vmax=vmax, interpolation='none')
        plt.title(f"Raw {sn_name} ({filter_type} filter)\nExposure Time: {exposure_time}s")
        plt.xlabel('X Pixel')
        plt.ylabel('Y Pixel')

        # Save the plot as a PDF file in the current directory
        pdf_file_name = base_name.replace(".fts", ".pdf")
        pdf_file_path = os.path.join(root_directory, pdf_file_name)  # Save in the current directory
        plt.savefig(pdf_file_path, format='pdf')
        plt.close()
        print(f"Saved {pdf_file_path}")

    except Exception as e:
        print(f"Error processing {science_file_name}: {e}")

print("-" * 40)
