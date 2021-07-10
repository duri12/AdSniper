from tkinter import *
from PIL import ImageTk, Image
import subprocess
import os
import signal

FEATURES = [
    # the list of filters for the proxy.
    # #to add a filter just add it here and make sure its in the right place in
    # adblock.py in the REQUEST_FEATURES or RESPONSE_FEATURES
    "none",
    "css",
    "inject img",
    "block img by condition",
    "find and replace"
]

txt = "update block list"

root = Tk()
root.title("adblocker and filter GUI")
root.tk.call('wm', 'iconphoto', root._w, ImageTk.PhotoImage(Image.open('/home/eyal/Desktop/adblock/files/adblock_icon'
                                                                       '.ico')))
root.geometry("750x750+200+200")  # width x height +posx+posy
root.configure(background='black')

file_path_entry = Entry(
    root,
    bg="black",
    fg="white",
    font=("Courier", 16)
)
file_path_entry2 = Entry(
    root,
    bg="black",
    fg="white",
    font=("Courier", 16)
)
path_label2 = Label(
    root,
    text="enter option 2 here :",
    bd=0,
    relief=SUNKEN,
    fg="green",
    bg="black",
    font=("TkDefaultFont", 12),
    anchor=W)
path_label = Label(
    root,
    text="enter option 1 here :",
    bd=0,
    relief=SUNKEN,
    fg="green",
    bg="black",
    font=("TkDefaultFont", 12),
    anchor=W)


def apply_filter():
    """
    get the current FEATURE selected from the list . and send it to feature.txt so
    the proxy script can read it .
    input : none
    output : none
    """
    with open("/home/eyal/Desktop/adblock/files/feature.txt", "w") as filter_file:
        type = variable.get()
        filter_file.write(type)
        if type in ["css", "inject img", "block img by condition", "find and replace"]:
            filter_file.write("\n" + file_path_entry.get())
        if type == "find and replace":
            filter_file.write("\n" + file_path_entry2.get())
    status_bar.configure(text="updated the filter to:" + variable.get())


status_bar = Label(
    root,
    text="adblocker off",
    bd=1,
    relief=SUNKEN,
    anchor=W
)
status_bar.configure(font=("TkDefaultFont", 12))
status_bar.pack(side=BOTTOM, fill=X)

welcome = Label(
    root,
    text="Welcome to the adblocker menu. \n first, update the advertisement lists \n than start the proxy.",
    fg="green",
)
welcome.configure(
    font=("Courier", 16)
    , background='black'
)


def update_blocklist(status_bar):
    """"
    call the bash script to download the lists and  save them to teh blocklists folder
    updates the status bar
    input : status_bar widget
    output: none
    """
    subprocess.Popen("./update-blocklists", shell=True)
    status_bar.configure(text="finished and ready to launch the proxy ")


variable = StringVar(root)
variable.set(FEATURES[0])

proxy_process = subprocess


def kill_port(port):
    """
    Kill the corresponding process according to the port number
    input : the port number to clear
    output : none
    """
    os.system("kill -9 $(lsof -t -i:" + str(port) + ")")


def start_stop_proxy(switch, proxy_process):
    """"
    call the bash script that opens the proxy,
    apply the current filter
    and updates the status bar
    input : the state of the button
    output : the subprocess or none
    """

    if switch:
        proxy_process = subprocess.Popen("./start ", shell=True)
        status_bar.configure(text="started the proxy with the feature :" + variable.get())
        return proxy_process
    else:
        os.kill(proxy_process.pid, signal.SIGINT)
        kill_port(8118)
        status_bar.configure(text="stopped the proxy ")
    return None


option = OptionMenu(
    root,
    variable,
    *FEATURES,
)

option.config(
    bg="green",
    highlightthickness=0,
    activebackground="green",
    fg="black",
    bd=0,
    width=23,
    height=2,
    font=("Courier", 12)
)

submit_button = Button(root, text='Submit', command=apply_filter)
submit_button.config(
    bg="green",
    highlightthickness=0,
    bd=0,
    activebackground="green",
    fg="black",
    width=8,
    height=2,
    font=("Courier", 12)
)

is_on = True

# track the status of the switch img/button

subpro = None


def switch():
    """"
    handles the click on the switch .
    if now on :
        call the start func change status bar
    if now off:
        call the stop func and change status bar
    input : none
    output : none
    """
    global is_on
    global subpro

    if not is_on:
        # stop the proxy
        on_off_button.config(image=off)
        on_off_label.config(text="tap to start the proxy")
        subpro = start_stop_proxy(is_on, subpro)
        is_on = True
    else:
        # start the proxy
        on_off_button.config(image=on)
        on_off_label.config(text="tap to stop the proxy")
        subpro = start_stop_proxy(is_on, subpro)
        is_on = False


# open the on and off imges
# saves it for use in switch
on = Image.open('/home/eyal/Desktop/adblock/files/on.png')
on = on.resize((100, 100), Image.ANTIALIAS)
on = ImageTk.PhotoImage(on)
off = Image.open('/home/eyal/Desktop/adblock/files/off.png')
off = off.resize((100, 100), Image.ANTIALIAS)
off = ImageTk.PhotoImage(off)

on_off_button = Button(
    root,
    image=off,
    bg="black",
    highlightthickness=0,
    activebackground="black",
    bd=0,
    command=switch
)

on_off_label = Label(
    root,
    text="tap to start the proxy",
    fg="green",
    bg="black",
    font=("Courier", 12)
)

load_list = Button(
    text=txt,
    width=20,
    height=3,
    highlightthickness=0,
    bg="green",
    bd=0,
    activebackground="green",
    fg="black",
    font=("Courier", 12),
    command=lambda: update_blocklist(status_bar)
)

# the pos of each object on the GUI
welcome.place(x=130, y=10)
on_off_button.place(x=100, y=210)
on_off_label.place(x=50, y=180)
option.place(x=350, y=100)
submit_button.place(x=630, y=100)
load_list.place(x=50, y=100)
file_path_entry.place(x=200, y=400)
path_label.place(x=10, y=400)
file_path_entry2.place(x=200, y=450)
path_label2.place(x=10, y=450)

# mainloop
root.mainloop()

# ["none"]+list(RESPONSE_FEATURES.keys())+list(REQUEST_FEATURES.keys())
