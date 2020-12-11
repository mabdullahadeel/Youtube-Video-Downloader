from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
from PIL import ImageTk
from Utils.utils import *
from Utils.tkutils import *
import threading

# Window Setting
root = Tk()
root.iconbitmap("Images/logo.ico")
root.title("AU YT Downloader")

width = 900
height = 550
root.minsize(810, 650)
root.configure(background="#2b2929")
# Placing the screen in the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{width}x{height}+{int((screen_width / 2) - (width / 2))}+{int((screen_height / 2) - (height / 2))}")

# Responsive Screen Configuration
n_rows = 3
n_columns = 2
for i in range(n_rows):
    root.grid_rowconfigure(i,  weight=1)
for i in range(n_columns):
    root.grid_columnconfigure(i,  weight=1)

# Global Font Configurations
heading_font = Font(
    family="Helvetica",
    size=20, weight="bold", slant="roman", underline=0, overstrike=0
)


def thread_search():
    if url_entry.get():
        search_button['state'] = DISABLED
        threading.Thread(target=search_video).start()
    else:
        messagebox.showerror('Required Fields', 'Please Provide a valid URL')


def search_video():
    video_url = url_entry.get()
    if video_url:
        res = search(url=video_url)

        # Creating the Frame from the available data to download the video
        show_result_frame(root_window=root,
                          available_stream=res["streams"],
                          originalStream=res["originalStream"],
                          thumbnail_url=res["thumbnail_url"],
                          title=res["title"],
                          video_url=video_url,
                          search_button=search_button,
                          url_entry=url_entry)


from PIL import Image
image = ImageTk.PhotoImage(Image.open("images/Youtube.png"))
imageLabel = Label(root, image=image, bg="#2b2929")
imageLabel.grid(row=0, column=0, sticky=E)
heading = Label(root, text='Youtube Video Downloader', font=heading_font, bg="#2b2929", fg="white")
heading.grid(row=0, column=1, padx=0)

url_label = Label(root, text='Video URL', font=('bold', 14), bg="#2b2929", fg="white")
url_label.grid(row=1, column=0, padx=0)
url_text = StringVar()
url_entry = Entry(root, textvariable=url_text, width=55, borderwidth=1, font=('bold', 14))
url_entry.grid(row=1, column=1)

search_button = Button(root, text='Search', bg='#5872a8', command=thread_search,
                           fg='#ffffff', font=('bold', 13), width=20)
search_button.grid(row=2, column=0, columnspan=2, pady=10)


root.mainloop()