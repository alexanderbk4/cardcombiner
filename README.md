# Card Combiner

A Python script that combines front and back images of cards into a single side-by-side image.

## Installation

1. Clone the repository
2. Create a conda environment:
   ```bash
   conda create -n cardcombiner python=3.11
   conda activate cardcombiner
3. Install required packages 
   ```bash
   pip install -r requirements.txt

## Usage

1. Make sure conda environment is activated: 
   ```bash
   conda activate cardcombiner
2. Put labelled cards in root directory labelled in pairs as follows:
   front card: {title} F.jpg
   back card: {title} B.jpg
3. ```bash
   python src/combiner.py