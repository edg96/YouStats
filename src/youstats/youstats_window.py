import os

from concurrent import futures
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from src.youstats.channel_analyzer import analyze_channel, ChannelAnalyzer
from src.youstats.data_visualizer_posts import DataVisualizerPosts
from src.youstats.data_visualizer_views import DataVisualizerViews


"""
This section contains the global variables responsible for various purposes involving paths required 
by the application in order to function without visual bugs or to malfunction on certain functionalities.

SYS_DESKTOP_PATH: Default saving location for CSV files (defaults to the Desktop of the OS).
APP_ICONS_PATH: Application resources folder for icons.
FILL_CHANNELS_ERROR_MESSAGE: Message to prompt channel name input.
NO_DATA_ERROR_MESSAGE: Message indicating the need for channel analysis.
ANALYSIS_BUTTON_ERROR_MESSAGE: Message for proper analysis steps.
FURTHER_INSTRUCTIONS_MESSAGE: Instructions after channel analysis.

Note:
    Some variables paths are critical for the functionality of the application since some 
    functionalities can be accessed only by using the buttons from the custom tkinter-GUI interface. 
    The absence of the paths will rise errors in the custom tkinter-GUI library (mostly related to 
    the impossibility of finding the icons paths).
"""
SYS_DESKTOP_PATH = os.path.join(os.path.expanduser('~/Desktop'))
APP_ICONS_PATH = os.path.join(Path(__file__).resolve().parent.parent.parent, 'resources', 'icons')
FILL_CHANNELS_ERROR_MESSAGE = "Please provide names for both channels."
NO_DATA_ERROR_MESSAGE = "Please provide channels for analyzing."
ANALYSIS_BUTTON_ERROR_MESSAGE = ("After filling the channels press this button again. \n"
                                 "You will be able to use the functions of the application after the data is "
                                 "collected.")
FURTHER_INSTRUCTIONS_MESSAGE = ("After filling the channels press the top middle button to start the "
                                "analyzing process (the one with teal colored margins). \n"
                                "You will be able to use the functions of the application after the data is "
                                "collected.")


class NoChannelNameError(Exception):
    """
    Custom exception class raised when no channel name is provided for one or both channels.

    This exception is raised when the `analyze_channels` function is called without providing
    the necessary channel names.
    It indicates that either the pivot channel name, the targeted channel name, or both
    are missing.
    """

    def __init__(self):
        super().__init__('No channel name provided for one or both channels.')


def analyze_channels(pivot_channel_name: str, targeted_channel_name: str) -> \
        tuple[ChannelAnalyzer, ChannelAnalyzer]:
    """
    Analyze the provided YouTube channel names.

    Args:
        pivot_channel_name (str): The name of the pivot channel.
        targeted_channel_name (str): The name of the targeted channel.

    Returns:
        tuple: A tuple containing two `ChannelAnalyzer` objects, one for the pivot channel
        and one for the targeted channel.
    """
    if not pivot_channel_name or not targeted_channel_name:
        raise NoChannelNameError()

    channel_names = [pivot_channel_name, targeted_channel_name]

    analyzer_objects = []
    with futures.ThreadPoolExecutor(len(channel_names)) as executor:
        analyzer_objects = list(executor.map(analyze_channel, channel_names))

    return analyzer_objects[0], analyzer_objects[1]


class YouStatsWindow(ctk.CTk):
    """
    YouStatsWindow is a custom tkinter application for analyzing and visualizing two YouTube
    channel datas.
    """
    _saving_location = SYS_DESKTOP_PATH

    def __init__(self):
        """
        Initialize the YouStatsWindow.

        This constructor sets up the GUI elements for analyzing YouTube channels and visualizing data.
        """
        super().__init__()
        self.title(' YouStats')
        self.geometry('448x150')
        self.resizable(False, False)
        print(APP_ICONS_PATH)
        self.after(250, lambda: self.iconbitmap(os.path.join(APP_ICONS_PATH, 'main.ico')))
        self._pc_analyze, self._tc_analyze = None, None

        default_color_bg = self.cget('bg')

        # Entry and Label for "Your channel"
        blueberry_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'blueberry.png')))
        pc_name_lbl = ctk.CTkLabel(self, text=' Yours:',
                                   image=blueberry_image_path, compound='left',
                                   font=('Helvetica', 14, 'bold'))
        pc_name_lbl.grid(row=0, column=0, padx=(10, 10), pady=(5, 0))
        pc_name_ent = ctk.CTkEntry(self, placeholder_text='Type here')
        pc_name_ent.grid(row=1, column=0, padx=(10, 10))

        # Export buttons
        export_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'exportspreedsheet.png')))
        pc_export_image_btn = ctk.CTkButton(self, text='', image=export_image_path, width=5, height=5,
                                            fg_color=default_color_bg,
                                            command=lambda: self.save_pivot_data_to_csv(self._pc_analyze))
        pc_export_image_btn.grid(row=1, column=1, padx=(4, 15))
        tc_export_image_btn = ctk.CTkButton(self, text='', image=export_image_path, width=5, height=5,
                                            fg_color=default_color_bg,
                                            command=lambda: self.save_targeted_data_to_csv(self._tc_analyze))
        tc_export_image_btn.grid(row=1, column=3, padx=(15, 4))

        # Entry and Label for "Targeted channel"
        orange_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'orange.png')))
        tc_name_lbl = ctk.CTkLabel(self, text=' Target:', image=orange_image_path,
                                   compound='left', font=('Helvetica', 14, 'bold'))
        tc_name_lbl.grid(row=0, column=4, padx=(10, 10), pady=(5, 0))
        tc_name_ent = ctk.CTkEntry(self, placeholder_text='Type here')
        tc_name_ent.grid(row=1, column=4, padx=(10, 10))

        # Analyzing button
        analyzing_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'analysis.png')))
        start_analyzing_btn = ctk.CTkButton(self, text='', image=analyzing_image_path, width=25, height=25,
                                            fg_color=default_color_bg, border_width=1, border_color='#00AADC',
                                            command=lambda: self.set_analyzer_objects(pc_name_ent.get(),
                                                                                      tc_name_ent.get()))
        start_analyzing_btn.grid(row=1, column=2)

        # Common posting and views buttons
        common_posting_months_path = ctk.CTkImage(
            Image.open(os.path.join(APP_ICONS_PATH, 'commonstatistics.png')))
        common_posting_months_btn = ctk.CTkButton(self, text='', image=common_posting_months_path,
                                                  width=5, height=5, fg_color=default_color_bg,
                                                  command=lambda: self.get_channels_common_years_posts(
                                                      self._pc_analyze, self._tc_analyze
                                                  ))
        common_posting_months_btn.grid(row=3, column=2, pady=(12, 0))

        common_views_months_btn = ctk.CTkButton(self, text='', image=common_posting_months_path,
                                                width=5, height=5, fg_color=default_color_bg,
                                                command=lambda: self.get_channels_common_years_views(
                                                    self._pc_analyze, self._tc_analyze
                                                ))
        common_views_months_btn.grid(row=4, column=2, pady=(12, 0))

        # Buttons with labels
        pc_posting_rates_btn = ctk.CTkButton(self, text='Posting graphs', font=('Helvetica', 14, 'bold'),
                                             border_width=2, border_color='#00AADC',
                                             command=lambda: self.get_single_channel_posts(
                                                 self._pc_analyze, self._tc_analyze,
                                                 True, False))
        pc_posting_rates_btn.grid(row=3, column=0, padx=(10, 10), pady=(10, 0))

        pc_views_per_month_btn = ctk.CTkButton(self, text='Views graphs', font=('Helvetica', 14, 'bold'),
                                               border_width=2, border_color='#00AADC',
                                               command=lambda: self.get_single_channel_views(
                                                   self._pc_analyze, self._tc_analyze,
                                                   True, False))
        pc_views_per_month_btn.grid(row=4, column=0, padx=(10, 10), pady=(10, 0))

        tc_posting_rates_btn = ctk.CTkButton(self, text='Posting graphs', font=('Helvetica', 14, 'bold'),
                                             border_width=2, border_color='#00AADC',
                                             command=lambda: self.get_single_channel_posts(
                                                 self._pc_analyze, self._tc_analyze,
                                                 False, True))
        tc_posting_rates_btn.grid(row=3, column=4, padx=(10, 10), pady=(10, 0))

        tc_views_per_month_btn = ctk.CTkButton(self, text='Views graphs', font=('Helvetica', 14, 'bold'),
                                               border_width=2, border_color='#00AADC',
                                               command=lambda: self.get_single_channel_views(
                                                   self._pc_analyze, self._tc_analyze,
                                                   False, True))
        tc_views_per_month_btn.grid(row=4, column=4, padx=(10, 10), pady=(10, 0))

        # Arrow buttons
        right_arrow_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'rightarrow.png')))
        left_arrow_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'leftarrow.png')))

        right_arrow_btn = ctk.CTkButton(self, text='', image=right_arrow_path, width=5, height=5,
                                        fg_color=default_color_bg, hover_color=default_color_bg)
        right_arrow_btn.grid(row=3, column=1, pady=(12, 0))
        left_arrow_btn = ctk.CTkButton(self, text='', image=left_arrow_path, width=5, height=5,
                                       fg_color=default_color_bg, hover_color=default_color_bg)
        left_arrow_btn.grid(row=3, column=3, pady=(12, 0))
        right_arrow_btn = ctk.CTkButton(self, text='', image=right_arrow_path, width=5, height=5,
                                        fg_color=default_color_bg, hover_color=default_color_bg)
        right_arrow_btn.grid(row=4, column=1, pady=(12, 0))
        left_arrow_btn = ctk.CTkButton(self, text='', image=left_arrow_path, width=5, height=5,
                                       fg_color=default_color_bg, hover_color=default_color_bg)
        left_arrow_btn.grid(row=4, column=3, pady=(12, 0))

        self.mainloop()

    @staticmethod
    def show_error_message(title, message) -> None:
        """
        Show an error message as a pop-up window.

        Args:
            title (str): The title of the error message.
            message (str): The error message text.
        """
        messagebox.showerror(title, message)

    # Essential function
    def set_analyzer_objects(self, pivot_name, targeted_name) -> None:
        """
        Set the analyzer objects for the pivot and targeted channels.

        Args:
            pivot_name (str): The name of the pivot channel.
            targeted_name (str): The name of the targeted channel.
        """
        try:
            self._pc_analyze, self._tc_analyze = analyze_channels(pivot_name, targeted_name)
        except NoChannelNameError:
            self.show_error_message(" Channels Fill Error", FILL_CHANNELS_ERROR_MESSAGE + '\n'
                                    + ANALYSIS_BUTTON_ERROR_MESSAGE)

    # Export to CSV functions
    def save_pivot_data_to_csv(self, pc_analyze: ChannelAnalyzer) -> None:
        """
        Save the details of the pivot channel to a CSV file.

        Args:
            pc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
        """
        try:
            pc_analyze.save_channel_details()
        except AttributeError:
            self.show_error_message(" Export CSV Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    def save_targeted_data_to_csv(self, tc_analyze: ChannelAnalyzer) -> None:
        """
        Save the details of the targeted channel to a CSV file.

        Args:
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
        """
        try:
            tc_analyze.save_channel_details()
        except AttributeError:
            self.show_error_message(" Export CSV Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    # Posting buttons related functions
    def get_channels_common_years_posts(self, pc_analyze, tc_analyze) -> None:
        """
        Show common years posting data for both channels.

        Args:
            pc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
        """
        dvp = DataVisualizerPosts(pc_analyze, tc_analyze)
        try:
            dvp.show_common_years_posting()
        except AttributeError:
            self.show_error_message(" Posting Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    def get_single_channel_posts(self, pc_analyze, tc_analyze, pc_option: bool, tc_option: bool) -> None:
        """
        Show posting data for one or both channels.

        Args:
            pc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
            pc_option (bool): Show posting data for the pivot channel.
            tc_option (bool): Show posting data for the targeted channel.
        """
        dvp = DataVisualizerPosts(pc_analyze, tc_analyze)
        try:
            dvp.show_single_channel_posting(pc_option, tc_option)
        except AttributeError:
            self.show_error_message(" Posting Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    def get_channels_common_years_views(self, pc_analyze, tc_analyze) -> None:
        """
        Show common years views data for both channels.

        Args:
            pc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
        """
        dvv = DataVisualizerViews(pc_analyze, tc_analyze)
        try:
            dvv.show_common_years_views()
        except AttributeError:
            self.show_error_message("Views Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    def get_single_channel_views(self, pc_analyze, tc_analyze, pc_option: bool, tc_option: bool) -> None:
        """
        Show views data for one or both channels.

        Args:
            pc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
            pc_option (bool): Show views data for the pivot channel.
            tc_option (bool): Show views data for the targeted channel.
        """
        dvv = DataVisualizerViews(pc_analyze, tc_analyze)
        try:
            dvv.show_single_channel_views(pc_option, tc_option)
        except AttributeError:
            self.show_error_message("Views Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)
