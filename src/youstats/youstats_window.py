import os
from concurrent import futures
from pathlib import Path

import customtkinter as ctk
from PIL import Image

from src.youstats.channel_analyzer import analyze_channel, ChannelAnalyzer


class NoChannelNameError(Exception):
    def __init__(self):
        super().__init__('No channel name provided for one or both channels.')


def analyze_channels(pivot_channel_name: str, targeted_channel_name: str):
    if not pivot_channel_name or not targeted_channel_name:
        raise NoChannelNameError()

    channel_names = [pivot_channel_name, targeted_channel_name]
    analyzer_objects = []

    with futures.ThreadPoolExecutor(len(channel_names)) as executor:
        analyzer_objects = list(executor.map(analyze_channel, channel_names))

    return analyzer_objects[0], analyzer_objects[1]


SYS_DESKTOP_PATH = os.path.join(os.path.expanduser('~/Desktop'))


class YouStatsWindow(ctk.CTk):
    _saving_location = SYS_DESKTOP_PATH

    def __init__(self):
        super().__init__()
        self.title(' YouStats')
        self.geometry('440x150')
        self.resizable(False, False)
        self.after(250, lambda: self.iconbitmap(os.path.join(Path(__file__).resolve().parent.parent.parent,
                   'resources', 'main.ico')))
        self._pc_analyze, self._tc_analyze = None, None

        default_color_bg = self.cget('bg')

        # Entry and Label for "Your channel"
        pc_name_lbl = ctk.CTkLabel(self, text='Your channel:', font=('Helvetica', 14, 'bold'))
        pc_name_lbl.grid(row=0, column=0, padx=(10, 10), pady=(5, 0))
        pc_name_ent = ctk.CTkEntry(self, placeholder_text='Type here')
        pc_name_ent.grid(row=1, column=0, padx=(10, 10))

        # Export buttons
        export_image_path = ctk.CTkImage(Image.open(r'D:\2xProjects\Python\YouStats\resources\exportspreedsheet.png'))
        pc_export_image_btn = ctk.CTkButton(self, text='', image=export_image_path, width=5, height=5,
                                            fg_color=default_color_bg,
                                            command=lambda: self.save_pivot_data_to_csv(self._pc_analyze))
        pc_export_image_btn.grid(row=1, column=1, padx=(4, 15))
        tc_export_image_btn = ctk.CTkButton(self, text='', image=export_image_path, width=5, height=5,
                                            fg_color=default_color_bg,
                                            command=lambda: self.save_targeted_data_to_csv(self._tc_analyze))
        tc_export_image_btn.grid(row=1, column=3, padx=(15, 4))

        # Entry and Label for "Targeted channel"
        tc_name_lbl = ctk.CTkLabel(self, text='Targeted channel:', font=('Helvetica', 14, 'bold'))
        tc_name_lbl.grid(row=0, column=4, padx=(10, 10), pady=(5, 0))
        tc_name_ent = ctk.CTkEntry(self, placeholder_text='Type here')
        tc_name_ent.grid(row=1, column=4, padx=(10, 10))

        # Analyzing button
        analyzing_image_path = ctk.CTkImage(Image.open(r'D:\2xProjects\Python\YouStats\resources\analysis.png'))
        start_analyzing_btn = ctk.CTkButton(self, text='', image=analyzing_image_path, width=25, height=25,
                                            fg_color=default_color_bg, border_width=1, border_color='#00AADC',
                                            command=lambda: self.set_analyzer_objects(pc_name_ent.get(),
                                                                                      tc_name_ent.get()))
        start_analyzing_btn.grid(row=1, column=2)

        # Common posting and views buttons
        common_posting_months_path = ctk.CTkImage(Image.open(r'D:\2xProjects\Python\YouStats\resources\commonstatistics.png'))
        common_posting_months_btn = ctk.CTkButton(self, text='', image=common_posting_months_path,
                                                  width=5, height=5, fg_color=default_color_bg,
                                                  command=lambda: self.get_channels_common_years_posts(
                                                      self._pc_analyze, self._tc_analyze
                                                  ))
        common_posting_months_btn.grid(row=3, column=2, pady=(12, 0))

        common_views_months_btn = ctk.CTkButton(self, text='', image=common_posting_months_path,
                                                width=5, height=5, fg_color=default_color_bg)
        common_views_months_btn.grid(row=4, column=2, pady=(12, 0))

        # Buttons with labels
        pc_posting_rates_btn = ctk.CTkButton(self, text='Posting graphs', font=('Helvetica', 14, 'bold'),
                                             border_width=2, border_color='#00AADC',
                                             command=lambda: self.get_single_channel_posts(
                                                 self._pc_analyze, self._tc_analyze,
                                                 True, False))
        pc_posting_rates_btn.grid(row=3, column=0, padx=(10, 10), pady=(10, 0))

        pc_views_per_month_btn = ctk.CTkButton(self, text='Views graphs', font=('Helvetica', 14, 'bold'),
                                             border_width=2, border_color='#00AADC')
        pc_views_per_month_btn.grid(row=4, column=0, padx=(10, 10), pady=(10, 0))

        tc_posting_rates_btn = ctk.CTkButton(self, text='Posting graphs', font=('Helvetica', 14, 'bold'),
                                             border_width=2, border_color='#00AADC',
                                             command=lambda: self.get_single_channel_posts(
                                                 self._pc_analyze, self._tc_analyze,
                                                 False, True))
        tc_posting_rates_btn.grid(row=3, column=4, padx=(10, 10), pady=(10, 0))

        tc_views_per_month_btn = ctk.CTkButton(self, text='Views graphs', font=('Helvetica', 14, 'bold'),
                                             border_width=2, border_color='#00AADC')
        tc_views_per_month_btn.grid(row=4, column=4, padx=(10, 10), pady=(10, 0))

        # Arrow buttons
        right_arrow_path = ctk.CTkImage(Image.open(r'D:\2xProjects\Python\YouStats\resources\rightarrow.png'))
        left_arrow_path = ctk.CTkImage(Image.open(r'D:\2xProjects\Python\YouStats\resources\leftarrow.png'))

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

    # Essential function
    def set_analyzer_objects(self, pivot_name, targeted_name):
        self._pc_analyze, self._tc_analyze = analyze_channels(pivot_name, targeted_name)

    # Export to CSV functions
    def save_pivot_data_to_csv(self, pc_analyze: ChannelAnalyzer):
        pass

    def save_targeted_data_to_csv(self, tc_analyze: ChannelAnalyzer):
        pass

    # Posting buttons related functions
    def get_channels_common_years_posts(self, pc_analyze, tc_analyze):
        pass

    def get_single_channel_posts(self, pc_analyze, tc_analyze, pc_option: bool, tc_option: bool):
        pass

    # Views buttons related functions
    def get_channels_common_years_posts(self):
        pass

    def get_single_channel_views(self):
        pass
