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
height = 650
root.minsize(810, 650)
root.configure(background="#2b2929")
# Placing the screen in the center of the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{width}x{height}+{int((screen_width / 2) - (width / 2))}+{int((screen_height / 2) - (height / 2))}")


def _on_mousewheel_download_history(event):
    download_history_main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def download_history_mouse_enter(event):
    print("Enter")
    download_history_main_canvas.bind_all("<MouseWheel>", _on_mousewheel_download_history)


def download_history_mouse_leave(event):
    print("Leave")
    download_history_main_canvas.unbind_all("<MouseWheel>")

# Frame to hold universal stuff like url input, logo etc
welcome_frame = Frame(root)
welcome_frame.pack(fill=BOTH, expand=1, pady=8)
# Frame to show download options
download_menu = Frame(root)
download_menu.configure(background="red")
download_menu.pack()
# Frame to show the download history
download_history_frame = Frame(root)
download_history_frame.configure(background="green", height=1000)
download_history_frame.pack(fill=BOTH, expand=1, side=BOTTOM)
download_history_frame.bind("<Enter>", download_history_mouse_enter)
download_history_frame.bind("<Leave>", download_history_mouse_leave)
# Create A Canvas
download_history_main_canvas = Canvas(download_history_frame)
download_history_scrollbar = ttk.Scrollbar(download_history_frame, orient=VERTICAL,
                                           command=download_history_main_canvas.yview)
download_history_main_canvas.configure(yscrollcommand=download_history_scrollbar.set)
download_history_main_canvas.pack(side=LEFT, fill=BOTH, expand=1)
# Add A Scrollbar To The Canvas
download_history_scrollbar.pack(side=RIGHT, fill=Y)
download_history_scrollbar.bind('<Configure>', lambda e: download_history_main_canvas
                                .configure(scrollregion=download_history_main_canvas.bbox("all")))
# Creating the child frame to hold the items
inner_download_frame = Frame(download_history_main_canvas)
child_frame_ref = download_history_main_canvas.create_window((0, 0),window=inner_download_frame,
                                                             anchor="nw", width=width, height=height)

# Responsive Screen Configuration
n_rows = 3
n_columns = 2
for i in range(n_rows):
    welcome_frame.grid_rowconfigure(i,  weight=1)
for i in range(n_columns):
    welcome_frame.grid_columnconfigure(i,  weight=1)
download_menu.grid_columnconfigure(1,  weight=1)
download_menu.grid_rowconfigure(1,  weight=1)

# Global Font Configurations
heading_font = Font(
    family="Helvetica",
    size=20, weight="bold", slant="roman", underline=0, overstrike=0
)


def thread_search():
    if url_entry.get():
        # search_button['state'] = DISABLED
        threading.Thread(target=search_video).start()
    else:
        messagebox.showerror('Required Fields', 'Please Provide a valid URL')


def search_video():
    video_url = url_entry.get()
    if video_url:
        res = search(url=video_url)

        # Creating the Frame from the available data to download the video
        m = DownloadMenu(root_window=download_menu,
                         available_stream=res["streams"],
                         originalStream=res["originalStream"],
                         thumbnail_url=res["thumbnail_url"],
                         title=res["title"],
                         video_url=video_url,
                         search_button=search_button,
                         url_entry=url_entry,
                         menu_frame=download_menu
                         )
        m.show_result_frame()


from PIL import Image
image = ImageTk.PhotoImage(Image.open("images/Youtube.png"))
imageLabel = Label(welcome_frame, image=image, bg="#2b2929")
imageLabel.grid(row=0, column=0, sticky=E)
heading = Label(welcome_frame, text='Youtube Video Downloader', font=heading_font, bg="#2b2929", fg="white")
heading.grid(row=0, column=1, padx=0)

url_label = Label(welcome_frame, text='Video URL', font=('bold', 14), bg="#2b2929", fg="white")
url_label.grid(row=1, column=0, padx=0)
url_text = StringVar()
url_entry = Entry(welcome_frame, textvariable=url_text, width=55, borderwidth=1, font=('bold', 14))
url_entry.grid(row=1, column=1)

search_button = Button(welcome_frame, text='Search', bg='#5872a8', command=thread_search,
                           fg='#ffffff', font=('bold', 13), width=20)
search_button.grid(row=2, column=0, columnspan=2, pady=10)

# Test
for i in range(20):
    url_label = Label(inner_download_frame, text='Video URL', font=('bold', 14), bg="#2b2929", fg="white")
    url_label.grid(row=i, column=0, padx=0)

for i in range(20):
    url_label = Label(inner_download_frame, text='A Big HEY!', font=('bold', 14), bg="#2b2929", fg="white")
    url_label.grid(row=i, column=1, padx=10)

root.mainloop()