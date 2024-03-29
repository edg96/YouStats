import os
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

SITE = 'https://www.youtube.com'
SYS_DESKTOP_PATH = os.path.join(os.path.expanduser('~/Desktop'))


class ChannelIsNone(Exception):
    """Custom exception for a None channel attribute."""
    def __init__(self, message='Channel is None. It needs a value to serve as a target.'):
        super().__init__(message)


class DataFrameEmpty(Exception):
    """Custom exception for a None DataFrame."""
    def __init__(self, message='DataFrame is None. Analyze a channel to provide data for the DataFrame.'):
        super().__init__(message)


class DataFrameAssignment(Exception):
    """Custom exception for assigning a non-DataFrame object."""
    def __init__(self, message='The provided object for assignment is not a DataFrame'):
        super().__init__(message)


class ChannelAnalyzer:
    """
    The ChannelAnalyzer class is responsible for opening Chrome, accepting the cookie policy and
    collecting the following information from a YouTube channel:
        - general information: number of subscribers, number of videos, information from about
        section etc.
        - information from each video: description, number of views, post day, video link

    Attributes:
        self._channel_name (str): The name of the targeted YouTube channel.
        self.url (str): The URL of the targeted YouTube channel.
        self._general_channel_info (list[dict]): A list to store general channel information.
        self._links_of_all_videos (list[str]): A list to store links to all videos on the channel.
        self._all_videos_details (list[dict]): A list to store details of each video on the channel.
    """
    _general_info_dataframe = None
    _videos_info_dataframe = None
    _videos_statistic_dataframe = None

    def __init__(self, target: str):
        """
        Initialize a ChannelAnalyzer instance with a target channel name.

        Params:
            target (str): The name of the targeted YouTube channel.
        """
        self._channel_name = target
        self.url = f'{SITE}/{target}'
        self._general_channel_info = []
        self._links_of_all_videos = []
        self._all_videos_details = []
        self.years_of_activity = []
        self.chrome_options = Options()
        self.chrome_options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    @property
    def channel_name(self) -> str:
        """
        The property for accessing the channel name.

        Raises:
            ChannelIsNone - If the channel name is None, it raises an exception.
        """
        if self._channel_name is None:
            raise ChannelIsNone()
        return self._channel_name

    @property
    def general_info_dataframe(self) -> pd.DataFrame:
        """
        The property for accessing the general information DataFrame.

        Raises:
            DataFrameEmpty - If the DataFrame is None, it raises an exception.
        """
        if self._general_info_dataframe is None:
            raise DataFrameEmpty()
        return self._general_info_dataframe.copy()

    @property
    def videos_info_dataframe(self) -> pd.DataFrame:
        """
        The property for accessing the videos information DataFrame.

        Raises:
            DataFrameEmpty - If the DataFrame is None, it raises an exception.
        """
        if self._videos_info_dataframe is None:
            raise DataFrameEmpty()
        return self._videos_info_dataframe.copy()

    @property
    def videos_statistic_dataframe(self) -> pd.DataFrame:
        """
        The property for accessing the videos statistic DataFrame.

        Raises:
            DataFrameEmpty - If the DataFrame is None, it raises an exception.
        """
        if self._videos_statistic_dataframe is None:
            raise DataFrameEmpty()
        return self._videos_statistic_dataframe.copy()

    @channel_name.setter
    def channel_name(self, channel_name):
        """
        The setter for the channel name property. It allows setting a new channel name.

        Params:
            channel_name (str): The new channel name.

        Raises:
            ChannelIsNone - If the provided channel name is None, it raises an exception.
        """
        if channel_name is None:
            raise ChannelIsNone()
        self._channel_name = channel_name

    @general_info_dataframe.setter
    def general_info_dataframe(self, general_info_dataframe):
        """
        The setter for the general information DataFrame property. It allows updating the DataFrame.

        Params:
            general_info_dataframe (pd.DataFrame): The new general information DataFrame.

        Raises:
            DataFrameAssignment - If the provided object is not a DataFrame, it raises an exception.
        """
        if not isinstance(general_info_dataframe, pd.DataFrame):
            raise DataFrameAssignment()
        self._general_info_dataframe = general_info_dataframe

    @videos_info_dataframe.setter
    def videos_info_dataframe(self, videos_info_dataframe):
        """
        The setter for the videos information DataFrame property. It allows updating the DataFrame.

        Params:
            videos_info_dataframe (pd.DataFrame): The new videos information DataFrame.

        Raises:
            DataFrameAssignment - If the provided object is not a DataFrame, it raises an exception.
        """
        if not isinstance(videos_info_dataframe, pd.DataFrame):
            raise DataFrameAssignment()
        self._videos_info_dataframe = videos_info_dataframe

    @videos_statistic_dataframe.setter
    def videos_statistic_dataframe(self, videos_statistic_info):
        """
        The setter for the videos statistic DataFrame property. It allows updating the DataFrame.

        Params:
            videos_statistic_info (pd.DataFrame): The new videos statistic DataFrame.

        Raises:
            DataFrameAssignment - If the provided object is not a DataFrame, it raises an exception.
        """
        if not isinstance(videos_statistic_info, pd.DataFrame):
            raise DataFrameAssignment()
        self._videos_statistic_dataframe = videos_statistic_info

    @staticmethod
    def _convert_subs_or_videos(value: str) -> int:
        """
        Extract the number of subscribers or videos from a given YouTube format.

        Params:
            value (str): The number of subscribers and videos in text format.
        """
        value_no_point = value.replace('.', '')

        if 'K' in value_no_point:
            value_without_k = value_no_point.replace('K', '')
            num_digits = len(value_without_k) - 1

            threshold = 100_000

            if num_digits >= 1:
                for _ in range(num_digits):
                    threshold /= 10

            final_value = int(int(value_without_k) * threshold)
        elif 'M' in value_no_point:
            value_without_m = value_no_point.replace('M', '')
            num_digits = len(value_without_m) - 1

            threshold = 1_000_000

            if num_digits >= 1:
                for _ in range(num_digits):
                    threshold /= 10

            final_value = int(int(value_without_m) * threshold)
        else:
            final_value = int(value_no_point.split()[0])

        return final_value

    @staticmethod
    def _format_views(views: str) -> int:
        """
        Converts a YouTube views string to a new formatted number of type int.

        Params:
            views (str): A string containing the number of views from a YouTube video.
        """
        return int(views.split()[0].replace(',', ''))

    @staticmethod
    def _convert_date(date: str) -> str:
        """
        Converts a YouTube video date format to the USA standard date format.

        Params:
            date (str): A date as a string with the form of 'MM (Jan, Feb, etc.) DD, YYYY'.
        """
        if 'Premiered' in date or 'Joined' in date:
            date = date.replace('Premiered', '').replace('Joined', '').strip()

        str_to_datetime = datetime.strptime(date, '%b %d, %Y')
        return str_to_datetime.strftime('%m/%d/%Y')

    def _open_url(self) -> None:
        """
        Access the YouTube specified channel.
        """
        self.driver.get(self.url)

    def _access_youtube(self) -> None:
        """
        Accepts the cookies policies.
        """
        accept_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                     '#yDmH0d > c-wiz > div > div > div > div.nYlMgf > div.gOOQJb > div.qqtRac > div.csJmFc > form:nth-child(3) > div > div > button')))
        accept_btn.click()

    def _scroll(self) -> None:
        """
        Scroll to the bottom of the page.
        """
        height = self.driver.execute_script('return document.documentElement.scrollHeight')
        while True:
            html = self.driver.find_element(By.TAG_NAME, 'html')
            html.send_keys(Keys.END)
            time.sleep(2)
            new_height = self.driver.execute_script('return document.documentElement.scrollHeight')
            if height == new_height:
                break
            height = new_height

    def _get_general_info(self) -> None:
        """
        Get the header information of the channel.
        """
        try:
            container = self.wait.until(EC.presence_of_element_located((By.ID, 'additional-info-container')))
            channel_header_name = container.find_element(By.XPATH, '//*[@id="text"]').text
            get_subscribers_num = self._convert_subs_or_videos(container.find_element(By.CSS_SELECTOR,
                                                                                      '#additional-info-container > table > tbody > tr:nth-child(4) > td:nth-child(2)').text)
            get_videos_num = self._convert_subs_or_videos(container.find_element(By.CSS_SELECTOR,
                                                                                 '#additional-info-container > table > tbody > tr:nth-child(5) > td:nth-child(2)').text)
            join_date = container.find_element(By.CSS_SELECTOR,
                                               '#additional-info-container > table > tbody > tr:nth-child(7) > td:nth-child(2) > yt-attributed-string > span > span').text
            total_views = container.find_element(By.CSS_SELECTOR,
                                                 '#additional-info-container > table > tbody > tr:nth-child(6) > td:nth-child(2)').text

            self._general_channel_info.append({
                'header_name': channel_header_name.replace(' ', ''),
                'subscribers_num': get_subscribers_num,
                'videos_num': get_videos_num,
                'join_date': self._convert_date(join_date),
                'total_views': self._format_views(total_views)
            })

        except NoSuchElementException as e:
            print('Error finding elements in the header of the YouTube channel.\n')
            print(e)

    def _find_all_videos_links(self) -> None:
        """
        Get each video from the channel.
        """
        self.driver.get(f'{SITE}/{self._channel_name}/videos')

        try:
            self._scroll()
            videos = self.driver.find_elements(By.CLASS_NAME, 'style-scope ytd-rich-item-renderer')
            for video in videos:
                video_link = video.find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint').get_attribute('href')
                self._links_of_all_videos.append(video_link)

        except NoSuchElementException as e:
            print('Error finding elements while retrieving video links.\n')
            print(e)

    def _find_videos_info(self) -> None:
        """
        Find the details of the video, including the title, description, number of views
        and the date of posting (format 'Jan DD, YYYY').
        """
        for link in self._links_of_all_videos:
            self.driver.get(link)

            try:
                description_box = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#expand')))
                description_box.send_keys(Keys.RETURN)

                title = self.driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string').text
                description = self.driver.find_element(By.ID, 'description-inline-expander').text
                views = self.driver.find_element(By.XPATH, '//*[@id="info"]/span[1]').text
                date = self.driver.find_element(By.XPATH, '//*[@id="info"]/span[3]').text

                self._all_videos_details.append({
                    'title': title,
                    'views': self._format_views(views),
                    'date': self._convert_date(date),
                    'description': description,
                    'link': link
                })

            except NoSuchElementException as e:
                print(f'Error finding elements for video: {link}\n')
                print(e)

    def _update_dataframes(self) -> None:
        """
        Update the general information and videos details DataFrames of the channel analyzer.
        """
        try:
            self._general_info_dataframe = pd.DataFrame(self._general_channel_info)
            self._videos_info_dataframe = pd.DataFrame(self._all_videos_details)
            self._videos_statistic_dataframe = self._videos_info_dataframe.describe()
        except Exception as e:
            print('Error updating DataFrames.\n')
            print(e)

    def _extract_years_of_activity(self):
        """
        Extract the years of activity from the channel's videos DataFrame.
        """
        if self._videos_info_dataframe is not None:
            years = self._videos_info_dataframe['date'].str[-4:].unique()
            self.years_of_activity = sorted(list(years))

    def harvest_data(self):
        """
        Collects data from the targeted YouTube channel.

        This method is a collection of multiple methods that are responsible for collecting the
        required data needed for the DataFrames.

        The used methods responsibilities are as follows:
        1. Opens the URL of the specified YouTube channel.
        2. Accepts the YouTube cookies policies.
        3. Retrieves general information about the channel (name, subscribers, videos, etc.).
        4. Finds and stores links to all videos on the channel.
        5. Extracts details of each video, including title, description, views and post date.
        6. Updates the general information and video details DataFrames.
        """
        try:
            self._open_url()
            self._access_youtube()
            self._get_general_info()
            self._find_all_videos_links()
            self._find_videos_info()
            self._update_dataframes()
            self._extract_years_of_activity()
        finally:
            self.driver.close()

    def get_harvested_data(self) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Get the DataFrames containing the harvested data.
        """
        return self._general_info_dataframe, self._videos_info_dataframe, self._videos_statistic_dataframe

    def _provide_csv_name(self) -> str:
        """
        Provides the name of the Excel file containing information about the channel name that is
        described in the file with the date and time of creation.
        """
        return f'{self._channel_name[1:]}&{datetime.now().strftime("%d_%m_%Y&%H_%M_%S")}.xlsx'

    def save_channel_details(self) -> None:
        """
        Save the channel details to an Excel file with separate sheets.

        The Excel file contains two sheets:
            - 'general': containing general channel information.
            - 'videos': containing details about every video on the channel.
        """
        saving_location = os.path.join(SYS_DESKTOP_PATH, self._provide_csv_name())

        with pd.ExcelWriter(saving_location) as writer:
            self._general_info_dataframe.to_excel(writer, sheet_name='general', index=False)
            self._videos_info_dataframe.index = self._videos_info_dataframe.index + 1
            self._videos_info_dataframe.to_excel(writer, sheet_name='videos')
            self._videos_statistic_dataframe.to_excel(writer, sheet_name='statistics')


def analyze_channel(channel_name: str) -> ChannelAnalyzer:
    """
    Analyze a YouTube channel and return a ChannelAnalyzer object with harvested data.

    Params:
        channel_name (str): The name of the targeted YouTube channel.
    """
    ca = ChannelAnalyzer(channel_name)
    ca.harvest_data()
    return ca
