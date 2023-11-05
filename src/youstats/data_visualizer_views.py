import calendar
import random
import time

import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import numpy as np
import pandas as pd

from src.youstats.channel_analyzer import ChannelAnalyzer
from src.youstats.data_visualizer import DataVisualizer, MONTHS_MAPPING


class DataVisualizerViews(DataVisualizer):
    """
    DataVisualizerViews is a subclass of DataVisualizer specialized for visualizing data related to
    views on YouTube channels.

    This class extends DataVisualizer to provide methods for visualizing the total views per
    month and per year
    for one or both YouTube channels. It works with instances of the ChannelAnalyzer class for
    pivot and targeted
    channels.
    """

    def __init__(self, pivot_channel: ChannelAnalyzer, targeted_channel: ChannelAnalyzer):
        """
        Initialize a DataVisualizerViews instance with pivot and targeted channels.

        Arguments:
            pivot_channel (ChannelAnalyzer): An instance of ChannelAnalyzer representing the
            pivot channel.
            targeted_channel (ChannelAnalyzer): An instance of ChannelAnalyzer representing
            the targeted channel.
        """
        super().__init__(pivot_channel, targeted_channel)

    @staticmethod
    def _get_views(channel: ChannelAnalyzer) -> pd.Series:
        """
        Retrieve the 'views' data from the videos information DataFrame of a YouTube channel.

        Parameters:
            channel (ChannelAnalyzer): An instance of the ChannelAnalyzer class containing the
            YouTube channel's details.

        Returns:
            pd.Series: The views data for each video.
        """
        return channel.videos_info_dataframe['views']

    @staticmethod
    def _get_dates(channel: ChannelAnalyzer) -> pd.Series:
        """
        Retrieve the 'views' data from the videos information DataFrame of a YouTube channel.

        Parameters:
            channel (ChannelAnalyzer): An instance of the ChannelAnalyzer class containing the
            YouTube channel's details.

        Returns:
            pd.Series: The views data for each video.
        """
        return channel.videos_info_dataframe['date']

    @staticmethod
    def _get_views_per_year(views_data: pd.Series, posting_data: pd.Series) -> dict:
        """
        Retrieve the views data from the videos information using Pandas Series.

        Parameters:
            views_data (pd.Series): A Pandas Series representing the views data of the videos.
            posting_data (pd.Series): A Pandas Series representing the posting dates of the videos.

        Returns:
            dict: A dictionary that stores the years as keys, and for each year, it stores another
            dictionary with months of the year as keys and the total views for each month as values.
        """
        accumulated_views = {}

        for i in range(len(views_data)):
            date = posting_data.iloc[i]
            view = views_data.iloc[i]
            year = date[-4:]
            month = MONTHS_MAPPING.get(date[0:2])

            if year not in accumulated_views:
                accumulated_views[year] = {month: 0 for month in MONTHS_MAPPING.values()}

            accumulated_views[year][month] += view

        return accumulated_views

    @staticmethod
    def _plot_views_single_channel(self, channel_data: dict[str, dict[str, int]], years_for_plotting: list[str],
                                   channel_name: str) -> None:
        """
        Plot the total views per month for a YouTube channel.

        Parameters:
            channel_data (dict[str, dict[str, int]): Views data for a channel, grouped
            by year and month.
            years_for_plotting (list[str]): List of year(s) for plotting.
            channel_name (str): Name of the channel.
        """
        channel_name = channel_name[1:]
        for year in years_for_plotting:
            months = list(MONTHS_MAPPING.values())
            channel_values = list(channel_data.get(year).values())

            legend_channel = self._generate_legend(channel_data[year])

            plt.figure(num=f'{channel_name}{calendar.timegm(time.gmtime())}{random.randint(0, 999)}')
            plt.plot(months, channel_values, marker='o', label=legend_channel)
            plt.title(f'{channel_name}: {year}: Videos views per month', fontsize=15)
            plt.xlabel('Months')
            plt.ylabel('Total Views')
            plt.grid()
            plt.legend()

        plt.show()

    @staticmethod
    def _plot_views_common_years(self, pivot_data: dict[str, dict[str, int]], targeted_data: dict[str, dict[str, int]],
                                 common_years: list[str]) -> None:
        """
        Plot the total views per month for the given years of two YouTube channels.

        Parameters:
            pivot_data (dict[str, dict[str, int]): Views data for the pivot channel, grouped by year and month.
            targeted_data (dict[str, dict[str, int]): Views data for the targeted channel, grouped by year and month.
            common_years (list[str]): List of years with data available for both channels.
        """
        for year in common_years:
            months = list(MONTHS_MAPPING.values())
            pivot_values = [pivot_data[year].get(month, 0) for month in months]
            targeted_values = [targeted_data[year].get(month, 0) for month in months]

            legend_pivot = self._generate_legend(pivot_data[year])
            legend_targeted = self._generate_legend(targeted_data[year])

            plt.figure(num=f'Common{calendar.timegm(time.gmtime())}{random.randint(0, 100)}')
            plt.plot(months, pivot_values, marker='o', label=legend_pivot)
            plt.plot(months, targeted_values, marker='o', label=legend_targeted)
            plt.title(f'Common: {year}: Videos posted per month', fontsize=15)
            plt.xlabel('Months')
            plt.ylabel('Total Views')

            y_max = max(max(pivot_values), max(targeted_values))
            y_ticks = np.arange(0, y_max + 1, y_max // 10)

            plt.yticks(y_ticks)

            plt.gca().yaxis.set_major_formatter(tck.FormatStrFormatter('%d'))
            plt.grid()
            plt.legend(ncol=2)

        plt.show()

    # Calling functions
    def show_common_years_views(self, common_years) -> None:
        """
        Visualize the total views per month by the pivot and targeted YouTube channels.

        Parameters:
            common_years (list[str]): List of common years for which views data will be visualized.
        """
        pivot_views = self._get_views(self._pivot_channel)
        pivot_posting_dates = self._get_dates(self._pivot_channel)
        targeted_views = self._get_views(self._targeted_channel)
        targeted_posting_dates = self._get_dates(self._targeted_channel)

        pivot_views_per_year = self._get_views_per_year(pivot_views, pivot_posting_dates)
        targeted_views_per_year = self._get_views_per_year(targeted_views, targeted_posting_dates)

        self._plot_views_common_years(self, pivot_views_per_year, targeted_views_per_year, common_years)

    def show_single_channel_views(self, pivot_channel: bool, targeted_channel: bool,
                                  years_for_plotting: list[str], channel_name: str) -> None:
        """
        Visualize the total views per month by the pivot and targeted YouTube channels.

        Parameters:
            pivot_channel (bool): Whether to visualize views data for the pivot channel.
            targeted_channel (bool): Whether to visualize views data for the targeted channel.
            years_for_plotting (list[str]): List of year(s) for which views data will be visualized.
            channel_name (str): Name of the channel.
        """
        if pivot_channel:
            pivot_views = self._get_views(self._pivot_channel)
            pivot_dates = self._get_dates(self._pivot_channel)
            pivot_views_per_year = self._get_views_per_year(pivot_views, pivot_dates)
            self._plot_views_single_channel(self, pivot_views_per_year, years_for_plotting, channel_name)

        if targeted_channel:
            targeted_views = self._get_views(self._targeted_channel)
            targeted_dates = self._get_dates(self._targeted_channel)
            targeted_views_per_year = self._get_views_per_year(targeted_views, targeted_dates)
            self._plot_views_single_channel(self, targeted_views_per_year, years_for_plotting, channel_name)
