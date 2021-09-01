import os
import threading
from tkinter import *
import time
import requests  # pip install requests
from bs4 import *  # pip install beautifulsoup4

# global variables
VERSION = '1.0.0-SNAP'
debug = True
ping_result = None  # should equal True after ping thread finishes

# thread 1 is main
if debug:
    print(f"creating Python WebScraper {VERSION}")
    time.sleep(0.5)  # blocking
    print("thread 1 created")


def scraper():  # needs building
    url = url_entry.get()
    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="ResultsContainer")
    print(results.prettify())


def thread_ping():  # thread 2
    if debug:
        print("thread 2 created")
    exit_code = os.system(f"ping google.com")
    if exit_code == 0:
        if debug:
            print("ping succeeded")
        global ping_result
        ping_result = True
    else:
        if debug:
            print("ping failed")
        ping_result = False


def thread_window():  # thread 3
    if debug:
        print("thread 3 created")
        print("creating ping window")
    window = Tk()  # creates window widget
    connect = Label(window, text="Connecting to the Internet...")  # creates the text for window
    connect.place(x=60, y=50)
    window.title(f"Python WebScraper {VERSION}")
    window.geometry('300x200+10+10')
    window.mainloop()  # blocking


def error_window(error_message):  # template for error windows
    error = Tk()
    error.title("An error occurred!")
    error.geometry('300x60+20+30')
    error_label = Label(error, text=error_message)
    error_label.place(x=10, y=20)
    error.focus_force()
    error.mainloop()  # blocking


def scrape_parse(selection):
    prop = scrape_entry.index(selection)  # converts tuple to an int based on selection, errors if none is selected
    switcher = {
        0: "test 0",
        1: "test 1"
    }
    return switcher.get(prop, "test default")  # second argument is default


def on_click_1():  # cancel button
    print("button 1 pushed, closing program")
    time.sleep(0.5)  # blocking
    GUI.destroy()


def on_click_2():  # continue button
    print("button pushed 2, launching parser **WIP**")
    # scraper()
    try:
        prop = scrape_parse(scrape_entry.curselection())
        wip = Label(GUI, text=f"I gathered {prop}", fg="red")
        wip.place(x=125, y=350)
    except EXCEPTION:  # cant find correct exception
        pass


if __name__ == "__main__":

    window_thread = threading.Thread(target=thread_window)
    window_thread.setDaemon(True)

    ping = threading.Thread(target=thread_ping)

    ping.start()
    window_thread.start()
    if debug:
        print("launching ping window on thread 3")

    print(f"active threads: {threading.active_count()}")
    time.sleep(4)  # blocking

    if ping_result:  # ping check succeeded
        if debug:
            print("launching GUI window on main thread")
        GUI = Tk()
        GUI.title(f'Python WebScraper {VERSION}')
        GUI.geometry('400x400+0+0')
        GUI.focus_force()

        url_entry = Entry(GUI)
        url_entry.place(x=30, y=50)
        url_label = Label(GUI, text="URL")
        url_label.place(x=30, y=25)

        scrape_entry = Listbox(GUI, selectmode=SINGLE)

        scrape_entry.insert(1, "test")  # return a value of 0 in tuple form
        scrape_entry.insert(2, "test2")

        scrape_entry.place(x=30, y=100)
        scrape_label = Label(GUI, text='Scrape')
        scrape_label.place(x=30, y=75)

        cancel = Button(GUI, text="Cancel", command=on_click_1)
        cancel.place(x=30, y=300)
        cont = Button(GUI, text="Continue", command=on_click_2)
        cont.place(x=300, y=300)

        GUI.mainloop()  # blocking
    elif ping_result is None:  # ping check didn't happen
        error_window('ping failed to launch')
    else:  # ping check failed
        error_window('ping failed to connect')
