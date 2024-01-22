__author__ = 'Dragos-Gabriel Enache'
__copyright__ = 'N/A'
__credits__ = ['N/A']

__license__ = 'N/A'
__version__ = "1.0.1"
__maintainer__ = 'Dragos-Gabriel Enache'
__email__ = 'edragosgabriel@gmail.com'
__status__ = 'Development temporary suspended. Unit tests are not finished.'

from youstats.youstats_window import YouStatsWindow

"""
================== Application description ==================

This module contains the main execution point of the application.
YouStats is an application containing two main components:
    - ChannelAnalyzer: A class responsible for analyzing a YouTube channel and collecting all the 
    the relevant information about the corresponding channel.
    - DataVisualizer: A class responsible for manipulating the data collected from the previous class
    (in form on DataFrames with very specific roles: general channel information, videos information 
    and statistics about the videos focused on the views section) and creating different graphs using 
    the Plotly library.

Notes:
    - ChannelAnalyzer should work only with the specified DataFrames that serve also as the sheets 
    of a generated CSV file that will log the information for future usage, but with the important 
    mention that the DataVisualizer class DO NOT need the CSV file to extract information from. 
    The CSV file is just for the user to use as it sees fit.
    - DataVisualizer must not collect data. All the required resources (the DataFrames specified 
    before) should be already provided for the class to manipulate in a graphical form of tables and 
    statistics.
    - Multiple instances of ChannelAnalyzer must be used for efficiency.
"""

if __name__ == '__main__':
    ys = YouStatsWindow()
    ys.mainloop()
