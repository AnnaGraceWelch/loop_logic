#!/usr/bin/env python

# Author: Anna Grace Welch
# Date: 01/21/2026

"This script contains helpful functions when starting a knitting project....."

# Imports 
#####################################################################################################################################################
import argparse


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
    if expected_width != 0 and desired_width != 0:
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

    # Calculate new bust width
    return(total_bust_stitches/(stitch_gauge/10))



# def get_args():
#     parser = argparse.ArgumentParser(description = 'Module containing helpful functions for knitting or crochet projects.')
#     parser.add_argument('-w', )

    


# Main
#####################################################################################################################################################

def main():
    print(calculate_stitches(16, 10, 11, 68, 100, 102))






if __name__ == "__main__":
    main()