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
        with ui.nav_panel("Stitch Calculator"):

                # ui.input_numeric("expected_stitches", "Expected Gauge (Stitches per 10 cm)", 0)
                # ui.input_numeric("actual_stitches", "Actual Gauge (Stitches per 10 cm)", 0)
                # ui.input_numeric("pattern_caston_sts", "Number of Cast-on Stitches for Desired Pattern Size", 0)
                # ui.input_numeric("expected_width", "Expected Bust Width of Sweater based on Pattern", value=None)
                # ui.input_numeric("desired_width", "Desired Bust Width of Sweater", value=None)

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
                    ui.input_numeric("expected_width", "Pattern bust width (optional)", value=None)
                    ui.input_numeric("desired_width", "Desired bust width (optional)", value=None)




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

        
            
# ------------------------------- Page 3: Changed Bust Circumference --------------------------------------------------------------------------------------------------------------------------
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

                return(f'Your garment would have a finished bust circumference of {new_bust_circumference} cm at this stitch gauge.')



# ------------------------------- Page 4: Crochet Graph --------------------------------------------------------------------------------------------------------------------------
        # image = load_crochet_graph('/Users/annagracewelch/knitting_code/simple_graph.jpg')
        # grid = image_to_grid(image, 29, 29)
        with ui.nav_panel('Crochet Graph'):
            with ui.card():
                ui.card_header('Graph File Input')
                with ui.div(class_="d-flex justify-content-center align-items-center", style="height: 100%;"):
                    ui.input_file('graph', 'Input file containing crochet graph. Make sure there are no numbers numbering rows or columns and that the file only contains the grid of color.')
            with ui.card():
                ui.card_header('Dimensions')
                ui.input_numeric('rows', 'Input number of overall rows in graph.', 1)
                ui.input_numeric('columns', 'Input number of overall columns in graph.', 1)

            def compute_grid():
                file = input.graph()
                rows = input.rows()
                columns = input.columns()
                if file == None or rows == None or columns == None:
                    return None
                image = load_crochet_graph(file[0]["datapath"])
                return image_to_grid(image, rows, columns)
            
            @render.text
            def graph_input():
                if compute_grid() == None: 
                    return 'Please input file and dimensions.'
                return "Graph loaded successfully."
            

    
            @render.ui
            def color_naming_ui():
                grid = compute_grid()
                if grid == None:
                    return

                colors = get_unique_colors(grid)  # your reactive grid
                
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
                if grid == None:
                    return
                
                colors = get_unique_colors(grid)
                color_map = get_color_map(colors)
                
                lines = []
                
                for i, row in enumerate(grid):
                    # zig zag rows (even numbered rows go from right to left)
                    if i % 2 == 1:
                        row = row[::-1]

                    instr = row_to_instruction(row, color_map)
                    lines.append(format_row(i+1, instr))
                
                return ui.pre("\n".join(lines))