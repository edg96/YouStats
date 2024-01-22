import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from src.youstats.data_visualizer_views import DataVisualizerViews


VIEWS_PD_SERIES = pd.Series([100, 200, 300])
DATES_PD_SERIES = pd.Series(['01/15/2022', '02/20/2022', '03/25/2022'], name='date')


class TestDataVisualizerViews(unittest.TestCase):
    """
    Unit tests for the DataVisualizerViews class.
    """

    def setUp(self):
        """
        Initialize the pivot and targeted channels and create a DataVisualizerViews instance.

        This method sets up the necessary components for testing by creating instances of the pivot and targeted channels
        and a DataVisualizerViews instance.
        """
        self.pivot_channel = MagicMock()
        self.targeted_channel = MagicMock()

        self.data_visualizer_views = DataVisualizerViews(self.pivot_channel, self.targeted_channel)

    @patch('src.youstats.data_visualizer_views.DataVisualizer._generate_legend', return_value='Test Legend')
    def test_generate_legend(self, mock_generate_legend):
        """
        Retrieve the dates legend successfully from the inherited function.

        This test ensures that the _generate_legend method retrieves the expected dates legend.
        """
        test_data = {'01': 100, '02': 200, '03': 300}

        result = self.data_visualizer_views._generate_legend(test_data)

        mock_generate_legend.assert_called_once_with(test_data)
        self.assertEqual(result, 'Test Legend')

    def test_get_views(self):
        """
        Retrieve the views data successfully from the inherited function.

        This test ensures that the _get_views method retrieves the expected views data.
        """
        mock_data = {'views': VIEWS_PD_SERIES}
        self.pivot_channel.videos_info_dataframe = pd.DataFrame(mock_data)

        result = self.data_visualizer_views._get_views(self.pivot_channel)

        expected_result = pd.Series(VIEWS_PD_SERIES, name='views')

        pd.testing.assert_series_equal(result, expected_result)

    def test_get_dates(self):
        """
        Retrieve the dates data successfully from the inherited function.

        This test ensures that the _get_dates method retrieves the expected dates data.
        """
        mock_data = {'date': DATES_PD_SERIES}
        self.pivot_channel.videos_info_dataframe = pd.DataFrame(mock_data)

        result = self.data_visualizer_views._get_dates(self.pivot_channel)

        expected_result = DATES_PD_SERIES

        pd.testing.assert_series_equal(result, expected_result)

    @patch('src.youstats.data_visualizer_views.DataVisualizerViews._get_views')
    @patch('src.youstats.data_visualizer_views.DataVisualizerViews._get_dates')
    def test_get_views_per_year(self, mock_get_dates, mock_get_views):
        """
        Ensure that views data per year and month are retrieved successfully.

        This test verifies that the _get_views_per_year method retrieves the expected views data per year and month.
        """
        mock_get_views.return_value = VIEWS_PD_SERIES
        mock_get_dates.return_value = DATES_PD_SERIES

        result = self.data_visualizer_views._get_views_per_year(mock_get_views(), mock_get_dates())

        expected_result = {'2022': {'January': 100, 'February': 200, 'March': 300, 'April': 0, 'May': 0, 'June': 0,
                                    'July': 0, 'August': 0, 'September': 0, 'October': 0, 'November': 0, 'December': 0}}
        self.assertEqual(result, expected_result)

    @patch('src.youstats.data_visualizer_views.DataVisualizerViews._plot_views_single_channel')
    def test_show_single_channel_views(self, mock_plot_views_single_channel):
        """
        Ensure that views counts per year and month are calculated correctly based on views and posting dates.

        This test verifies that the show_single_channel_views method correctly calculates views counts per year and month
        based on views and posting dates.
        """
        pivot_channel_mock = MagicMock()
        self.data_visualizer_views._pivot_channel = pivot_channel_mock
        targeted_channel_mock = MagicMock()
        self.data_visualizer_views._targeted_channel = targeted_channel_mock

        self.data_visualizer_views.show_single_channel_views(True, True, ['2022'], 'ChannelName')

        mock_plot_views_single_channel.assert_called_with(
            self.data_visualizer_views, {}, ['2022'], 'ChannelName'
        )

    @patch('src.youstats.data_visualizer_views.DataVisualizerViews._plot_views_common_years')
    def test_show_common_years_views(self, mock_plot_views_common_years):
        """
        Ensure that views counts for common years are calculated correctly based on views and posting dates.

        This test verifies that the show_common_years_views method correctly calculates views counts for common years
        based on views and posting dates.
        """
        pivot_channel_mock = MagicMock()
        self.data_visualizer_views._pivot_channel = pivot_channel_mock
        targeted_channel_mock = MagicMock()
        self.data_visualizer_views._targeted_channel = targeted_channel_mock

        self.data_visualizer_views.show_common_years_views(['2022'])

        mock_plot_views_common_years.assert_called_with(
            self.data_visualizer_views, {}, {}, ['2022']
        )


if __name__ == '__main__':
    unittest.main()
