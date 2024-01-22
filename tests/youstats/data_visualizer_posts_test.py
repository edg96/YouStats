import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.youstats.data_visualizer_posts import DataVisualizerPosts

DATES_PD_SERIES = pd.Series(['01/15/2022', '02/20/2022', '03/25/2022'])


class TestDataVisualizerPosts(unittest.TestCase):
    """
    Unit tests for the DataVisualizerPosts class.
    """

    def setUp(self):
        """
        Initialize the pivot and targeted channels and create a DataVisualizerPosts instance.

        This method sets up the necessary components for testing by creating instances of the pivot and targeted channels
        and a DataVisualizerPosts instance.
        """
        self.pivot_channel = MagicMock()
        self.targeted_channel = MagicMock()

        self.data_visualizer_posts = DataVisualizerPosts(self.pivot_channel, self.targeted_channel)

    @patch('src.youstats.data_visualizer_posts.DataVisualizer._generate_legend', return_value='Test Legend')
    def test_generate_legend(self, mock_generate_legend):
        """
        Retrieve the dates legend successfully from the inherited function.

        This test verifies that the _generate_legend method retrieves the expected dates legend from the inherited function.
        """
        test_data = {'01': 100, '02': 200, '03': 300}

        result = self.data_visualizer_posts._generate_legend(test_data)

        mock_generate_legend.assert_called_once_with(test_data)
        self.assertEqual(result, 'Test Legend')

    def test_get_posting_dates(self):
        """
        Retrieve the dates legend successfully from the inherited function.

        This test ensures that the _get_posting_dates method retrieves the expected dates legend from the inherited function.
        """
        mock_data = {'date': DATES_PD_SERIES}
        self.pivot_channel.videos_info_dataframe = pd.DataFrame(mock_data)

        result = self.data_visualizer_posts._get_posting_dates(self.pivot_channel)

        expected_result = pd.Series(DATES_PD_SERIES, name='date')

        pd.testing.assert_series_equal(result, expected_result)

    @patch('src.youstats.data_visualizer_posts.DataVisualizerPosts._get_posting_dates')
    def test_get_posting_per_year(self, mock_get_posting_dates):
        """
        Ensure that posting dates are retrieved successfully from the pivot channel's video information dataframe.

        This test checks that the _get_posting_per_year method retrieves posting dates successfully from the pivot channel's
        video information dataframe.
        """
        mock_get_posting_dates.return_value = DATES_PD_SERIES

        result = self.data_visualizer_posts._get_posting_per_year(mock_get_posting_dates())

        expected_result = {'2022': {'January': 1, 'February': 1, 'March': 1, 'April': 0, 'May': 0, 'June': 0, 'July': 0,
                                    'August': 0, 'September': 0, 'October': 0, 'November': 0, 'December': 0}}
        self.assertEqual(result, expected_result)

    @patch('src.youstats.data_visualizer_posts.DataVisualizerPosts._plot_posting_single_channel')
    def test_show_single_channel_posting(self, mock_plot_posting_single_channel):
        """
        Ensure that posting counts per year and month are calculated correctly based on posting dates.

        This test checks that the show_single_channel_posting method calculates posting counts per year and month correctly
        based on posting dates.
        """
        pivot_channel_mock = MagicMock()
        self.data_visualizer_posts._pivot_channel = pivot_channel_mock
        targeted_channel_mock = MagicMock()
        self.data_visualizer_posts._targeted_channel = targeted_channel_mock

        self.data_visualizer_posts.show_single_channel_posting(True, True, ['2022'], 'ChannelName')

        mock_plot_posting_single_channel.assert_called_with(
            self.data_visualizer_posts, {}, ['2022'], 'ChannelName'
        )


if __name__ == '__main__':
    unittest.main()
