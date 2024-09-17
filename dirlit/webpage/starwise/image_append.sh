#!/bin/bash

# Placeholder for the image name
image_name1="MPA_lightcurve.png"
image_name2="MPA_phase_lc_1.png"

# Loop over each subdirectory
for dir in */; do
    # Remove the trailing slash to get the directory name
    dir_name="${dir%/}"

    # Paths to the two images with the same name in the subdirectory
    image1="${dir}${image_name1}"
    image2="${dir}${image_name2}"

    # Output file name
    output_file="star_${dir_name}_lc.png"

    # Append the two images vertically and save in the main directory
    convert "$image1" "$image2" -append "$output_file"
done

