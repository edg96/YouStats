import os
import tkinter
from concurrent import futures
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from youstats.channel_analyzer import analyze_channel, ChannelAnalyzer
from youstats.data_visualizer_posts import DataVisualizerPosts
from youstats.data_visualizer_views import DataVisualizerViews

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
FILL_CHANNELS_ERROR_MESSAGE = 'Please provide names for both channels.'
NO_DATA_ERROR_MESSAGE = 'Please provide channels for analyzing.'
ANALYSIS_BUTTON_ERROR_MESSAGE = ('After filling the channels press this button again. \n'
                                 'You will be able to use the functions of the application after the data is '
                                 'collected.')
FURTHER_INSTRUCTIONS_MESSAGE = ('After filling the channels press the top middle button to start the '
                                'analyzing process (the one with teal colored margins). \n'
                                'You will be able to use the functions of the application after the data is '
                                'collected.')
DISABLED_OPTION_MESSAGE = 'Waiting for data'


class MissingChannelNamesError(Exception):
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

    Parameters:
        pivot_channel_name (str): The name of the pivot channel.
        targeted_channel_name (str): The name of the targeted channel.

    Returns:
        tuple: A tuple containing two `ChannelAnalyzer` objects, one for the pivot channel
        and one for the targeted channel.
    """
    if not pivot_channel_name or not targeted_channel_name:
        raise MissingChannelNamesError()

    channel_names = [pivot_channel_name, targeted_channel_name]

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
        self.geometry('602x340')
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(os.path.join(APP_ICONS_PATH, 'main.ico')))
        self.configure(fg_color='#283649')
        self._yc_analyze, self._tc_analyze = None, None
        self.yc_posting_years = self.yc_views_years = DISABLED_OPTION_MESSAGE
        self.tc_posting_years = self.tc_views_years = DISABLED_OPTION_MESSAGE
        self.common_posting_years = self.common_views_years = DISABLED_OPTION_MESSAGE

        default_color_bg = self.cget('bg')

        def menu_option_selection(choice):
            ctk.StringVar(value=choice)

        # *********************
        # Icons paths loading *
        # *********************
        self.orange_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'orange.png')))
        self.blueberry_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'blueberry.png')))
        self.analyzing_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'analysis.png')))
        self.export_image_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'exportspreedsheet.png')))
        self.common_posting_months_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'commonstatistics.png')))
        self.all_years_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'all.png')))
        self.right_arrow_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'rightarrow.png')))
        self.left_arrow_path = ctk.CTkImage(Image.open(os.path.join(APP_ICONS_PATH, 'leftarrow.png')))

        # ******************************
        # Your channel related content *
        # ******************************
        # Label for channel name
        self.yc_name_lbl = ctk.CTkLabel(self, text=' Yours:',
                                        image=self.blueberry_image_path, compound='left',
                                        font=('Helvetica', 14, 'bold'))
        self.yc_name_lbl.grid(row=0, column=0, padx=(10, 10), pady=(5, 0))

        # Entry for channel name
        self.yc_name_ent = ctk.CTkEntry(self, placeholder_text='Type here')
        self.yc_name_ent.grid(row=1, column=0, padx=(10, 10))

        # Button for saving to excel
        self.yc_export_data_csv_btn = ctk.CTkButton(self, text='', image=self.export_image_path, width=5, height=5,
                                                    fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.save_data_to_csv(self._yc_analyze))
        self.yc_export_data_csv_btn.grid(row=1, column=1, padx=(4, 15))

        # Button retrieving graph for posts (single year)
        self.yc_posts_single_year_btn = ctk.CTkButton(self, text='Posting graphs', font=('Helvetica', 14, 'bold'),
                                                      border_width=3, border_color='#45556d',
                                                      fg_color='#87a0b5', hover_color='#7a8ca2',
                                                      text_color='#283649',
                                                      command=lambda: self.get_single_channel_posts(
                                                          self._yc_analyze, self._tc_analyze,
                                                          True, False, self.yc_posts_select_year_var,
                                                          self.yc_name_ent.get()))
        self.yc_posts_single_year_btn.grid(row=3, column=0, padx=(10, 10), pady=(10, 0))

        # Button retrieving the graph for posts (all years)
        self.yc_posts_all_years_btn = ctk.CTkButton(self, text='', image=self.all_years_path,
                                                    width=5, height=5, fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.get_single_channel_posts(
                                                        self._yc_analyze, self._tc_analyze,
                                                        True, False, self.yc_posting_years,
                                                        self.yc_name_ent.get()
                                                    ))
        self.yc_posts_all_years_btn.grid(row=4, column=1, padx=(10, 10), pady=(10, 10))

        # Button retrieving graph for views (single year)
        self.yc_views_single_year_btn = ctk.CTkButton(self, text='Views graphs', font=('Helvetica', 14, 'bold'),
                                                      border_width=3, border_color='#45556d',
                                                      fg_color='#87a0b5', hover_color='#7a8ca2',
                                                      text_color='#283649',
                                                      command=lambda: self.get_single_channel_views(
                                                          self._yc_analyze, self._tc_analyze,
                                                          True, False, self.yc_views_select_year_var,
                                                          self.yc_name_ent.get()))
        self.yc_views_single_year_btn.grid(row=6, column=0, padx=(10, 10), pady=(10, 0))

        # Button retrieving graph for posts (all years)
        self.yc_views_all_years_btn = ctk.CTkButton(self, text='', image=self.all_years_path,
                                                    width=5, height=5, fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.get_single_channel_views(
                                                        self._yc_analyze, self._tc_analyze,
                                                        True, False, self.yc_views_years,
                                                        self.yc_name_ent.get()
                                                    ))
        self.yc_views_all_years_btn.grid(row=7, column=1, padx=(10, 10), pady=(10, 10))

        # Dropdown menu for posting years
        self.yc_posts_select_year_var = ctk.StringVar(value=DISABLED_OPTION_MESSAGE)
        self.yc_posts_select_year_menu = ctk.CTkOptionMenu(self, state='disabled', font=('Helvetica', 14, 'bold'),
                                                           fg_color='#87a0b5', button_hover_color='#7a8ca2',
                                                           text_color='#283649', text_color_disabled='#283649',
                                                           button_color='#45556d', dropdown_fg_color='#87a0b5',
                                                           dropdown_hover_color='#7a8ca2',
                                                           dropdown_text_color='#283649',
                                                           command=lambda choice:
                                                           menu_option_selection(choice),
                                                           variable=self.yc_posts_select_year_var)
        self.yc_posts_select_year_menu.grid(row=4, column=0, padx=(10, 10), pady=(10, 10))

        # Dropdown menu for views years
        self.yc_views_select_year_var = ctk.StringVar(value=DISABLED_OPTION_MESSAGE)
        self.yc_views_select_year_menu = ctk.CTkOptionMenu(self, state='disabled', font=('Helvetica', 14, 'bold'),
                                                           fg_color='#87a0b5', button_hover_color='#7a8ca2',
                                                           text_color='#283649', text_color_disabled='#283649',
                                                           button_color='#45556d', dropdown_fg_color='#87a0b5',
                                                           dropdown_hover_color='#7a8ca2',
                                                           dropdown_text_color='#283649',
                                                           command=lambda choice:
                                                           menu_option_selection(choice),
                                                           variable=self.yc_views_select_year_var)
        self.yc_views_select_year_menu.grid(row=7, column=0, padx=(10, 10), pady=(10, 10))

        # **********************************
        # Targeted channel related content *
        # **********************************
        # Label for channel name
        self.tc_name_lbl = ctk.CTkLabel(self, text=' Target:', image=self.orange_image_path,
                                        compound='left', font=('Helvetica', 14, 'bold'))
        self.tc_name_lbl.grid(row=0, column=4, padx=(10, 10), pady=(5, 0))

        # Entry for channel name
        self.tc_name_ent = ctk.CTkEntry(self, placeholder_text='Type here')
        self.tc_name_ent.grid(row=1, column=4, padx=(10, 10))

        # Button for saving to excel
        self.tc_export_data_csv_btn = ctk.CTkButton(self, text='', image=self.export_image_path, width=5, height=5,
                                                    fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.save_data_to_csv(self._tc_analyze))
        self.tc_export_data_csv_btn.grid(row=1, column=3, padx=(15, 4))

        # Button retrieving graph for posts (single year)
        self.tc_posts_single_year_btn = ctk.CTkButton(self, text='Posting graphs', font=('Helvetica', 14, 'bold'),
                                                      border_width=3, border_color='#45556d',
                                                      fg_color='#87a0b5', hover_color='#7a8ca2',
                                                      text_color='#283649',
                                                      command=lambda: self.get_single_channel_posts(
                                                          self._yc_analyze, self._tc_analyze,
                                                          False, True, self.tc_posts_select_year_var,
                                                          self.tc_name_ent.get()))
        self.tc_posts_single_year_btn.grid(row=3, column=4, padx=(10, 10), pady=(10, 0))

        # Button retrieving the graph for posts (all years)
        self.tc_posts_all_years_btn = ctk.CTkButton(self, text='', image=self.all_years_path,
                                                    width=5, height=5, fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.get_single_channel_posts(
                                                        self._yc_analyze, self._tc_analyze,
                                                        False, True, self.tc_posting_years,
                                                        self.tc_name_ent.get()
                                                    ))
        self.tc_posts_all_years_btn.grid(row=4, column=3, padx=(10, 10), pady=(10, 10))

        # Button retrieving graph for views (single year)
        self.tc_views_single_year_btn = ctk.CTkButton(self, text='Views graphs', font=('Helvetica', 14, 'bold'),
                                                      border_width=3, border_color='#45556d',
                                                      fg_color='#87a0b5', hover_color='#7a8ca2',
                                                      text_color='#283649',
                                                      command=lambda: self.get_single_channel_views(
                                                          self._yc_analyze, self._tc_analyze,
                                                          False, True, self.tc_views_select_year_var,
                                                          self.tc_name_ent.get()))
        self.tc_views_single_year_btn.grid(row=6, column=4, padx=(10, 10), pady=(10, 0))

        # Button retrieving graph for posts (all years)
        self.tc_views_all_years_btn = ctk.CTkButton(self, text='', image=self.all_years_path,
                                                    width=5, height=5, fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.get_single_channel_views(
                                                        self._yc_analyze, self._tc_analyze,
                                                        False, True, self.tc_views_years,
                                                        self.tc_name_ent.get()
                                                    ))
        self.tc_views_all_years_btn.grid(row=7, column=3, padx=(10, 10), pady=(10, 10))

        # Dropdown menu for selecting posting year
        self.tc_posts_select_year_var = ctk.StringVar(value=DISABLED_OPTION_MESSAGE)
        self.tc_posts_select_year_menu = ctk.CTkOptionMenu(self, state='disabled', font=('Helvetica', 14, 'bold'),
                                                           fg_color='#87a0b5', button_hover_color='#7a8ca2',
                                                           text_color='#283649', text_color_disabled='#283649',
                                                           button_color='#45556d', dropdown_fg_color='#87a0b5',
                                                           dropdown_hover_color='#7a8ca2',
                                                           dropdown_text_color='#283649',
                                                           command=lambda choice:
                                                           menu_option_selection(choice),
                                                           variable=self.tc_posts_select_year_var)
        self.tc_posts_select_year_menu.grid(row=4, column=4, padx=(10, 10), pady=(10, 10))

        # Dropdown menu for selecting views year
        self.tc_views_select_year_var = ctk.StringVar(value=DISABLED_OPTION_MESSAGE)
        self.tc_views_select_year_menu = ctk.CTkOptionMenu(self, state='disabled', font=('Helvetica', 14, 'bold'),
                                                           fg_color='#87a0b5', button_hover_color='#7a8ca2',
                                                           text_color='#283649', text_color_disabled='#283649',
                                                           button_color='#45556d', dropdown_fg_color='#87a0b5',
                                                           dropdown_hover_color='#7a8ca2',
                                                           dropdown_text_color='#283649',
                                                           command=lambda choice:
                                                           menu_option_selection(choice),
                                                           variable=self.tc_views_select_year_var)
        self.tc_views_select_year_menu.grid(row=7, column=4, padx=(10, 10), pady=(10, 10))

        # *********************************
        # Common channels related content *
        # *********************************
        # Posting section
        # Button retrieving graph for posts (start operation)
        self.common_years_posts_btn = ctk.CTkButton(self, text='', image=self.common_posting_months_path,
                                                    width=15, height=15, fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.get_channels_common_years_posts(
                                                        self._yc_analyze, self._tc_analyze,
                                                        self.common_posts_select_year_var
                                                    ))
        self.common_years_posts_btn.grid(row=3, column=2, pady=(12, 0))

        # Button retrieving graph for posts (all years)
        self.common_posts_all_years_btn = ctk.CTkButton(self, text='All years posts', font=('Helvetica', 14, 'bold'),
                                                        border_width=3, border_color='#45556d',
                                                        fg_color='#87a0b5', hover_color='#7a8ca2',
                                                        text_color='#283649',
                                                        command=lambda: self.get_channels_common_years_posts(
                                                            self._yc_analyze, self._tc_analyze,
                                                            self.common_posting_years))
        self.common_posts_all_years_btn.grid(row=5, column=2, padx=(10, 10), pady=(10, 10))

        # Dropdown menu for selecting posting years
        self.common_posts_select_year_var = ctk.StringVar(value=DISABLED_OPTION_MESSAGE)
        self.common_posts_select_year_menu = ctk.CTkOptionMenu(self, state='disabled', font=('Helvetica', 14, 'bold'),
                                                               fg_color='#87a0b5', button_hover_color='#7a8ca2',
                                                               text_color='#283649', text_color_disabled='#283649',
                                                               button_color='#45556d', dropdown_fg_color='#87a0b5',
                                                               dropdown_hover_color='#7a8ca2',
                                                               dropdown_text_color='#283649',
                                                               command=lambda choice:
                                                               menu_option_selection(choice),
                                                               variable=self.common_posts_select_year_var)
        self.common_posts_select_year_menu.grid(row=4, column=2, padx=(10, 10), pady=(10, 10))

        # Views section
        # Button retrieving graph for views (start operation)
        self.common_years_views_btn = ctk.CTkButton(self, text='', image=self.common_posting_months_path,
                                                    width=15, height=15, fg_color=default_color_bg,
                                                    hover_color='#657282',
                                                    command=lambda: self.get_channels_common_years_views(
                                                        self._yc_analyze, self._tc_analyze,
                                                        self.common_views_select_year_var
                                                    ))
        self.common_years_views_btn.grid(row=6, column=2, pady=(12, 0))

        # Button retrieving graph for views (all years)
        self.common_views_all_years_btn = ctk.CTkButton(self, text='All years views', font=('Helvetica', 14, 'bold'),
                                                        border_width=3, border_color='#45556d',
                                                        fg_color='#87a0b5', hover_color='#7a8ca2',
                                                        text_color='#283649',
                                                        command=lambda: self.get_channels_common_years_views(
                                                            self._yc_analyze, self._tc_analyze,
                                                            self.common_views_years))
        self.common_views_all_years_btn.grid(row=8, column=2, padx=(10, 10), pady=(10, 10))

        # Dropdown menu for selecting views years
        self.common_views_select_year_var = ctk.StringVar(value=DISABLED_OPTION_MESSAGE)
        self.common_views_select_year_menu = ctk.CTkOptionMenu(self, state='disabled', font=('Helvetica', 14, 'bold'),
                                                               fg_color='#87a0b5', button_hover_color='#7a8ca2',
                                                               text_color='#283649', text_color_disabled='#283649',
                                                               button_color='#45556d', dropdown_fg_color='#87a0b5',
                                                               dropdown_hover_color='#7a8ca2',
                                                               dropdown_text_color='#283649',
                                                               command=lambda choice:
                                                               menu_option_selection(choice),
                                                               variable=self.common_views_select_year_var)
        self.common_views_select_year_menu.grid(row=7, column=2, padx=(10, 10), pady=(10, 10))

        # *************************
        # General related content *
        # *************************
        # Analyze channels process
        self.start_analyzing_btn = ctk.CTkButton(self, text='', image=self.analyzing_image_path, width=25, height=25,
                                                 fg_color=default_color_bg, border_width=2, border_color='#00AADC',
                                                 command=lambda: self.set_analyzer_objects(self.yc_name_ent.get(),
                                                                                           self.tc_name_ent.get()))
        self.start_analyzing_btn.grid(row=1, column=2)

        # Arrow buttons
        self.right_arrow_btn = ctk.CTkButton(self, text='', image=self.right_arrow_path, width=5, height=5,
                                             fg_color=default_color_bg, hover_color=default_color_bg)
        self.right_arrow_btn.grid(row=3, column=1, pady=(12, 0))
        self.left_arrow_btn = ctk.CTkButton(self, text='', image=self.left_arrow_path, width=5, height=5,
                                            fg_color=default_color_bg, hover_color=default_color_bg)
        self.left_arrow_btn.grid(row=3, column=3, pady=(12, 0))
        self.right_arrow_btn = ctk.CTkButton(self, text='', image=self.right_arrow_path, width=5, height=5,
                                             fg_color=default_color_bg, hover_color=default_color_bg)
        self.right_arrow_btn.grid(row=6, column=1, pady=(12, 0))
        self.left_arrow_btn = ctk.CTkButton(self, text='', image=self.left_arrow_path, width=5, height=5,
                                            fg_color=default_color_bg, hover_color=default_color_bg)
        self.left_arrow_btn.grid(row=6, column=3, pady=(12, 0))

    # **************************
    # Functions related to the custom tkinter-GUI interface functionalities
    # General functions
    @staticmethod
    def show_error_message(title: str, message: str) -> None:
        """
        Show an error message as a pop-up window.

        Parameters:
            title (str): The title of the error message.
            message (str): The error message text.
        """
        messagebox.showerror(title, message)

    @staticmethod
    def set_dropdown_menus(years: list[str], dropdown_var: tkinter.StringVar,
                           dropdown_menu: ctk.CTkOptionMenu) -> None:
        """
        Set dropdown menus with available years.

        Parameters:
            years (list[str]): List of available years.
            dropdown_var (tkinter.StringVar): Variable for the dropdown year.
            dropdown_menu (CTkOptionMenu): The dropdown menu.
        """
        first_year_in_list = years[0]
        dropdown_var.set(first_year_in_list)
        dropdown_menu.configure(state='normal', values=years)

    @staticmethod
    def find_common_years(yc_years: list[str], tc_years: list[str]) -> list[str]:
        """
        Find the common years between the pivot and targeted channels.

        Parameters:
            yc_years (list[str]): Years of activity for the pivot channel.
            tc_years (list[str]): Years of activity for the targeted channel.

        Returns:
            list[str]: A list of common years between the two channels.
        """
        print(yc_years)
        print(type(yc_years))
        common_years = list(set(yc_years) & set(tc_years))
        common_years.sort()

        return common_years

    def update_available_years(self) -> None:
        """
        Update the available years for both channels and common years.
        """
        self.yc_posting_years = self.yc_views_years = self._yc_analyze.years_of_activity
        self.tc_posting_years = self.tc_views_years = self._tc_analyze.years_of_activity

        self.common_posting_years = self.find_common_years(self.yc_posting_years, self.tc_posting_years)
        self.common_views_years = self.find_common_years(self.yc_views_years, self.tc_views_years)

        self.set_dropdown_menus(self.yc_posting_years, self.yc_posts_select_year_var, self.yc_posts_select_year_menu)
        self.set_dropdown_menus(self.yc_views_years, self.yc_views_select_year_var, self.yc_views_select_year_menu)

        self.set_dropdown_menus(self.tc_posting_years, self.tc_posts_select_year_var, self.tc_posts_select_year_menu)
        self.set_dropdown_menus(self.tc_views_years, self.tc_views_select_year_var, self.tc_views_select_year_menu)

        self.set_dropdown_menus(self.common_posting_years, self.common_posts_select_year_var,
                                self.common_posts_select_year_menu)
        self.set_dropdown_menus(self.common_views_years, self.common_views_select_year_var,
                                self.common_views_select_year_menu)

    # **************************
    # Channels related functions
    def set_analyzer_objects(self, pivot_name: str, targeted_name: str) -> None:
        """
        Set the analyzer objects for the pivot and targeted channels, proceeding to call the update
        method to set the years variables and fill up the menus with the years found after the
        analysis.

        Parameters:
            pivot_name (str): The name of the pivot channel.
            targeted_name (str): The name of the targeted channel.
        """
        try:
            self._yc_analyze, self._tc_analyze = analyze_channels(pivot_name, targeted_name)
        except MissingChannelNamesError as e:
            print(e.__traceback__)
            print(e)
            self.show_error_message(" Channels Fill Error", FILL_CHANNELS_ERROR_MESSAGE + '\n'
                                    + ANALYSIS_BUTTON_ERROR_MESSAGE)
        self.update_available_years()

    # Export to CSV functions
    def save_data_to_csv(self, channel: ChannelAnalyzer) -> None:
        """
        Save the details of the pivot channel to a CSV file.

        Parameters:
            channel (ChannelAnalyzer): The analyzer object for the pivot channel.
        """
        try:
            channel.save_channel_details()
        except AttributeError as e:
            print(e.__traceback__)
            print(e)
            self.show_error_message(" Export CSV Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    # Posting buttons related functions
    def get_single_channel_posts(self, yc_analyze: ChannelAnalyzer, tc_analyze: ChannelAnalyzer,
                                 yc_option: bool, tc_option: bool,
                                 year_for_plotting: tkinter.StringVar | str, channel_name: str) -> None:
        """
        Show posting data for one or both channels.

        Parameters:
            yc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
            yc_option (bool): Show posting data for the pivot channel.
            tc_option (bool): Show posting data for the targeted channel.
            year_for_plotting (str | tkinter.StringVar): Year(s) for plotting.
            channel_name (str): The name of the channel associated with the years for plotting.
        """
        if isinstance(year_for_plotting, tkinter.StringVar):
            selected_year = year_for_plotting.get()
            year_for_plotting = selected_year.split(',')

        dvp = DataVisualizerPosts(yc_analyze, tc_analyze)
        try:
            dvp.show_single_channel_posting(yc_option, tc_option, year_for_plotting, channel_name)
        except AttributeError as e:
            print(e.__traceback__)
            print(e)
            self.show_error_message(" Posting Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    def get_single_channel_views(self, yc_analyze: ChannelAnalyzer, tc_analyze: ChannelAnalyzer,
                                 yc_option: bool, tc_option: bool,
                                 year_for_plotting: tkinter.StringVar | str,
                                 channel_name: str) -> None:
        """
        Show views data for one or both channels.

        Parameters:
            yc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
            yc_option (bool): Show views data for the pivot channel.
            tc_option (bool): Show views data for the targeted channel.
            year_for_plotting (str | tkinter.StringVar): Year(s) for plotting.
            channel_name (str): The name of the channel associated with the years for plotting.
        """
        if isinstance(year_for_plotting, tkinter.StringVar):
            selected_year = year_for_plotting.get()
            year_for_plotting = selected_year.split(',')

        dvv = DataVisualizerViews(yc_analyze, tc_analyze)
        try:
            dvv.show_single_channel_views(yc_option, tc_option, year_for_plotting, channel_name)
        except AttributeError as e:
            print(e.__traceback__)
            print(e)
            self.show_error_message(" Views Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    def get_channels_common_years_posts(self, yc_analyze: ChannelAnalyzer, tc_analyze: ChannelAnalyzer,
                                        year_for_plotting: tkinter.StringVar | str) -> None:
        """
        Show common years posting data for both channels.

        Parameters:
            yc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
            year_for_plotting (str | tkinter.StringVar): Year(s) for plotting.
        """
        if isinstance(year_for_plotting, tkinter.StringVar):
            selected_year = year_for_plotting.get()
            year_for_plotting = selected_year.split(',')

        dvp = DataVisualizerPosts(yc_analyze, tc_analyze)
        try:
            dvp.show_common_years_posting(year_for_plotting)
        except AttributeError as e:
            print(e.__traceback__)
            print(e)
            self.show_error_message(" Posting Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)

    def get_channels_common_years_views(self, yc_analyze: ChannelAnalyzer, tc_analyze: ChannelAnalyzer,
                                        year_for_plotting: tkinter.StringVar | str) -> None:
        """
        Show common years views data for both channels.

        Parameters:
            yc_analyze (ChannelAnalyzer): The analyzer object for the pivot channel.
            tc_analyze (ChannelAnalyzer): The analyzer object for the targeted channel.
            year_for_plotting (str | tkinter.StringVar): Year(s) for plotting.
        """
        if isinstance(year_for_plotting, tkinter.StringVar):
            selected_year = year_for_plotting.get()
            year_for_plotting = selected_year.split(',')

        dvv = DataVisualizerViews(yc_analyze, tc_analyze)
        try:
            dvv.show_common_years_views(year_for_plotting)
        except AttributeError as e:
            print(e.__traceback__)
            print(e)
            self.show_error_message(" Views Graphs Error", NO_DATA_ERROR_MESSAGE + '\n'
                                    + FURTHER_INSTRUCTIONS_MESSAGE)
