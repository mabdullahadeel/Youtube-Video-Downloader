import pytube
from tkinter import *
from tkinter import ttk


def show_image(image_url):
    from PIL import Image, ImageTk
    import requests
    from io import BytesIO

    url = image_url
    response = requests.get(url)
    raw_data = response.content
    response.close()
    im = Image.open(BytesIO(raw_data))
    im = im.resize((100, 80), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(im)
    return photo


def combine_audio(vidname, audname, outname, fps=30):
    import moviepy.editor as mpe
    my_clip = mpe.VideoFileClip(vidname)
    audio_background = mpe.AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps, logger=None)


# Grabs the file path for Download on Any Machine
def file_path():
    import os
    home = os.path.expanduser('~')
    download_path = os.path.join(home, 'Downloads')
    return download_path


class ProgressBar:
    def __init__(self, root_frame, length, fileSize=None):
        self.root_frame = root_frame
        self.length = length
        self.fileSize = fileSize

        # Creating the progress bar
        self.progressbar_frame = LabelFrame(self.root_frame, borderwidth=0, highlightthickness=0)
        self.progressbar_frame.configure(background="#2b2929")
        self.progressbar = ttk.Progressbar(self.progressbar_frame, orient=HORIZONTAL, length=self.length, mode="determinate")
        self.label = Label(self.progressbar_frame, text="Downloaded", bg="#2b2929", fg="white", font=('bold', 14))

    def place_progressbar(self, Row, Column, columnSpan):
        self.progressbar_frame.grid(row=Row, column=Column, columnspan=columnSpan, padx=5, pady=(4, 6), sticky=W)
        # Placing internal Frame Components
        self.label.grid(row=0, column=0, pady=15, sticky=W)
        self.progressbar.grid(row=0, column=1, sticky=W, padx=(150, 10))

    def step(self, increment_value):
        self.progressbar.config(value=increment_value)
        # updating the frame to update the progressbar in real time
        self.progressbar_frame.update_idletasks()

    def progress_Check(self, stream: pytube.Stream, chunk: bytes, bytes_remaining: int):
        # Gets the percentage of the file that has been downloaded.
        file_size = self.fileSize
        percent = (100 * (int(file_size) - int(bytes_remaining))) / file_size
        self.step(increment_value=percent)
        # print("{:00.0f}% downloaded".format(percent))

