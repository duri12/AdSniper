import os
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


# format for more funcs -
# input - path to file
# output - path to new file
# all functions saves the files in the same place as the original file
# all conversions are to png
# note that in order to support the new funcs they must be added to CONVERSION in features.py

def gif2png(path):
    """"
    get a gif and convert it into png
    removes the gif
    input : path to gif
    output: path to png
    """
    img = Image.open(path)
    img.save(path.split(".")[0] + ".png", 'png', optimize=True, quality=70)
    os.remove(path)
    return path.split(".")[0] + ".png"


def jpeg2png(path):
    """
    convert a jpeg file format to gif file format
    convert jpeg to png
    input: path to jpeg
    """
    im1 = Image.open(path)
    im1.save(path.split(".")[0] + ".png")
    return path.split(".")[0] + ".png"


def svg2png(path, out_path):
    """"
    get a svg and convert it into png
    removes the svg
    input : path to svg
    output: path to png
    """
    drawing = svg2rlg(path)
    renderPM.drawToFile(drawing, out_path, fmt='PNG')
    os.remove(path)
    return path.split(".")[0] + ".png"
