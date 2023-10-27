import os
import time
from datetime import datetime

import pandas as pd
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

__all__ = ['analyze_channel']

SITE = 'https://www.youtube.com'
SYS_DESKTOP_PATH = os.path.join(os.path.expanduser('~/Desktop'))


class ChannelIsNone(Exception):
    """
    Custom exception class for the channel attribute from a ChannelAnalyzer type object, raised when
    the operations of assign or getting that is associated with the channel name is None.

    Notes:
        - Important Custom Exception for assuring that a channel name is provided and the
        ChannelAnalyzer have a channel to work with, being the starting point and a mandatory
        condition for the application.
    """
    def __init__(self, message='Channel is None. It needs a value to serve as target.'):
        super().__init__(message)


class DataFrameEmpty(Exception):
    """
    Custom exception class for a DataFrame from a ChannelAnalyzer type object, raised when the DataFrame
    is associated with a value of None, which flags the DataFrame as being not fit for use.
    """
    def __init__(self, message='DataFrame is None. Analyze a channel to provide data for the DataFrame.'):
        super().__init__(message)


class DataFrameAssignment(Exception):
    """
    Custom exception class for a DataFrame from a ChannelAnalyzer type object, raised when the assign
    operation is attempting to associate a non DataFrame type of object to a field that is not
    expecting another type of object other than DataFrame.
    """
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
        _channel_name (str): The name of the targeted YouTube channel.
        url (str): The URL of the targeted YouTube channel.
        _general_channel_info (list[dict]): A list to store general channel information.
        _links_of_all_videos (list[str]): A list to store links to all videos on the channel.
        _all_videos_details (list[dict]): A list to store details of each video on the channel.
    """
    _general_info_dataframe = None
    _videos_info_dataframe = None
    _videos_statistic_dataframe = None

    def __init__(self, target: str):
        self._channel_name = target
        self.url = f'{SITE}/{target}'
        self._general_channel_info = []
        self._links_of_all_videos = []
        self._all_videos_details = []

        self.chrome_options = Options()
        self.chrome_options.add_argument("--mute-audio")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    @property
    def channel_name(self):
        if self._channel_name is None:
            raise ChannelIsNone()
        return self._channel_name

    @property
    def general_info_dataframe(self):
        if self._general_info_dataframe is None:
            raise DataFrameEmpty()
        else:
            return self._general_info_dataframe

    @property
    def videos_info_dataframe(self):
        if self._videos_info_dataframe is None:
            raise DataFrameEmpty()
        else:
            return self._videos_info_dataframe

    @property
    def videos_statistic_dataframe(self):
        if self._videos_statistic_dataframe is None:
            raise DataFrameEmpty()
        else:
            return self._videos_statistic_dataframe

    @channel_name.setter
    def channel_name(self, channel_name):
        if channel_name is None:
            raise ChannelIsNone()
        self._channel_name = channel_name

    @general_info_dataframe.setter
    def general_info_dataframe(self, general_info_dataframe):
        if not isinstance(general_info_dataframe, pd.DataFrame):
            raise DataFrameAssignment()
        self._general_info_dataframe = general_info_dataframe

    @videos_info_dataframe.setter
    def videos_info_dataframe(self, videos_info_dataframe):
        if not isinstance(videos_info_dataframe, pd.DataFrame):
            raise DataFrameAssignment()
        self._videos_info_dataframe = videos_info_dataframe

    @videos_statistic_dataframe.setter
    def videos_statistic_dataframe(self, videos_statistic_info):
        if not isinstance(videos_statistic_info, pd.DataFrame):
            raise DataFrameAssignment()
        self._videos_statistic_dataframe = videos_statistic_info

    @staticmethod
    def _convert_subs_or_videos(value: str) -> int:
        """
        Extract the number of subscribers or videos from a given YouTube format.
        Parameters:
            value (str): The number of subscribers and videos in text format.
        Returns:
            int: The numbs of subcribers and videos converted.
        """
        value_no_point = value.replace('.', '')
        clean_value = 0

        if value_no_point.find('K') != -1:
            clean_value = value_no_point[:value_no_point.find('K ')]
            clean_value = int(clean_value) * 1_000
        elif value_no_point.find('M') != -1:
            clean_value = value_no_point[:value_no_point.find('M ')]
            clean_value = int(clean_value) * 1_000_000
        else:
            clean_value = value[0: value.find(' ')]

        return clean_value

    @staticmethod
    def _format_views(views: str) -> int:
        """
        Converts a YouTube views string to a new formatted number of type int.

        Parameters:
            views (str): A string containing the number of views from a YouTube video.

        Returns:
            int: The newly formatted views count.
        """
        strip_text = views[0:views.find(' ')]

        return int(strip_text.replace(',', ''))

    @staticmethod
    def _convert_date(date: str) -> str:
        """
        Converts a YouTube video date format to the USA standard date format.

        Parameters:
            date (str): A date as string with the form of 'MM (Jan, Feb etc.) DD, YYYY'.

        Returns:
            str: The date formatted as 'MM/DD/YYYY'.
        """
        str_to_datetime = datetime.strptime(date, '%b %d, %Y')
        formatted_date = str_to_datetime.strftime('%m/%d/%Y')

        return formatted_date

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

    def _open_url(self) -> None:
        """
        Access the YouTube specified channel.
        """
        self.driver.get(self.url)

    def _access_youtube(self) -> None:
        """
        Accepts the cookies policies.
        """
        accept_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#yDmH0d > c-wiz > div > div > div > div.nYlMgf > div.gOOQJb > div.qqtRac > div.csJmFc > form:nth-child(3) > div > div > button')))
        accept_btn.click()

    def _get_general_info(self) -> None:
        """
        Get the header information of the channel.
        """
        self.driver.get(f'{SITE}/{self._channel_name}/about')

        channel_header_name = self.driver.find_element(By.XPATH, '//*[@id="text"]').text
        get_subcribers_num = self._convert_subs_or_videos(self.driver.find_element(By.ID, 'subscriber-count').text)
        get_videos_num = self._convert_subs_or_videos(self.driver.find_element(By.ID, 'videos-count').text)
        join_date = self.driver.find_element(By.XPATH, '//*[@id="right-column"]/yt-formatted-string[2]/span[2]').text
        total_views = self.driver.find_element(By.XPATH, '//*[@id="right-column"]/yt-formatted-string[3]').text

        self._general_channel_info.append({
            'header_name': channel_header_name.replace(' ', ''),
            'subcribers_num': get_subcribers_num,
            'videos_num': get_videos_num,
            'join_date': self._convert_date(join_date),
            'total_views': self._format_views(total_views)
        })

    def _find_all_videos_links(self) -> None:
        """
        Get each video from the channel.
        """
        self.driver.get(f'{SITE}/{self._channel_name}/videos')

        self._scroll()
        videos = self.driver.find_elements(By.CLASS_NAME, 'style-scope ytd-rich-item-renderer')
        for video in videos:
            video_link = video.find_element(By.CSS_SELECTOR, 'a.yt-simple-endpoint').get_attribute('href')
            self._links_of_all_videos.append(video_link)

    def _find_videos_info(self) -> None:
        """
        Find the details of the video, including the title, description, number of views
        and the date of posting (format 'Jan DD, YYYY').
        """
        for link in self._links_of_all_videos:
            self.driver.get(link)
            description_box = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#expand')))
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

    def _update_dataframes(self) -> None:
        """
        Update the general information and videos details DataFrames of the channel analyzer.
        """
        self._general_info_dataframe = pd.DataFrame(self._general_channel_info)
        self._videos_info_dataframe = pd.DataFrame(self._all_videos_details)
        self._videos_statistic_dataframe = self._videos_info_dataframe.describe()

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
        self._open_url()
        self._access_youtube()
        self._get_general_info()
        self._find_all_videos_links()
        self._find_videos_info()
        self._update_dataframes()

    def get_harvested_data(self):
        return self._general_info_dataframe, self._videos_info_dataframe, self._videos_statistic_dataframe

    def _provide_csv_name(self) -> str:
        """
        Provides the name of the CSV file containing information about the channel name that is
        described in the file with the date and time of creation.

        Returns:
            str: The name of the CSV file.
        """
        return self._channel_name[1::] + '&' + datetime.now().strftime("%d_%m_%Y&%H_%M_%S") + '.xlsx'

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


def analyze_channel(channel_name):
    ca = ChannelAnalyzer(channel_name)
    ca.harvest_data()
    ca.driver.close()
    return ca
