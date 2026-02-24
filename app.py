#!/usr/bin/env python

# Author: Anna Grace Welch
# Date: 01/21/2026

# "This script contains a shiny application to calculate amount of cast-on stitches based on knitting gauge and pattern specifications."

# Imports 
#####################################################################################################################################################
from shiny.express import input, render, ui
from knitting_functions import calculate_stitches, to_cm, calculate_new_bust_circumference
import matplotlib.pyplot as plt

# Functions
#####################################################################################################################################################




# App
####################################################################################################################################################


ui.page_opts(title="Knitting Calculator")

ui.tags.style(
    "body { font-family: sans-serif; color: black}",
    ".card-header { color: white; background:black  !important; }",
    ".card { background: #ADD8E6; }"
    
)



with ui.navset_card_pill():
    # -------- Page 1 --------
    with ui.nav_panel("About / Help"):
        ui.markdown(
            """
            ### How this app works
            - Uses your actual stitch gauge
            - Calculates a new cast-on to hit your desired bust size

                Happy knitting!
            """
        )

    
    # -------- Page 2 --------
    with ui.nav_panel("Stitch Calculator"):

        # with ui.sidebar():
        ui.input_numeric("expected_stitches", "Expected Gauge (Stitches per 10 cm)", 0)
        ui.input_numeric("actual_stitches", "Actual Gauge (Stitches per 10 cm)", 0)
        ui.input_numeric("pattern_caston_sts", "Number of Cast-on Stitches for Desired Pattern Size", 0)
        ui.input_numeric("expected_width", "Expected Bust Width of Sweater based on Pattern", 0)
        ui.input_numeric("desired_width", "Desired Bust Width of Sweater", 0)


        ui.input_radio_buttons(
            "unit",
            "Width units",
            choices=["cm", "in"],
            selected="cm",
            inline=True,
        )

        @render.text
        def stitch_count():
            if any(
                v == 0
                for v in [
                    input.expected_stitches(),
                    input.actual_stitches(),
                    input.pattern_caston_sts(),
                    # input.expected_width(),
                    # input.desired_width(),
                ]
            ):
                return "Enter all values to calculate stitch count."

            unit = input.unit()

            expected_width_cm = to_cm(input.expected_width(), unit)
            desired_width_cm = to_cm(input.desired_width(), unit)

            new_st_count = calculate_stitches(
                input.expected_stitches(),
                input.actual_stitches(),
                input.pattern_caston_sts(),
                expected_width_cm,
                desired_width_cm,
            )

            return f"You should cast on {new_st_count} stitches."
    
    # -------- Page 3 --------
    with ui.nav_panel('Changed Bust Circumference'):
        ui.input_numeric("stitch_gauge", "Stitches per 10 cm", 0)
        ui.input_numeric("total_bust_stitches", "Total stitches around bust at widest point in pattern", 0)

        @render.text
        def new_bust_circumference():
            if any(
                v == 0
                for v in [
                    input.stitch_gauge(),
                    input.total_bust_stitches()
                ]
            ):
                return "Enter all values to calculate new bust circumference."
            
            new_bust_circumference = calculate_new_bust_circumference(
                input.stitch_gauge(),
                input.total_bust_stitches()
            )

            return(f'Your sweater would have a finished bust circumference of {new_bust_circumference} cm at this stitch gauge.')




# @render.plot
# def stitch_plot():
#     # Prevent plotting before inputs are filled
#     if any(
#         v == 0
#         for v in [
#             input.stitches(),
#             input.expect_cm(),
#             input.actual_cm(),
#             input.pattern_caston_sts(),
#             input.expected_width(),
#             input.desired_width(),
#         ]
#     ):
#         return

#     # Pattern values
#     pattern_width = input.expected_width()
#     pattern_sts = input.pattern_caston_sts()

#     # Desired values
#     desired_width = input.desired_width()
#     calculated_sts = calculate_stitches(
#         input.stitches(),
#         input.expect_cm(),
#         input.actual_cm(),
#         pattern_sts,
#         pattern_width,
#         desired_width,
#     )

#     fig, ax = plt.subplots()

#     # Line connecting pattern to desired
#     ax.plot(
#         [pattern_width, desired_width],
#         [pattern_sts, calculated_sts],
#         marker="o",
#     )

#     # Vertical reference lines
#     ax.axvline(pattern_width, linestyle="--")
#     ax.axvline(desired_width, linestyle="--")

#     # Labels
#     ax.set_xlabel("Bust Width")
#     ax.set_ylabel("Cast-on Stitches")
#     ax.set_title("Pattern vs Desired Sweater Width")

#     # Annotations (very knitter-friendly)
#     ax.annotate(
#         "Pattern",
#         (pattern_width, pattern_sts),
#         textcoords="offset points",
#         xytext=(5, 5),
#     )
#     ax.annotate(
#         "Desired",
#         (desired_width, calculated_sts),
#         textcoords="offset points",
#         xytext=(5, 5),
#     )

#     return fig


    