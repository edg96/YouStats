from youstats.channel_analyzer import ChannelAnalyzer

MONTHS_MAPPING = {
    '01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May',
    '06': 'June', '07': 'July', '08': 'August', '09': 'September', '10': 'October',
    '11': 'November', '12': 'December'
}


class DataVisualizer:
    """
    DataVisualizer is a class that provides methods for visualizing data related to YouTube channels.

    This class is designed to work with two instances of the ChannelAnalyzer class:
        - one for a pivot channel
        - one for a targeted channel.

    It contains methods for generating legends, extracting common years, and other data
    visualization tasks.
    """

    def __init__(self, pivot_channel: ChannelAnalyzer, targeted_channel: ChannelAnalyzer):
        """
        Initialize a DataVisualizer instance with pivot and targeted channels.

        Arguments:
            pivot_channel (ChannelAnalyzer): An instance of ChannelAnalyzer representing
            the pivot channel.
            targeted_channel (ChannelAnalyzer): An instance of ChannelAnalyzer representing
            the targeted channel.
        """
        self._pivot_channel = pivot_channel
        self._targeted_channel = targeted_channel

    @property
    def pivot_channel(self):
        """
        Get the pivot channel's ChannelAnalyzer instance.

        Returns:
            ChannelAnalyzer: The ChannelAnalyzer instance for the pivot channel.
        """
        return self._pivot_channel

    @property
    def targeted_channel(self):
        """
        Get the targeted channel's ChannelAnalyzer instance.

        Returns:
            ChannelAnalyzer: The ChannelAnalyzer instance for the targeted channel.
        """
        return self._targeted_channel

    @staticmethod
    def _generate_legend(data: dict[str, int]) -> str:
        """
        Generate a legend from a data dictionary.

        Parameters:
            data (dict[str, int]): A dictionary containing month-value pairs.

        Returns:
            str: A formatted legend as a string.
        """
        return '\n'.join([f'{month}: {value}' for month, value in data.items()])
