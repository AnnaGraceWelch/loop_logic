#!/usr/bin/env python

# Author: Anna Grace Welch
# Date: 01/21/2026

# "This script contains a Shiny for Python application to assist knitters and crocheters in the crafting process."

# Imports 
#####################################################################################################################################################
from shiny.express import input, render, ui
from shiny import reactive
from knitting_functions import calculate_stitches, to_cm, calculate_new_bust_circumference, \
get_unique_colors, load_crochet_graph, image_to_grid, row_to_instruction, format_row
import matplotlib.pyplot as plt
import shinyswatch

# Functions
#####################################################################################################################################################
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# Style Set-Up
#####################################################################################################################################################
ui.page_opts(title="LoopLogic", 
             theme=shinyswatch.theme.litera,
             navbar_options=ui.navbar_options(bg="primary"))

# ui.head_content(             
# ui.tags.style(
#     ""
#     ".navbar { background: navBarColor01; }" \
#     "")
# )


# ui.head_content(
#     ui.tags.style("""
#     body {
#         font-family: -apple-system, BlinkMacSystemFont, sans-serif;
#         background-color: #f8f9fb;
#     }
#     """)
# )

# .card {
#     background: white;
#     border-radius: 12px;
#     padding: 15px;
#     box-shadow: 0 4px 10px rgba(0,0,0,0.05);
# 
# .nav-tabs {
#     background: #4a6fa5 ;
#     border-radius: 12px;
#     padding: 15px;
#     box-shadow: 0 4px 10px rgba(0,0,0,0.05);
# }

# .card-header {
#     background: #4a6fa5 !important;
#     color: white !important;
#     font-weight: 600;
#     border-radius: 10px 10px 0 0;
# }

# .result-box {
#     font-size: 1.3em;
#     font-weight: 600;
#     margin-top: 15px;
#     padding: 15px;
#     background: #eef4ff;
#     border-radius: 10px;
# }

# /* Default state for tab links */
# .nav-link {
#     color: #000000 !important; 
# } 

# /* Active/Selected tab */                 
# .nav-link.active { 
#     color: #FFFFFF !important; 
# } 

# /* Hover State */   
# .nav-link:hover { 
#     color: #3498db !important; 
# }  
# """)

# App
####################################################################################################################################################     
# ------------------------------- Page 1: Welcome/About  --------------------------------------------------------------------------------------------------------------------------

with ui.nav_panel(title="Welcome"):
    ui.markdown(
        """
        ## 🧶 **Welcome to LoopLogic!** 🧶
        
        ### What is LoopLogic?
        - LoopLogic is an interactive application designed to aid kyounitters and crocheters in the crafting process.
            It includes helpful features such as stitch calculators and written instruction generators.
            The current features are detailed in the sections below. 
    

            Happy crafting! 😊

        ---

        ### Features:

        #### Cast-on Stitch Calculator
        - Calculates the cast-on stitches needed for garment to be a certain pattern size if user's gauge is different than pattern gauge.
        - Also has the option to calculate cast-on stitches is user desires a bust circumference different than the pattern's sizes.
            
        #### Bust Circumference Calculator
        - Calculates the bust circumference of a specific garment from a pattern based on user's stitch gauge. 
            
        #### Crochet Colorwork Grid Written Instruction Generator
        - Generates written instructions from a crochet colorwork grid                        


        """
    )

# ------------------------------- Page 2:  Cast-on Stitch Calculator --------------------------------------------------------------------------------------------------------------------------    

# Navigation panel containing calculator for adjusting
# cast-on stitches based on gauge differences and optional
# size modification.
with ui.nav_panel ("Knitting Tools"):
    with ui.navset_tab():
        with ui.nav_panel(title="Cast-on Stitch Calculator"):

            # Provides explanation of calculator purpose and required inputs
            with ui.card():

                ui.card_header("About the Cast-on Stitch Calculator")

                ui.markdown("""
                This calculator computes the cast-on stitches needed to
                reach pattern gauge and optionally adjust garment size.
            
                """)

            # User enters pattern gauge and personal swatch gauge
            with ui.card():
                ui.card_header("Gauge")

                # Display inputs side-by-side
                with ui.layout_columns():
                    ui.input_numeric(
                        "expected_stitches",
                        "Pattern gauge (sts / 10 cm)",
                        0
                    )
                    ui.input_numeric(
                        "actual_stitches",
                        "Your gauge (sts / 10 cm)",
                        0
                    )

            # Number of stitches specified by original pattern
            with ui.card():
                ui.card_header("Pattern")

                ui.input_numeric(
                    "pattern_caston_sts",
                    "Cast-on stitches",
                    0
                )


            # Allows resizing garment based on desired bust measurement
            with ui.card():
                ui.card_header("Optional Size Adjustment")

                with ui.layout_columns():
                    ui.input_numeric(
                        "expected_width",
                        "Pattern bust circumference (optional)",
                        value=None
                    )
                    ui.input_numeric(
                        "desired_width",
                        "Desired bust circumference (optional)",
                        value=None
                    )


            # Currently disabled — future support for inches/cm conversion
            # ui.input_radio_buttons(
            #     "unit",
            #     "Width units",
            #     choices=["cm", "in"],
            #     selected="cm",
            #     inline=True,
            # )

            # Reactive text output updating whenever inputs change
            @render.text
            def stitch_count():

                # Prevent calculation if required fields are empty or zero
                if any(
                    v in (None, 0)
                    for v in [
                        input.expected_stitches(),
                        input.actual_stitches(),
                        input.pattern_caston_sts(),
                    ]
                ):
                    return (
                        "Enter pattern gauge, actual gauge, and pattern stitch count. "
                        "Optionally, enter expected and desired bust measurements."
                    )

                # Currently assumes cm; conversion logic prepared for later
                unit = input.unit()

                # Convert widths to centimeters if optional inputs exist
                if (
                    input.expected_width not in (None, 0)
                    and input.desired_width not in (None, 0)
                ):
                    expected_width_cm = to_cm(input.expected_width(), unit)
                    desired_width_cm = to_cm(input.desired_width(), unit)
                else:
                    expected_width_cm = None
                    desired_width_cm = None


                # Computes adjusted cast-on stitch count
                new_st_count = calculate_stitches(
                    input.expected_stitches(),
                    input.actual_stitches(),
                    input.pattern_caston_sts(),
                    expected_width_cm,
                    desired_width_cm,
                )


                return f"You should cast on {new_st_count} stitches."

            
                
# ------------------------------- Page 3: Bust Circumference Calculator --------------------------------------------------------------------------------------------------------------------------
# Navigation panel for computing finished garment bust circumference
# when knitting with a different stitch gauge than the pattern gauge.
        with ui.nav_panel('Bust Circumference Calculator'):

            # Explains purpose and required inputs to the user
            with ui.card():
                ui.card_header("About the Bust Circumference Calculator")

                ui.markdown("""
                This calculator computes the bust circumference in cm of a finished garment
                if you knit with a different stitch gauge than the pattern gauge.

                ---
                ## Required Inputs

                ### Your Stitch Gauge
                - Stitch gauge of your knitted swatch **after** blocking.

                **Example:**  
                18 sts × 26 rows = 10 × 10 cm → Input: **18**

                ---

                ### Total stitches around bust at widest point in pattern
                - Stitches at the widest point of the pattern's body section after all increases.

                **Example:**  
                At the end of body increases, you should have **192 stitches** on the needles. → Input: **192**

                ---
                Enter required values to calculate the bust circumference of the finished garment
                if knit with your stitch gauge.
                """)


            # Collects user inputs for stitch gauge and total bust stitches
            with ui.card():
                ui.card_header("Inputs")

                # User enters their swatch stitch gauge
                ui.input_numeric(
                    "stitch_gauge",
                    "Stitch gauge (stitches per 10 cm)",
                    0
                )

                # User enters total stitches at the bust in the pattern
                ui.input_numeric(
                    "total_bust_stitches",
                    "Total stitches around bust at widest point in pattern",
                    0
                )


            @render.text
            def new_bust_circumference():

                # Return prompt if required values are missing or zero
                if any(
                    v == 0
                    for v in [
                        input.stitch_gauge(),
                        input.total_bust_stitches()
                    ]
                ):
                    return "Enter all values to calculate new bust circumference."


                # Compute new bust circumference based on user's stitch gauge
                new_bust_circumference = calculate_new_bust_circumference(
                    input.stitch_gauge(),
                    input.total_bust_stitches()
                )

                # Display result in cm with explanatory text
                return (
                    f'Your garment would have a finished bust circumference of '
                    f'{new_bust_circumference} cm at this stitch gauge.'
                )



# ------------------------------- Page 4: Crochet Colorwork Grid Written Instruction Generator --------------------------------------------------------------------------------------------------------------------------       
with ui.nav_panel("Crochet Tools"):
    with ui.navset_tab():
        # Navigation panel containing the crochet instruction generator
        with ui.nav_panel(title="Crochet Colorwork Grid Written Instruction Generator"):

            # --------------------------------------------------------
            # INFORMATION / ABOUT CARD
            # --------------------------------------------------------
            # Provides user instructions explaining required inputs
            with ui.card():
                ui.card_header("About the Written Instruction Generator")

                ui.markdown("""
                This page creates written instructions from a crochet colorwork graph.

                ---
                ## Required Inputs

                ### Graph File Input
                - Image file containing **only** your crochet graph in PNG format
                where one pixel = one stitch.

                **Example input image:**""")

                # Example image showing correct input format
                ui.img(src="heart_grid.png", width='29px')

                ui.markdown("""
                This is best done by inputting your graph into StitchFiddle
                and downloading the design as a PNG file.

                **Tip:** Ensure colors match intended yarn colors.
                Merge similar colors before exporting if needed.
                """)

            # --------------------------------------------------------
            # FILE INPUT CARD
            # --------------------------------------------------------
            # Allows user to upload crochet graph PNG
            with ui.card():
                ui.card_header('Graph File Input')

                # Center file upload widget
                with ui.div(
                    class_="d-flex justify-content-center align-items-center",
                    style="height: 100%;"
                ):
                    ui.input_file(
                        'graph',
                        'Input file containing crochet graph. '
                        'Image must contain only the grid (no numbering).'
                    )

            # --------------------------------------------------------
            # REACTIVE GRID COMPUTATION
            # --------------------------------------------------------
            # Converts uploaded PNG into a structured color grid
            # This function is called reactively whenever input.graph changes
            def compute_grid():
                file = input.graph()

                # No file uploaded yet
                if file is None:
                    return None

                # Load image as RGB array
                image = load_crochet_graph(file[0]["datapath"])

                # Convert pixels → stitch color grid
                grid = image_to_grid(image)

                return grid

            # --------------------------------------------------------
            # FILE STATUS MESSAGE
            # --------------------------------------------------------
            # Displays confirmation once graph loads successfully
            @render.text
            def graph_input():
                if compute_grid() is None:
                    return 'Please input a PNG file.'
                return "Graph loaded successfully."

            # --------------------------------------------------------
            # DYNAMIC COLOR NAMING UI
            # --------------------------------------------------------
            # Automatically generates text boxes allowing user
            # to assign yarn/color names to detected grid colors.
            @render.ui
            def color_naming_ui():

                grid = compute_grid()
                if grid is None:
                    return

                # Extract unique RGB colors from image
                colors = get_unique_colors(grid)

                # Create UI row for each detected color
                return ui.div(
                    *[
                        ui.div(
                            {
                                "style": (
                                    "display:flex; align-items:center;"
                                    " gap:10px; margin-bottom:8px;"
                                )
                            },

                            # Color preview square
                            ui.div({
                                "style": (
                                    f"width:25px; height:25px;"
                                    f" background:{rgb_to_hex(color)};"
                                    " border:1px solid black;"
                                )
                            }),

                            # User-entered yarn/color name
                            ui.input_text(
                                f"color_{i}",
                                f"Color {i+1}",
                                value=f"color{i+1}"
                            )
                        )
                        for i, color in enumerate(colors)
                    ]
                )

            # --------------------------------------------------------
            # BUILD COLOR MAP
            # --------------------------------------------------------
            # Creates mapping:
            # RGB color → user-defined color name
            def get_color_map(colors):

                color_map = {}

                for i, color in enumerate(colors):
                    name = input[f"color_{i}"]()
                    color_map[tuple(color)] = name

                return color_map

            # --------------------------------------------------------
            # PATTERN INSTRUCTION GENERATION
            # --------------------------------------------------------
            # Converts grid rows into written crochet instructions
            @render.ui
            def pattern_output():

                grid = compute_grid()
                if grid is None:
                    return

                colors = get_unique_colors(grid)
                color_map = get_color_map(colors)

                lines = []

                # Iterate through rows of stitches
                # Starting from bottom to top 
                for i, row in enumerate(grid[::-1]):

                    # Crochet is worked in rows:
                    # odd rows → left to right
                    # even rows → right to left
                    # (zig-zag / turning work)
                    if i % 2 == 1:
                        row = row[::-1]

                    # Convert row colors to instruction string
                    instr = row_to_instruction(row, color_map)

                    # Add formatted row label
                    lines.append(format_row(i + 1, instr))

                # Display instructions as preformatted text block
                return ui.pre("\n".join(lines))