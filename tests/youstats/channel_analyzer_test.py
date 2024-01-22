import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from src.youstats.channel_analyzer import ChannelAnalyzer, ChannelIsNone, DataFrameEmpty, DataFrameAssignment

TESTING_CHANNEL_NAME = '@MariusCiurea1'
SAMPLE_DATE_1 = '11/27/2021'
SAMPLE_DATE_2 = '02/02/2023'
SAMPLE_VIDEO_1 = 'http://video1'
SAMPLE_VIDEO_2 = 'http://video2'


class TestChannelAnalyzer(unittest.TestCase):
    """
    Unit tests for the ChannelAnalyzer class.
    """

    def setUp(self):
        """
        Set up a ChannelAnalyzer instance for testing.

        This method creates an instance of ChannelAnalyzer with a specified channel name for testing.
        """
        self.ca = ChannelAnalyzer(TESTING_CHANNEL_NAME)

    def tearDown(self):
        """
        Clean up resources after testing.

        This method is called after each test to clean up resources created during testing.
        """
        self.ca = None

    def test_channel_analyzer_initialization(self):
        """
        Check if the name and the driver of the channel analyzer are set up correctly.

        This test verifies that the channel name and the driver are initialized correctly during ChannelAnalyzer creation.
        """
        self.assertEqual(self.ca._channel_name, TESTING_CHANNEL_NAME)
        self.assertIsNotNone(self.ca.driver)

    # Property testing
    def test_channel_name_property_valid(self):
        """
        Retrieve channel name successfully.

        This test verifies that the channel_name property returns the expected channel name.
        """
        self.assertEqual(self.ca.channel_name, TESTING_CHANNEL_NAME)

    def test_channel_name_property_invalid(self):
        """
        Attempt to retrieve channel name with None value.

        This test checks if the ChannelIsNone exception is raised when attempting to retrieve channel name with None value.
        """
        self.ca._channel_name = None

        with self.assertRaises(ChannelIsNone):
            _ = self.ca.channel_name

    def test_general_info_dataframe_valid(self):
        """
        Retrieve general info DataFrame successfully.

        This test ensures that the general_info_dataframe property returns the expected DataFrame when it is not None.
        """
        self.ca._general_info_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        expected_general_info_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        pd.testing.assert_frame_equal(self.ca.general_info_dataframe, expected_general_info_dataframe)

    def test_general_info_dataframe_invalid(self):
        """
        Attempt to retrieve general info DataFrame with None value.

        This test checks if the DataFrameEmpty exception is raised when attempting to retrieve a None general_info_dataframe.
        """
        with self.assertRaises(DataFrameEmpty):
            _ = self.ca.general_info_dataframe

    def test_videos_info_dataframe_valid(self):
        """
        Retrieve videos information DataFrame successfully.

        This test ensures that the videos_info_dataframe property returns the expected DataFrame when it is not None.
        """
        self.ca._videos_info_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        expected_videos_info_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        pd.testing.assert_frame_equal(self.ca.videos_info_dataframe, expected_videos_info_dataframe)

    def test_videos_info_dataframe_invalid(self):
        """
        Attempt to retrieve videos information DataFrame with None value.

        This test checks if the DataFrameEmpty exception is raised when attempting to retrieve a None videos_info_dataframe.
        """
        with self.assertRaises(DataFrameEmpty):
            _ = self.ca.videos_info_dataframe

    def test_videos_statistic_dataframe_valid(self):
        """
        Retrieve videos statistics DataFrame successfully.

        This test ensures that the videos_statistic_dataframe property returns the expected DataFrame when it is not None.
        """
        self.ca._videos_statistic_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        expected_videos_statistic_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        pd.testing.assert_frame_equal(self.ca.videos_statistic_dataframe, expected_videos_statistic_dataframe)

    def test_videos_statistic_dataframe_invalid(self):
        """
        Attempt to retrieve videos statistics DataFrame with None value.

        This test checks if the DataFrameEmpty exception is raised when attempting to retrieve a None videos_statistic_dataframe.
        """
        with self.assertRaises(DataFrameEmpty):
            _ = self.ca.videos_statistic_dataframe

    def test_channel_name_setter_valid(self):
        """
        Set channel name successfully.

        This test verifies that the channel_name setter updates the channel name correctly when given a valid value.
        """
        new_channel_name = TESTING_CHANNEL_NAME
        self.ca.channel_name = new_channel_name
        self.assertEqual(self.ca._channel_name, new_channel_name)

    def test_channel_name_setter_invalid(self):
        """
        Attempt to set channel name with None value.

        This test checks if the ChannelIsNone exception is raised when attempting to set channel name to None.
        """
        with self.assertRaises(ChannelIsNone):
            self.ca.channel_name = None

    def test_general_info_dataframe_setter_valid(self):
        """
        Set general info DataFrame name successfully.

        This test ensures that the general_info_dataframe setter updates the general info DataFrame correctly when given a valid DataFrame.
        """
        testing_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        self.ca._general_info_dataframe = testing_dataframe
        pd.testing.assert_frame_equal(self.ca.general_info_dataframe, testing_dataframe)

    def test_general_info_dataframe_setter_invalid(self):
        """
        Attempt to set general info DataFrame with None value.

        This test checks if the DataFrameAssignment exception is raised when attempting to set general info DataFrame to None.
        """
        with self.assertRaises(DataFrameAssignment):
            self.ca.general_info_dataframe = None

    def test_videos_info_dataframe_setter_valid(self):
        """
        Set videos info DataFrame name successfully.

        This test ensures that the videos_info_dataframe setter updates the videos info DataFrame correctly when given a valid DataFrame.
        """
        testing_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        self.ca._videos_info_dataframe = testing_dataframe
        pd.testing.assert_frame_equal(self.ca.videos_info_dataframe, testing_dataframe)

    def test_videos_info_dataframe_setter_invalid(self):
        """
        Attempt to set videos info DataFrame with None value.

        This test checks if the DataFrameAssignment exception is raised when attempting to set videos info DataFrame to None.
        """
        with self.assertRaises(DataFrameAssignment):
            self.ca.videos_info_dataframe = None

    def test_videos_statistic_dataframe_setter_valid(self):
        """
        Set videos statistic DataFrame name successfully.

        This test ensures that the videos_statistic_dataframe setter updates the videos statistic DataFrame correctly when given a valid DataFrame.
        """
        testing_dataframe = pd.DataFrame({'TestColumn1': [1, 2, 3]})
        self.ca._videos_statistic_dataframe = testing_dataframe
        pd.testing.assert_frame_equal(self.ca.videos_statistic_dataframe, testing_dataframe)

    def test_videos_statistic_dataframe_setter_invalid(self):
        """
        Attempt to set videos statistic DataFrame with None value.

        This test checks if the DataFrameAssignment exception is raised when attempting to set videos statistic DataFrame to None.
        """
        with self.assertRaises(DataFrameAssignment):
            self.ca.videos_statistic_dataframe = None

    def test_convert_subs_or_videos_no_letter(self):
        """
        Retrieve the formatted number of subscribers.

        Note:
            Number of subscribers is clean.

        This test ensures that the _convert_subs_or_videos method correctly formats a clean number of subscribers.
        """
        num_of_subscribers = '235'
        retrieved_num_of_subscribers = self.ca._convert_subs_or_videos(num_of_subscribers)
        expected_num_of_subscribers = 235
        self.assertEqual(retrieved_num_of_subscribers, expected_num_of_subscribers)

    def test_convert_subs_or_videos_k(self):
        """
        Retrieve the formatted number of subscribers.

        Note:
            Number of subscribers contains the 'k' keyword.

        This test ensures that the _convert_subs_or_videos method correctly formats a number of subscribers with 'k'.
        """
        num_of_subscribers = '2.37K'
        retrieved_num_of_subscribers = self.ca._convert_subs_or_videos(num_of_subscribers)
        expected_num_of_subscribers = 237_000
        self.assertEqual(retrieved_num_of_subscribers, expected_num_of_subscribers)

    def test_convert_subs_or_videos_m(self):
        """
        Retrieve the formatted number of subscribers.

        Note:
            Number of subscribers contains the 'm' keyword.

        This test ensures that the _convert_subs_or_videos method correctly formats a number of subscribers with 'm'.
        """
        num_of_subscribers = '5.347M'
        retrieved_num_of_subscribers = self.ca._convert_subs_or_videos(num_of_subscribers)
        expected_num_of_subscribers = 5_347_000
        self.assertEqual(retrieved_num_of_subscribers, expected_num_of_subscribers)

    def test_format_views(self):
        """
        Retrieve the formatted number of views.

        This test ensures that the _format_views method correctly formats the number of views.
        """
        views_number = '3,130 views'
        retrieved_views_number = self.ca._format_views(views_number)
        expected_views_number = 3_130
        self.assertEqual(retrieved_views_number, expected_views_number)

    def test_convert_date_clean(self):
        """
        Retrieve the formatted date (USA format: MM/DD/YYYY).

        This test ensures that the _convert_date method correctly formats a clean date.
        """
        date = 'Nov 27, 2021'
        retrieved_date = self.ca._convert_date(date)
        self.assertEqual(retrieved_date, SAMPLE_DATE_1)

    def test_convert_date_premiered(self):
        """
        Retrieve the formatted date (USA format: MM/DD/YYYY).

        Note:
            Number of subscribers contains the 'Premiered' keyword.

        This test ensures that the _convert_date method correctly formats a date with 'Premiered'.
        """
        date = 'Premiered Nov 27, 2021'
        retrieved_date = self.ca._convert_date(date)
        self.assertEqual(retrieved_date, SAMPLE_DATE_1)

    def test_convert_date_joined(self):
        """
        Retrieve the formatted date (USA format: MM/DD/YYYY).

        Note:
            Number of subscribers contains the 'Joined' keyword.

        This test ensures that the _convert_date method correctly formats a date with 'Joined'.
        """
        date = 'Joined Nov 27, 2021'
        retrieved_date = self.ca._convert_date(date)
        self.assertEqual(retrieved_date, SAMPLE_DATE_1)

    @patch('src.youstats.channel_analyzer.webdriver.Chrome')
    def test_open_url(self, mock_driver):
        """
        Open an instance of Chrome and access the expected YouTube channel.

        This test ensures that the _open_url method correctly opens an instance of Chrome and accesses the expected YouTube channel URL.
        """
        self.ca.driver = mock_driver.return_value

        expected_url = f'https://www.youtube.com/{TESTING_CHANNEL_NAME}'
        self.ca._open_url()

        self.ca.driver.get.assert_called_once_with(expected_url)

    def test_update_dataframes(self):
        """
        Test updating general and videos DataFrames with mock data.

        This test verifies that the _update_dataframes method correctly updates the general and videos DataFrames with mock data.
        """
        ca = ChannelAnalyzer(TESTING_CHANNEL_NAME)
        ca._general_channel_info = [{'header_name': 'TestChannel',
                                     'subscribers_num': 1000,
                                     'videos_num': 10,
                                     'join_date': SAMPLE_DATE_1,
                                     'total_views': 100_000}]

        ca._all_videos_details = [
            {'title': 'Video1', 'views': 1000, 'date': SAMPLE_DATE_1, 'description': 'Description1',
             'link': SAMPLE_VIDEO_1},
            {'title': 'Video2', 'views': 2000, 'date': SAMPLE_DATE_2, 'description': 'Description2',
             'link': SAMPLE_VIDEO_2},
        ]

        ca._update_dataframes()

        self.assertEqual(ca._general_info_dataframe.to_dict(orient='records'), [{'header_name': 'TestChannel',
                                                                                 'subscribers_num': 1000,
                                                                                 'videos_num': 10,
                                                                                 'join_date': SAMPLE_DATE_1,
                                                                                 'total_views': 100_000}])

        self.assertEqual(ca._videos_info_dataframe.to_dict(orient='records'), [
            {'title': 'Video1', 'views': 1000, 'date': SAMPLE_DATE_1, 'description': 'Description1',
             'link': SAMPLE_VIDEO_1},
            {'title': 'Video2', 'views': 2000, 'date': SAMPLE_DATE_2, 'description': 'Description2',
             'link': SAMPLE_VIDEO_2},
        ])

    def test_extract_years_of_activity(self):
        """
        Test extracting years of activity from videos DataFrame.

        This test ensures that the _extract_years_of_activity method correctly extracts years of activity from the videos DataFrame.
        """
        ca = ChannelAnalyzer(TESTING_CHANNEL_NAME)
        ca._videos_info_dataframe = pd.DataFrame({
            'date': ['01/01/2022', '02/02/2022', '03/03/2023', '04/04/2023'],
        })

        ca._extract_years_of_activity()

        self.assertEqual(ca.years_of_activity, ['2022', '2023'])

    def test_harvest_data(self):
        """
        Test the entire harvesting process with mocked methods.

        This test verifies that the harvest_data method correctly performs the entire harvesting process with mocked methods.
        """
        ca = ChannelAnalyzer(TESTING_CHANNEL_NAME)

        ca._open_url = MagicMock()
        ca._access_youtube = MagicMock()
        ca._get_general_info = MagicMock()
        ca._find_all_videos_links = MagicMock()
        ca._find_videos_info = MagicMock()
        ca._update_dataframes = MagicMock()
        ca._extract_years_of_activity = MagicMock()

        ca.harvest_data()

        ca._open_url.assert_called_once()
        ca._access_youtube.assert_called_once()
        ca._get_general_info.assert_called_once()
        ca._find_all_videos_links.assert_called_once()
        ca._find_videos_info.assert_called_once()
        ca._update_dataframes.assert_called_once()
        ca._extract_years_of_activity.assert_called_once()

    def test_get_harvested_data(self):
        """
        Test retrieving harvested data from general and videos DataFrames.

        This test ensures that the get_harvested_data method correctly retrieves harvested data from the general and videos DataFrames.
        """
        ca = ChannelAnalyzer(TESTING_CHANNEL_NAME)
        ca._general_info_dataframe = pd.DataFrame({'header_name': ['TestChannel'],
                                                   'subscribers_num': [1000],
                                                   'videos_num': [10],
                                                   'join_date': [SAMPLE_DATE_1],
                                                   'total_views': [100_000]})

        ca._videos_info_dataframe = pd.DataFrame({'title': ['Video1'],
                                                  'views': [1000],
                                                  'date': [SAMPLE_DATE_1],
                                                  'description': ['Description1'],
                                                  'link': [SAMPLE_VIDEO_1]})

        general_df, videos_df, statistics_df = ca.get_harvested_data()

        self.assertTrue(general_df.equals(ca._general_info_dataframe))
        self.assertTrue(videos_df.equals(ca._videos_info_dataframe))

    if __name__ == '__main__':
        unittest.main()
