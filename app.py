#!/usr/bin/env python

# Author: Anna Grace Welch
# Date: 01/21/2026

# "This script contains a shiny application to calculate amount of cast-on stitches based on knitting gauge and pattern specifications."

# Imports 
#####################################################################################################################################################
from shiny.express import input, render, ui
from shiny import reactive
from knitting_functions import calculate_stitches, to_cm, calculate_new_bust_circumference, get_unique_colors, load_crochet_graph, image_to_grid, row_to_instruction, format_row
import matplotlib.pyplot as plt

# Functions
#####################################################################################################################################################
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# Style Set-Up
#####################################################################################################################################################
ui.page_opts(title="LoopLogic",
             fillable=True)

ui.tags.style("""
body {
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #f8f9fb;
}

.card {
    background: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.card-header {
    background: #4a6fa5 !important;
    color: white !important;
    font-weight: 600;
    border-radius: 10px 10px 0 0;
}

.result-box {
    font-size: 1.3em;
    font-weight: 600;
    margin-top: 15px;
    padding: 15px;
    background: #eef4ff;
    border-radius: 10px;
}

/* Default state for tab links */
.nav-link {
    color: #000000 !important; 
} 

/* Active/Selected tab */                 
.nav-link.active { 
    color: #FFFFFF !important; 
} 

/* Hover State */   
.nav-link:hover { 
    color: #3498db !important; 
}  
""")

# App
####################################################################################################################################################
# Centers the content on the page
with ui.div(style="max-width: 800px; margin: auto;"):

    with ui.navset_card_pill():
        
# ------------------------------- Page 1 --------------------------------------------------------------------------------------------------------------------------
        with ui.nav_panel("About / Help"):
            ui.markdown(
                """
                ### How this app works
                - Uses your actual stitch gauge
                - Calculates a new cast-on to hit your desired bust size

                    Happy knitting!
                """
            )

# ------------------------------- Page 2 --------------------------------------------------------------------------------------------------------------------------
        with ui.nav_panel("Cast-on Stitch Calculator"):

            with ui.card(style="max-width:850px; margin:auto;", class_="p-4"):

                ui.card_header("About the Cast-on Stitch Calculator")

                ui.markdown("""
                                This calculator computes the cast-on stitches needed to reach pattern gauge.  
                                It can also calculate stitches required to achieve a desired bust measurement.

                                ---
                                ## Required Inputs

                                ### Pattern Gauge
                                - Stitch gauge written in the pattern (stitches per 10 cm).

                                **Example:**  
                                17 sts × 26 rows = 10 × 10 cm → Input: **17**

                                ---

                                ### Your Gauge
                                - Stitch gauge measured from your knitted swatch **after** blocking.

                                **Example:**  
                                18 sts = 10 cm → Input: **18**

                                ---

                                ### Cast-On Stitches
                                - Number of stitches to cast on specified by the pattern.

                                **Example:**  
                                Pattern says cast on **92 stitches** → Input: **92**

                                ---
                                ## Optional Inputs

                                ### (Optional) Pattern Bust Circumference
                                - Finished garment bust size listed in the pattern.

                                **Example:**  
                                Size S = **113 cm** → Input: **113**

                                ---

                                ### (Optional) Desired Bust Circumference
                                - Target bust size for the finished garment.

                                **Example:**  
                                You want a bust circumference of **115 cm** instead of 113 cm → Input: **115**

                                This is an optional input because if your desired measurement matches another pattern size's dimensions, 
                                                knitting that size is usually simpler than making your own calculations. 

                                ---

                                Enter required values (and optional values if needed) to calculate your cast-on stitches.
            """)

            with ui.card():
                ui.card_header("Gauge")
                with ui.layout_columns():  
                    ui.input_numeric("expected_stitches", "Pattern gauge (sts / 10 cm)", 0)
                    ui.input_numeric("actual_stitches", "Your gauge (sts / 10 cm)", 0)

            with ui.card():
                ui.card_header("Pattern")
                ui.input_numeric("pattern_caston_sts", "Cast-on stitches", 0)

            with ui.card():
                ui.card_header("Optional Size Adjustment")
                with ui.layout_columns():
                    ui.input_numeric("expected_width", "Pattern bust circumference (optional)", value=None)
                    ui.input_numeric("desired_width", "Desired bust circumference (optional)", value=None)




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
                    v in (None, 0)
                    for v in [
                        input.expected_stitches(),
                        input.actual_stitches(),
                        input.pattern_caston_sts(),
                    ]
                ):
                    return "Enter pattern gauge, actual gauge, and pattern stitch count. Optionally, enter expected bust width \
                        based on pattern and the desired bust width of the garment."
                

                unit = input.unit()
                
                if input.expected_width not in (None, 0) and input.desired_width not in (None, 0):
                    expected_width_cm = to_cm(input.expected_width(), unit)
                    desired_width_cm = to_cm(input.desired_width(), unit)
                else:
                    expected_width_cm = desired_width_cm = None

                new_st_count = calculate_stitches(
                    input.expected_stitches(),
                    input.actual_stitches(),
                    input.pattern_caston_sts(),
                    expected_width_cm,
                    desired_width_cm,
                )
                return f'You should cast on {new_st_count} stitches.'

        
            
# ------------------------------- Page 3: Bust Circumference Calculator --------------------------------------------------------------------------------------------------------------------------
        with ui.nav_panel('Bust Circumference Calculator'):

            with ui.card(style="max-width:850px; margin:auto;", class_="p-4"):
                ui.card_header("About the Bust Circumference Calculator")

                ui.markdown("""
                                This calculator computes the bust circumference in cm of a finished garment if you knit with a different stitch gauge than the pattern gauge.  

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
                            
                                Enter required values to calculate the bust circumference of finished garment if knit with your stitch gauge.
                            """)

            with ui.card():
                ui.card_header("Inputs")
                ui.input_numeric("stitch_gauge", "Stitch gauge (stitches per 10 cm)", 0)
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

                return(f'Your garment would have a finished bust circumference of {new_bust_circumference} cm at this stitch gauge.')



# ------------------------------- Page 4: Crochet Graph --------------------------------------------------------------------------------------------------------------------------
# This page is an interactive interface where users can input a crochet colorwork grid, and it outputs the written instructions in the format:
    # Row 1: 2 white, 1 black, 2 white
    # Row 2: 3 white, 2 black, 3 white
# Every odd row is crocheted from left to right, and every even row is crocheted from right to left. 
        with ui.nav_panel('Crochet Graph'):
            with ui.card(style="max-width:850px; margin:auto;", class_="p-4"):
                ui.card_header("About the Bust Circumference Calculator")

                ui.markdown("""
                                This page creates written instructions from a crochet colorwork graph.  

                                ---
                                ## Required Inputs

                                ### Graph File Input
                                - Image file containing **only** your crochet graph in PNG format where one pixel = one stitch. 
                            
                                **Example input image:**""")

                ui.img(src="heart_grid.png", width='29px')
                        
                ui.markdown("""
                                This is best done by inputting your graph into the website StitchFiddle and utilizing the download to .png option.

                                **Tip:** Make sure that the colors on StitchFiddle match your expected colors and number of colors. If it is recognizing more colors than yarn colors you intend to use,
                                merge some colors before downloading the PNG file.
                                                    """)
            with ui.card():
                ui.card_header('Graph File Input')
                with ui.div(class_="d-flex justify-content-center align-items-center", style="height: 100%;"):
                    ui.input_file('graph', 'Input file containing crochet graph. Make sure there are no numbers numbering rows or columns and that the file only contains the grid of color.')

            def compute_grid():
                file = input.graph()
                if file is None:
                    return None

                image = load_crochet_graph(file[0]["datapath"])
                grid = image_to_grid(image)  # no rows/columns needed
                return grid

            @render.text
            def graph_input():
                if compute_grid() is None: 
                    return 'Please input a PNG file.'
                return "Graph loaded successfully."

            @render.ui
            def color_naming_ui():
                grid = compute_grid()
                if grid is None:
                    return

                colors = get_unique_colors(grid)  # reactive unique colors
                
                return ui.div(
                    *[
                        ui.div(
                            {
                                "style": "display:flex; align-items:center; gap:10px; margin-bottom:8px;"
                            },
                            ui.div({
                                "style": f"width:25px; height:25px; background:{rgb_to_hex(color)}; border:1px solid black;"
                            }),
                            ui.input_text(
                                f"color_{i}",
                                f"Color {i+1}",
                                value=f"color{i+1}"
                            )
                        )
                        for i, color in enumerate(colors)
                    ]
                )

            def get_color_map(colors):
                color_map = {}
                for i, color in enumerate(colors):
                    name = input[f"color_{i}"]()
                    color_map[tuple(color)] = name
                return color_map

            @render.ui
            def pattern_output():
                grid = compute_grid()
                if grid is None:
                    return
                
                colors = get_unique_colors(grid)
                color_map = get_color_map(colors)
                
                lines = []
                for i, row in enumerate(grid):
                    # zig-zag rows (even numbered rows go from right to left)
                    if i % 2 == 1:
                        row = row[::-1]

                    instr = row_to_instruction(row, color_map)
                    lines.append(format_row(i+1, instr))
                
                return ui.pre("\n".join(lines))