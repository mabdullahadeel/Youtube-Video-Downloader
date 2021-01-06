import shutil
import os
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog, messagebox
import pytube
import random
import Utils.helpers as helperFunctions


class DownloadMenu:
    def __init__(self, root_window, *args, **kwargs):
        self.root_window = root_window
        self.args = args
        self.kwargs = kwargs

    def show_result_frame(self):
        result_frame = LabelFrame(self.root_window)
        result_frame.configure(background="#2b2929")
        result_frame.grid(row=3, column=0, columnspan=2, rowspan=4, padx=(2, 2), pady=(0, 10))

        resolution_options = {}

        for stream in self.kwargs["available_stream"]:
            if stream.type == "video":
                if f"Video {stream.resolution}" in resolution_options:
                    resolution_options.update(
                        [(f"Video {stream.resolution}-{random.randint(0, 100)}", int(stream.itag))])
                else:
                    resolution_options.update([(f"Video {stream.resolution}", int(stream.itag))])
            if stream.type == "audio":
                resolution_options.update([(f"Audio {stream.abr}", int(stream.itag))])

        def thread_download_video():
            if resolution_dropdown.get():
                threading.Thread(target=download_video).start()
            else:
                messagebox.showerror('Required Fields', 'Please select required resolution.')

        def select_folder():
            path = filedialog.askdirectory(initialdir=helperFunctions.file_path(), title="Select Folder")
            if path:
                file_path_info.config(text=f'file will be saved to {path}. Press "Select Folder" to change')
                global f_file_path, r_file_path
                f_file_path = path
                r_file_path = f_file_path.replace("/", "\\")

        def try_another():
            self.kwargs["url_entry"].delete(0, END)
            result_frame.destroy()
            self.kwargs["search_button"]["state"] = NORMAL

        def download_video():
            if resolution_dropdown.get():
                # Disabling the essential buttons to prevent running multiple threads
                download_button["state"] = DISABLED
                self.kwargs["search_button"]["state"] = DISABLED
                another_url_button["state"] = DISABLED
                essential_messages.config(text="Downloading the video...........")
                file_name_assigned = file_name_entry.get()
                try:
                    video_progressBar.fileSize = pytube.YouTube(url=self.kwargs["video_url"]) \
                        .streams.get_by_itag(resolution_options[f"{resolution_dropdown.get()}"]).filesize
                    streamQuery = pytube.YouTube(url=self.kwargs["video_url"],
                                                 on_progress_callback=video_progressBar.progress_Check) \
                        .streams.get_by_itag(resolution_options[f"{resolution_dropdown.get()}"])
                    if streamQuery.audio_codec and streamQuery.audio_codec == "mp4a.40.2":
                        path_to_file = streamQuery.download(output_path=r_file_path
                        if "r_file_path" in globals() else helperFunctions.file_path(),
                                                            filename=file_name_assigned if file_name_assigned else streamQuery.title)
                        essential_messages.config(text="Done!")

                        user_selection = messagebox.askquestion('Download Successful',
                                                                f"Video has been downloaded to {path_to_file}. Do you want to play it?",
                                                                icon='info', parent=self.root_window)
                        if user_selection == 'yes':
                            os.system('"%s"' % path_to_file)
                        # Enabling the search button for next search
                        self.kwargs["search_button"]["state"] = NORMAL
                        download_button["state"] = NORMAL
                        another_url_button["state"] = NORMAL
                    else:
                        essential_messages.config(text="Creating and Compiling the Video for you! Please Wait....")
                        streamQuery.download(filename=f"Video_0mpOlokeLYrCsQ64hk5K", output_path="cached/")
                        # Downloading the audio separately
                        pytube.YouTube(url=self.kwargs["video_url"],
                                       on_progress_callback=video_progressBar.progress_Check) \
                            .streams.get_by_itag(140).download(filename="Audio_0mpOlokeLYrCsQ64hk5K",
                                                               output_path="cached/")
                        # Merging the audio and video
                        master_path = r_file_path if "r_file_path" in globals() else helperFunctions.file_path()
                        f_path = ('"%s"' % master_path)
                        save_path = f"{f_path}/{file_name_assigned if file_name_assigned else streamQuery.title}.mp4"
                        helperFunctions.combine_audio(
                            vidname="cached/Video_0mpOlokeLYrCsQ64hk5K.mp4",
                            audname="cached/Audio_0mpOlokeLYrCsQ64hk5K.mp4",
                            outname=save_path,
                            fps=30
                        )
                        # Emptying / Removing the cached folder
                        if os.path.exists('cached/'):
                            shutil.rmtree("cached")
                        essential_messages.config(text="Done!")
                        # Enabling the search button for next search
                        self.kwargs["search_button"]["state"] = NORMAL
                        download_button["state"] = NORMAL
                        another_url_button["state"] = NORMAL

                        user_selection = messagebox.askquestion('Download Successful',
                                                                f"Video has been downloaded to {save_path}. Do you want to play it?",
                                                                icon='info', parent=self.root_window)
                        if user_selection == 'yes':
                            os.system(save_path)
                except AttributeError:
                    download_file = pytube.YouTube(url=self.kwargs["video_url"],
                                                   on_progress_callback=video_progressBar.progress_Check) \
                        .streams.get_highest_resolution()
                    download_file.download(
                        output_path=f"{r_file_path if 'r_file_path' in globals() else helperFunctions.file_path()}")
                    # Enabling the search button for next search
                    self.kwargs["search_button"]["state"] = NORMAL
                    download_button["state"] = NORMAL
                    another_url_button["state"] = NORMAL

        thumbnail = helperFunctions.show_image(image_url=self.kwargs["thumbnail_url"])
        thumbnail_label = Label(result_frame, image=thumbnail)
        thumbnail_label.image = thumbnail
        thumbnail_label.grid(row=0, column=0, sticky=W)

        title_frame = LabelFrame(result_frame, borderwidth=0, highlightthickness=0)
        title_frame.configure(background="#2b2929")
        title_frame.grid(row=0, column=1, padx=(150, 10), pady=(10, 40), sticky=W)

        title = Label(title_frame, text=self.kwargs["title"], font=("bold", 12), bg="#2b2929", fg="white", wraplength=500)
        title.grid(row=0, column=0, sticky=W)

        resolution_label = Label(result_frame, text="Resolution", font=('bold', 14), bg="#2b2929", fg="white")
        resolution_label.grid(row=1, column=0, pady=8, sticky=W)
        resolution_dropdown_value = StringVar()
        resolution_dropdown = ttk.Combobox(result_frame, textvariable=resolution_dropdown_value, width=33,
                                           font=('bold', 14))
        resolution_dropdown['values'] = [k for k in resolution_options]
        resolution_dropdown.grid(row=1, column=1, pady=8, padx=(150, 10), sticky=W)

        file_name = Label(result_frame, text='File Name', font=('bold', 14), bg="#2b2929", fg="white")
        file_name.grid(row=2, column=0, pady=8, sticky=W)
        file_name_text = StringVar()
        file_name_entry = Entry(result_frame, textvariable=file_name_text, width=35, borderwidth=1, font=('bold', 14))
        file_name_entry.grid(row=2, column=1, pady=8, sticky=W, padx=(150, 10))

        download_button = Button(result_frame, text='Download', bg='#5872a8', command=thread_download_video,
                                 fg='#ffffff', font=('bold', 13), width=18)
        download_button.grid(row=3, column=1, sticky=W, padx=(150, 10))

        file_path_button = Button(result_frame, text='Select Folder', bg='#5872a8', command=select_folder,
                                  fg='#ffffff', font=('bold', 13), width=18)
        file_path_button.grid(row=3, column=1, sticky=W, padx=(340, 10))

        another_url_button = Button(result_frame, text='Try Another', bg='#5872a8', command=try_another,
                                    fg='red', font=('bold', 13), width=18)
        another_url_button.grid(row=4, column=1, sticky=W, padx=(150, 10), pady=8)

        file_path_info = Label(result_frame,
                               text=f'file will be saved to {helperFunctions.file_path()}. Press "Select Folder" to change',
                               font=('normal', 7), bg="#2b2929", fg="white", wraplength=500)
        file_path_info.grid(row=5, column=1, pady=8, sticky=W, padx=(150, 0))

        essential_messages = Label(result_frame,
                                   text="",
                                   font=('normal', 10), bg="#2b2929", fg="red", wraplength=600)
        essential_messages.grid(row=7, column=1, pady=8, columnspan=2)

        video_progressBar = helperFunctions.ProgressBar(root_frame=result_frame, length=395)
        video_progressBar.place_progressbar(Row=6, Column=0, columnSpan=2)
