# LoopLogic

<p align="center">
  <img src="Loop_Logic_large_logo.png" width="350">
</p>

<p align="center">
  <b>Algorithm-powered knitting & crochet pattern tools</b><br>
  Transform measurements, gauge, and design inputs into structured fiber-arts instructions.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Shiny-Python-blue">
  <img src="https://img.shields.io/badge/Open%20Source-Yes-brightgreen">
  <img src="https://img.shields.io/badge/Status-Active%20Development-orange">
</p>

## 🚀 Try LoopLogic Online

The application is deployed and available directly in your browser:

👉 **[Launch LoopLogic Web App](https://annagracewelch.github.io/loop_logic/)**


No installation required.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Knitting Tools](#knitting-tools)
  - [Cast-on Stitch Calculator](#cast-on-stitch-calculator)
  - [Bust Circumference Calculator](#bust-circumference-calculator)
- [Crochet Tools](#crochet-tools)
  - [Crochet Colorwork Grid Written Instructions Generator](#crochet-colorwork-grid-written-instruction-generator)

## Overview

LoopLogic is an open-source interactive web application built using **Shiny for Python** that helps knitters and crocheters translate measurements, gauge, and design inputs into structured pattern instructions.

The goal of this project is to combine computational algorithms with fiber arts workflows to streamline the crafting process and make pattern customization more accessible and reproducible. 
The application applies algorithmic scaling, data transformation, and structured instruction generation to automate tasks traditionally done manually by crafters.


##  Knitting Tools
### Cast-on Stitch Calculator
<details>
<summary><b>Explanation</b></summary>
This calculator calculates the cast-on stitches needed to reach desired pattern size if user's gauge differs from pattern gauge. This can often be useful in choosing which size to knit as well. If the user does not want to change needles to meet gauge, this can help them determine which size is closest to the correct measurements using their own stitch gauge instead.
</details>

<details>
<summary><b>Inputs</b></summary>

**Required Inputs:**
- Pattern Gauge
  - Stitch gauge specified by the pattern (stitches per 10 cm)
  - Example: 17 sts x 26 rows = 10 cm x 10 cm → Input: 17
- Your Stitch Gauge
  - Actual stitch gauge of knitted swatch **after** blocking
  - Example: 18 sts x 26 rows = 10 cm x 10 cm → Input: 18
- Cast-on Stitches
  - Amount of stitches the pattern says to cast on for desired garment size
  - Example: The patterns says to cast on 192 stitches for size S → Input: 192

**Optional Inputs:**
- Pattern bust circumference
  - Bust circumference of the finished garment for the desired size written in the pattern
  - Example: Size S has a finished bust circumference of 113 cm. → Input: 113

- Desired Bust Circumference
  - Bust circumference desired by the user for the finished garment
  - Example: The user wants the finished garment to have a bust circumference of 115 cm. → Input: 115
 
 If the user does not input pattern bust circumference and/or desired bust circumference, the calculator output the cast-on stitches needed to create a garment the same size of the pattern with the user's stitch gauge. 

 If the user does input these values, the calculator outputs the cast-on stitches needed to create a garment with the desired bust circumference and the user's stitch gauge. 

 </details>

 ### Bust Circumference Calculator
 <details>
<summary><b>Explanation</b></summary>
 This calculator computes the bust circumference of a finished garment based on the user's stitch gauge if it differs from the pattern gauge. 

 This is especially useful when deciding how far off sizing will be if you were to knit your garment with a different gauge, and to decide next steps based on this value.
</details>

<details>
<summary><b>Inputs</b></summary>

**Required Inputs:**
- Your Stitch Gauge
  - Actual stitches per 10 cm of blocked gauge swatch
  - Example: 18 sts per 10 cm → Input: 18
- Total stitches on needles at end of body increases
  - Total stitches around bust at the widest point of the pattern
  - Example: At the end of increases, the pattern says "There should 192 stitches on the needles." → Input: 192
</details>

## Crochet Tools

### Crochet Colorwork Grid Written Instruction Generator
<details>
<summary><b>Explanation</b></summary>
This generator creates written instructions from a crochet colorwork grid. The written instructions are written in the way you would crochet it meaning each odd row is written from left to right and each even row is written from right to left. 
</details>

<details>
<summary><b>Inputs</b></summary>

**Required Inputs:**
- Graph File Input
  - PNG file upload of crochet colorwork grid where one pixel = one stitch
  - Example: 
  ![heart_grid](www/heart_grid.png)

The easiest way of obtaining this required input in the correct format is by uploading or creating the colorwork grid in the online tool StitchFiddle and then downloading the file using the "download to PNG option" under the File tab. 
</details>