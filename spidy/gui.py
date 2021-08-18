#!/usr/bin/env python3
from tkinter import (
    BooleanVar,
    # StringVar,
    IntVar,

    Tk,
    Text,

    N,
    W,
    E,
    S
)

from tkinter import ttk
from tkinter import filedialog

from spidy.crawler import (
    PACKAGE_DIR,
    main)


#############
# FUNCTIONS #
#############


def get_file():
    return filedialog.askopenfilename()


def get_text(field):
    return field.get('1.0', 'end')


def setup_window():
    global window
    # Main window
    window.title('spidy Web Crawler - by rivermont')
    window.iconbitmap('{0}\\media\\favicon.ico'.format(PACKAGE_DIR))

    overwrite = BooleanVar()
    raise_errors = BooleanVar()
    save_pages = BooleanVar()
    zip_files_ = BooleanVar()
    save_words = BooleanVar()
    # todo_file = StringVar()
    # done_file = StringVar()
    # bad_file = StringVar()
    # word_file = StringVar()
    save_count = IntVar()
    max_new_errors = IntVar()
    max_http_errors = IntVar()
    max_known_errors = IntVar()
    max_new_mimes = IntVar()
    # custom_headers = StringVar()

    # Frame to fill main window
    main_frame = ttk.Frame(window, padding='4')
    main_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    main_frame.columnconfigure(0, weight=1)
    main_frame.rowconfigure(0, weight=1)

    # Container to hold variable settings
    setting_box = ttk.Frame(main_frame, padding='4', borderwidth=1, relief='solid')
    setting_box.grid(column=0, row=0, sticky=(N, S, W))
    setting_box.columnconfigure(0, weight=1)
    setting_box.rowconfigure(0, weight=1)

    # Container for things on the right side of the main window
    right_bar = ttk.Frame(main_frame, padding='4', borderwidth=1, relief='solid')
    right_bar.grid(column=1, row=0, sticky=(N, S, E))
    right_bar.columnconfigure(2, weight=1)
    right_bar.rowconfigure(0, weight=1)

    # Container for controlling the crawler
    control_box = ttk.Frame(right_bar, padding='4', borderwidth=1, relief='solid')
    control_box.grid(column=1, row=0, sticky=(N, E, W))
    control_box.columnconfigure(1, weight=1)
    control_box.rowconfigure(0, weight=1)

    # Container for the status elements
    status_box = ttk.Frame(right_bar, padding='4', borderwidth=1, relief='solid')
    status_box.grid(column=0, row=1, sticky=(E, W))
    status_box.columnconfigure(0, weight=1)
    status_box.rowconfigure(1, weight=1)

    # Container for the console log
    console_box = ttk.Frame(right_bar, padding='4', borderwidth=1, relief='solid')
    console_box.grid(column=0, row=2)
    console_box.columnconfigure(0, weight=1)
    console_box.rowconfigure(2, weight=1)

    # Button to pause the crawler
    pause_button = ttk.Button(control_box, padding='4', text='Pause')
    pause_button.grid(column=0, row=0, sticky=(N, S, W))
    pause_button.columnconfigure(0, weight=1)
    pause_button.rowconfigure(0, weight=1)

    # Button to start the crawler
    go_button = ttk.Button(control_box, command=main(), padding='4', text='Go')
    go_button.grid(column=1, row=0, sticky=(N, S))
    go_button.columnconfigure(1, weight=1)
    go_button.rowconfigure(0, weight=1)

    # Button to stop the crawler
    stop_button = ttk.Button(control_box, padding='4', text='Stop')
    stop_button.grid(column=2, row=0, sticky=(N, S, E))
    stop_button.columnconfigure(2, weight=1)
    stop_button.rowconfigure(0, weight=1)

    # Title for crawler setting area
    ttk.Label(setting_box, text='Crawler Settings').grid(column=0, row=0, columnspan=4, sticky=(N, S))

    # Option to set Overwrite
    overwrite_check = ttk.Checkbutton(setting_box, text='Overwrite', variable=overwrite)
    overwrite_check.grid(column=0, row=1, columnspan=2, sticky=W)
    overwrite_check.columnconfigure(0, weight=1)
    overwrite_check.rowconfigure(1, weight=1)

    # Option to set RaiseErrors
    raise_errors_check = ttk.Checkbutton(setting_box, text='Raise Errors', variable=raise_errors)
    raise_errors_check.grid(column=0, row=2, columnspan=2, sticky=W)
    raise_errors_check.columnconfigure(0, weight=1)
    raise_errors_check.rowconfigure(2, weight=1)

    # Option to set SavePages
    save_pages_check = ttk.Checkbutton(setting_box, text='Save Pages', variable=save_pages)
    save_pages_check.grid(column=0, row=3, columnspan=2, sticky=W)
    save_pages_check.columnconfigure(0, weight=1)
    save_pages_check.rowconfigure(3, weight=1)

    # Option to set ZipFiles
    zip_files_check = ttk.Checkbutton(setting_box, text='Zip Files', variable=zip_files_)
    zip_files_check.grid(column=0, row=4, columnspan=2, sticky=W)
    zip_files_check.columnconfigure(0, weight=1)
    zip_files_check.rowconfigure(4, weight=1)

    # Option to set SaveWords
    save_words_check = ttk.Checkbutton(setting_box, text='Save Words', variable=save_words)
    save_words_check.grid(column=0, row=5, columnspan=2, sticky=W)
    save_words_check.columnconfigure(0, weight=1)
    save_words_check.rowconfigure(5, weight=1)

    # Field to enter number for SaveCount
    ttk.Label(setting_box, text='Save Count').grid(column=0, row=6, columnspan=2, sticky=W)

    save_count_entry = ttk.Entry(setting_box, width=5, textvariable=save_count)
    save_count_entry.grid(column=0, row=7, sticky=(E, W))
    save_count_entry.columnconfigure(0, weight=1)
    save_count_entry.rowconfigure(7, weight=1)

    # Field to enter custom headers
    ttk.Label(setting_box, text='Custom Headers').grid(column=0, row=8, columnspan=2, sticky=W)

    custom_headers_entry = Text(setting_box, height=3, width=16)
    custom_headers_entry.grid(column=0, row=9, columnspan=2, sticky=W)
    custom_headers_entry.columnconfigure(0, weight=1)
    custom_headers_entry.rowconfigure(9, weight=1)

    # Field to enter custom starting links
    ttk.Label(setting_box, text='Start Links').grid(column=0, row=10, columnspan=2, sticky=W)

    custom_start_links = Text(setting_box, height=2, width=16)
    custom_start_links.grid(column=0, row=11, columnspan=2, sticky=W)
    custom_start_links.columnconfigure(0, weight=1)
    custom_start_links.rowconfigure(11, weight=1)

    # Button to select todo file
    get_todo_file_button = ttk.Button(setting_box, text='...', command=get_file)
    get_todo_file_button.grid(column=2, row=1, sticky=W)
    get_todo_file_button.columnconfigure(1, weight=1)
    get_todo_file_button.rowconfigure(2, weight=1)

    ttk.Label(setting_box, text='TODO File').grid(column=3, row=1, sticky=W)

    # Button to select done file
    get_done_file_button = ttk.Button(setting_box, text='...', command=get_file)
    get_done_file_button.grid(column=2, row=2, sticky=W)
    get_done_file_button.columnconfigure(2, weight=1)
    get_done_file_button.rowconfigure(2, weight=1)

    ttk.Label(setting_box, text='Done File').grid(column=3, row=2, sticky=W)

    # Button to select bad link file
    get_bad_file_button = ttk.Button(setting_box, text='...', command=get_file)
    get_bad_file_button.grid(column=2, row=3, sticky=W)
    get_bad_file_button.columnconfigure(2, weight=1)
    get_bad_file_button.rowconfigure(3, weight=1)

    ttk.Label(setting_box, text='Bad Link File').grid(column=3, row=3, sticky=W)

    # Button to select word file
    get_word_file_button = ttk.Button(setting_box, text='...', command=get_file)
    get_word_file_button.grid(column=2, row=4, sticky=W)
    get_word_file_button.columnconfigure(2, weight=1)
    get_word_file_button.rowconfigure(4, weight=1)

    ttk.Label(setting_box, text='Word File').grid(column=3, row=4, sticky=W)

    # Field to set MaxNewErrors
    max_new_error_entry = ttk.Entry(setting_box, width=4, textvariable=max_new_errors)
    max_new_error_entry.grid(column=2, row=5, sticky=(E, W))
    max_new_error_entry.columnconfigure(2, weight=1)
    max_new_error_entry.rowconfigure(5, weight=1)

    ttk.Label(setting_box, text='Max New Errors').grid(column=3, row=5, sticky=W)

    # Field to set MaxHTTPErrors
    max_http_error_entry = ttk.Entry(setting_box, width=4, textvariable=max_http_errors)
    max_http_error_entry.grid(column=2, row=6, sticky=(E, W))
    max_http_error_entry.columnconfigure(2, weight=1)
    max_http_error_entry.rowconfigure(6, weight=1)

    ttk.Label(setting_box, text='Max HTTP Errors').grid(column=3, row=6, sticky=W)

    # Field to set MaxKnownErrors
    max_known_errors_entry = ttk.Entry(setting_box, width=4, textvariable=max_known_errors)
    max_known_errors_entry.grid(column=2, row=7, sticky=(E, W))
    max_known_errors_entry.columnconfigure(2, weight=1)
    max_known_errors_entry.rowconfigure(7, weight=1)

    ttk.Label(setting_box, text='Max Known Errors').grid(column=3, row=7, sticky=W)

    # Field to set MaxNewMIMEs
    max_new_mimes_entry = ttk.Entry(setting_box, width=4, textvariable=max_new_mimes)
    max_new_mimes_entry.grid(column=2, row=8, sticky=(E, W))
    max_new_mimes_entry.columnconfigure(2, weight=1)
    max_new_mimes_entry.rowconfigure(8, weight=1)

    ttk.Label(setting_box, text='Max New MIMEs').grid(column=3, row=8, sticky=W)


def keep_alive():
    while RUNNING:
        window.mainloop()


def run():
    global window
    setup_window()
    window.mainloop()


if __name__ == '__main__':
    pass
    window = Tk()
    RUNNING = True
    # Open thread for keep_alive
    # Open thread for window to run in
    # Open thread for crawler to run in?
    run()
