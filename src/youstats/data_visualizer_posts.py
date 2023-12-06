import calendar
import random
import time

import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import pandas as pd

from src.youstats.channel_analyzer import ChannelAnalyzer
from src.youstats.data_visualizer import DataVisualizer, MONTHS_MAPPING


class DataVisualizerPosts(DataVisualizer):
    """
    DataVisualizerPosts is a subclass of DataVisualizer specialized for visualizing data related to
    posting activities of YouTube channels.

    This class extends DataVisualizer to provide methods for visualizing the number of videos posted
    per month and per year for one or both YouTube channels.

    It works with instances of the ChannelAnalyzer class for pivot and targeted channels.
    """

    def __init__(self, pivot_channel: ChannelAnalyzer, targeted_channel: ChannelAnalyzer):
        """
        Initialize a DataVisualizerPosts instance with pivot and targeted channels.

        Params:
            pivot_channel (ChannelAnalyzer): An instance of ChannelAnalyzer representing the
            pivot channel.
            targeted_channel (ChannelAnalyzer): An instance of ChannelAnalyzer representing
            the targeted channel.
        """
        super().__init__(pivot_channel, targeted_channel)

    @staticmethod
    def _get_posting_dates(channel: ChannelAnalyzer) -> pd.Series:
        """
        Retrieve the 'date' data from the videos information DataFrame of a YouTube channel.

        Params:
            channel (ChannelAnalyzer): An instance of the ChannelAnalyzer class containing the
                YouTube channel's details.
        """
        return channel.videos_info_dataframe['date']

    @staticmethod
    def _get_posting_per_year(posting_dates: pd.Series) -> dict[str, dict[str, int]]:
        """
        Retrieve the 'date' data from the videos information DataFrame of a YouTube channel.

        Params:
            posting_dates (pd.Series): A Pandas Series representing the raw dates of the videos
                from the YouTube channel (MM/DD/YYYY).
        """
        yearly_data = {}

        for date in posting_dates:
            year = date[-4:]
            month = MONTHS_MAPPING.get(date[0:2])

            if year not in yearly_data:
                yearly_data[year] = {month: 0 for month in MONTHS_MAPPING.values()}

            yearly_data[year][month] += 1

        return yearly_data

    @staticmethod
    def _plot_posting_single_channel(self, channel_data: dict[str, dict[str, int]], years_for_plotting: list[str],
                                     channel_name: str) -> None:
        """
        Plot the number of videos posted through all years of activity for a YouTube channel.

        Params:
            channel_data (dict[str, dict[str, int]]): Video data for the YouTube channel, grouped
                by year and month.
            years_for_plotting (list[str]): List of years for plotting.
            channel_name (str): Name of the channel.
        """
        channel_name = channel_name[1:]
        for year in years_for_plotting:
            months = list(MONTHS_MAPPING.values())
            channel_values = list(channel_data.get(year).values())

            legend_channel = self._generate_legend(channel_data[year])

            plt.figure(num=f'{channel_name}{calendar.timegm(time.gmtime())}{random.randint(0, 999)}')
            plt.plot(months, channel_values, marker='o', label=legend_channel)
            plt.title(f'{channel_name}: {year}: Videos posted per month', fontsize=15)
            plt.xlabel('Months')
            plt.ylabel('Videos posted')

            y_ticks = range(max(channel_values) + 1)
            plt.yticks(y_ticks)

            plt.gca().yaxis.set_major_formatter(tck.FormatStrFormatter('%d'))
            plt.grid()
            plt.legend()

        plt.show()

    @staticmethod
    def _plot_posting_common_years(self, pivot_data: dict[str, dict[str, int]],
                                   targeted_data: dict[str, dict[str, int]], years_for_plotting: list[str]) -> None:
        """
        Plot the number of videos posted per month for the given years of two YouTube channels.

        Params:
            pivot_data (dict[str, dict[str, int]]): Video data for the pivot channel, grouped
                by year and month.
            targeted_data (dict[str, dict[str, int]]): Video data for the targeted channel, grouped
                by year and month.
            years_for_plotting (list[str]): List of year(s) for plotting.
        """
        for year in years_for_plotting:
            months = list(MONTHS_MAPPING.values())
            pivot_values = list(pivot_data.get(year).values())
            targeted_values = list(targeted_data.get(year).values())

            legend_pivot = self._generate_legend(pivot_data[year])
            legend_targeted = self._generate_legend(targeted_data[year])

            plt.figure(num=f'Common{calendar.timegm(time.gmtime())}{random.randint(0, 100)}')
            plt.plot(months, pivot_values, marker='o', label=legend_pivot)
            plt.plot(months, targeted_values, marker='o', label=legend_targeted)
            plt.title(f'Common: {year}: Videos posted per month', fontsize=15)
            plt.xlabel('Months')
            plt.ylabel('Videos posted')

            y_max = max(max(pivot_values), max(targeted_values))
            y_ticks = range(y_max + 1)
            plt.yticks(y_ticks)

            plt.gca().yaxis.set_major_formatter(tck.FormatStrFormatter('%d'))
            plt.grid()
            plt.legend(ncol=2)

        plt.show()

    # Calling functions
    def show_common_years_posting(self, common_years) -> None:
        """
        Visualize the number of videos posted per month by the pivot and targeted YouTube channels.

        Params:
            common_years (list[str]): List of common years for which posting data will be visualized.
        """
        pivot_posting_dates = self._get_posting_dates(self._pivot_channel)
        targeted_posting_dates = self._get_posting_dates(self._targeted_channel)

        pivot_posting_per_year = self._get_posting_per_year(pivot_posting_dates)
        targeted_posting_per_year = self._get_posting_per_year(targeted_posting_dates)

        self._plot_posting_common_years(self, pivot_posting_per_year, targeted_posting_per_year, common_years)

    def show_single_channel_posting(self, pivot_channel: bool, targeted_channel: bool, year_for_plotting: list[str],
                                    channel_name: str) -> None:
        """
        Visualize the number of videos posted per month by the pivot and targeted YouTube channels.

        Params:
            pivot_channel (bool): Whether to visualize posting data for the pivot channel.
            targeted_channel (bool): Whether to visualize posting data for the targeted channel.
            year_for_plotting (list[str]): The specific year for which posting data will be visualized.
            channel_name (str): Name of the channel.
        """
        if pivot_channel:
            pivot_posting_dates = self._get_posting_dates(self._pivot_channel)
            pivot_posting_per_year = self._get_posting_per_year(pivot_posting_dates)
            self._plot_posting_single_channel(self, pivot_posting_per_year, year_for_plotting, channel_name)

        if targeted_channel:
            target_posting_dates = self._get_posting_dates(self._targeted_channel)
            target_posting_per_year = self._get_posting_per_year(target_posting_dates)
            self._plot_posting_single_channel(self, target_posting_per_year, year_for_plotting, channel_name)
