#!/usr/bin/env python

# Author: Anna Grace Welch
# Date: 01/21/2026

"This script contains helpful functions when starting a knitting project....."

# Imports 
#####################################################################################################################################################
import argparse
from PIL import Image
import numpy as np


# Functions
#####################################################################################################################################################
def calculate_stitches(expected_stitches: float,  actual_stitches: float, pattern_cast_on_stitches: int, expected_width=None, desired_width=None):
    '''This function takes expected stitches and expected cm for gauge, actual cm of knit gauge swatch, and the amount of cast-on stitches the original pattern
    says as input, and returns the required cast-on stitches to knit the same size using the new gauge.'''
    # Calculate length per stitch and divide total stitches by the gauge (expected stitches per cm) to get expected original width
    expected_gauge = expected_stitches/10
    width_of_expected_caston = (pattern_cast_on_stitches/expected_gauge)

    # If you also want to knit in between a size for width on a pattern
    # For example, you want sweater bust size to be 102 cm, but the pattern only has sizes for 100 and 110 cm
    if expected_width not in (None, 0) and desired_width not in (None, 0):
        adjusted_caston_stitches = (pattern_cast_on_stitches * desired_width) / expected_width
        width_of_expected_caston = (adjusted_caston_stitches/expected_gauge)

    
    # Calculate required stitches for the new gauge
    actual_gauge = actual_stitches/10
    new_caston = width_of_expected_caston * actual_gauge
    return round(new_caston)

def to_cm(value, unit):
    return value * 2.54 if unit == "in" else value

def calculate_new_bust_circumference(stitch_gauge: float, total_bust_stitches: int):
    '''
        This function takes user's stitch gauge and the total amount of bust stitches written in a sweater pattern as input, 
        and calculates the bust circumference of the finished sweater if the user knit that size of the pattern with their gauge.

        Inputs:
            * stitch_gauge: amount of stitches needed to reach 10 cm, can be a decimal (e.g. 16.5 stitches)
            * total_bust_stitches: number of stitches written in the pattern around the chest at the widest point (usually written after final
                body increase)
        Returns:
            circumference (in cm) of bust of finished sweater if user changes nothing about gauge (no needle change, size change, etc.)

    '''

    # Calculate new bust circumference
    return(total_bust_stitches/(stitch_gauge/10))
    

def load_crochet_graph(path):
    '''
    Load an image (PNG) where each pixel is a stitch.
    Returns a numpy array of RGB values.
    '''
    img = Image.open(path).convert("RGB")
    return np.array(img)

def image_to_grid(img):
    '''
    Convert the image array into a grid where each element is the simplified color of a pixel.
    '''
    h, w, _ = img.shape
    grid = []

    for r in range(h):
        row = []
        for c in range(w):
            color = simplify_color(tuple(img[r, c]))
            row.append(color)
        grid.append(row)
    
    return grid

def simplify_color(color, step=40):
    '''
    Reduce color variation to discrete steps for easier mapping to yarn colors.
    '''
    return tuple((c // step) * step for c in color)

def get_unique_colors(grid):
    unique = set()
    for row in grid:
        for color in row:
            unique.add(tuple(color))
    return sorted(list(unique))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def row_to_instruction(row, color_map):
    instructions = []
    current_color = row[0]
    count = 1

    for pixel in row[1:]:
        if pixel == current_color:
            count += 1
        else:
            instructions.append((count, color_map[current_color]))
            current_color = pixel
            count = 1

    instructions.append((count, color_map[current_color]))
    return instructions

def format_row(row_num, instruction):
    parts = [f"{count} {color}" for count, color in instruction]
    return f"Row {row_num}: " + ", ".join(parts)



    


# Main
#####################################################################################################################################################

def main():
    image = load_crochet_graph('/Users/annagracewelch/knitting_code/simple_graph.jpg')
    grid = image_to_grid(image, 29, 29)
    print(get_unique_colors(grid))






if __name__ == "__main__":
    main()