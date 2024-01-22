import unittest
from unittest.mock import patch, MagicMock
from src.youstats.data_visualizer import DataVisualizer


class TestDataVisualizer(unittest.TestCase):
    """
    Unit tests for the DataVisualizer class.
    """

    def setUp(self):
        """
        Initialize the pivot and targeted channels and create a DataVisualizer instance.

        This method sets up the necessary components for testing by creating instances of the pivot and targeted channels
        and a DataVisualizer instance.
        """
        self.pivot_channel = MagicMock()
        self.targeted_channel = MagicMock()

        self.data_visualizer = DataVisualizer(self.pivot_channel, self.targeted_channel)

    def test_pivot_channel(self):
        """
        Retrieve pivot channel successfully.

        This test ensures that the pivot_channel property returns the expected pivot channel instance.
        """
        self.assertEqual(self.data_visualizer.pivot_channel, self.pivot_channel)

    def test_targeted_channel(self):
        """
        Retrieve targeted channel successfully.

        This test ensures that the targeted_channel property returns the expected targeted channel instance.
        """
        self.assertEqual(self.data_visualizer.targeted_channel, self.targeted_channel)

    @patch('src.youstats.data_visualizer.DataVisualizer._generate_legend', return_value='Test Legend')
    def test_generate_legend(self, mock_generate_legend):
        """
        Retrieve the dates legend successfully.

        This test verifies that the _generate_legend method retrieves the expected dates legend.
        """
        test_data = {'01': 100, '02': 200, '03': 300}

        result = self.data_visualizer._generate_legend(test_data)

        mock_generate_legend.assert_called_once_with(test_data)
        self.assertEqual(result, 'Test Legend')


if __name__ == '__main__':
    unittest.main()
