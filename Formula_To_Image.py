"""
Convert Formula String 

Author: Jameeehhhh
Date: 
Since: 30-7-2020
Version: 1.0
"""

import pylab

func = '2/3'


def text_to_fig(formula):

    fig = pylab.figure()
    text = fig.text(0, 0, formula)

    # Rendering text by saving image
    dpi = 300
    fig.savefig('formula.png', dpi=dpi)

    # Setting the sizes
    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.005
    # Figure size adjusted
    fig.set_size_inches((width, height))

    # Adjust text's vertical position.
    dy = (bbox.ymin/float(dpi))/height
    text.set_position((0, -dy))

    # Save adjusted and correct image.
    fig.savefig('formula.png', dpi=dpi)


text_to_fig(func)
