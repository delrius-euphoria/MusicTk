import os
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from io import BytesIO
import webbrowser
from glob import glob

import pygame
from PIL import Image, ImageTk
from mutagen.id3 import ID3

from player import Player
from read_write import write, read, create, save


root = tk.Tk()
root.tk.call("source", "sun-valley.tcl")
root.tk.call("set_theme", "light")
root.title('MusicTk')
root.iconbitmap('images/logo.ico')

pygame.init()

font_headers = ('Montserrat SemiBold', 18)
font_title = ('Montserrat SemiBold', 35)
font_hover = ('Poppins SemiBold', 15)
song_info = {}
updated_info = {}
count = 0
updated_count = 0
searched = False
started = False
once = False
VERSION = 'Beta 1.5'

h, w = root.winfo_screenheight(), root.winfo_screenwidth()

displaced_w, displaced_h = int(w/12.97), int(h/23.47)
root.geometry(f'+{displaced_w}+{displaced_h}')
root.resizable(0, 0)


def play(curselect, player=None, loader=False):
    global started, once

    if searched:
        try:
            song = updated_info[curselect]
        except KeyError:
            return

    else:
        try:
            song = song_info[curselect]
        except KeyError:
            return

    tag = ID3(song[1])
    title = tag.get('TIT2')
    album = tag.get('TALB')
    artist = tag.get('TPE1')
    if not loader:
        pygame.mixer.music.load(song[1])
        pygame.mixer.music.play()
        started = True

    try:
        art_data = tag.getall('APIC')[0].data
        im = Image.open(BytesIO(art_data)).resize(
            (500, 499), Image.ANTIALIAS
            ).convert('RGB')

        player.config(track=title, album=album, art=im, artist=artist,
                      backup_track=song[0])

    except IndexError:
        player.config(track=title, album=album, artist=artist, art=[],
                      backup_track=song[0])

    if started and not once and not loader:
        check_event()
        once = True


def directory(dir=''):
    global count, updated_count, path

    if dir:
        path = filedialog.askdirectory(title='Choose a directory with songs',
                                       initialdir=dir)
    else:
        path = filedialog.askdirectory(title='Choose a directory with songs')

    load_songs(path, 'dir') if path else ''


def load_songs(song_paths, path_type=None):
    global count, updated_count

    if not path_exists(song_paths):
        return

    if path_type == 'dir':
        song_paths = glob(song_paths+'/*.mp3')

    for song_path in song_paths:
        song = os.path.basename(song_path).split('.')[0]
        song_list.insert('end', song)
        if searched:
            updated_count += 1
            updated_info[updated_count] = [song, song_path]

        song_info[count] = [song, song_path]
        count += 1

    status_bar.config(text=f'Current song count: {song_list.size()}')


def file():
    global count, updated_count, path

    path = filedialog.askopenfilenames(title='Choose song files',
                                       filetypes=(('MP3 file', '*.mp3'),))
    load_songs(path)


def callback(*args):
    global updated_count, updated_info, searched

    updated_info = {}
    if searchbar.get():
        song_list.delete(0, 'end')
        for item in song_info.values():
            if searchbar.get().lower() in item[0].lower():
                updated_info[updated_count] = [item[0], item[1]]
                song_list.insert('end', item[0])
                updated_count += 1
                searched = True
        else:
            updated_count = 0
            if not song_list.size():
                searchbar.state(['invalid'])
            else:
                searchbar.state(['!invalid'])

        status_bar.config(text=f'Current song count: {song_list.size()}')

    else:
        song_list.delete(0, 'end')
        searched = False
        for item in song_info.values():
            song_list.insert('end', item[0])
        status_bar.config(text=f'Current song count: {song_list.size()}')


def play_song():
    global started

    if not once:
        song_list.selection_clear(0, 'end')
        song_list.selection_set(idx)
        song_list.activate(idx)
        song_list.see(idx)
        play(idx, player=init_player)

    else:
        if not started:
            pygame.mixer.music.unpause()
            started = True

        else:
            pygame.mixer.music.pause()
            started = False


def next_prev_song(action, player=None):

    try:
        idx = song_list.curselection()[0]
        song_list.selection_clear(0, 'end')

        if action == 'next':
            id = idx+1
        else:
            id = idx-1

        song_list.selection_set(id)
        song_list.activate(id)

        play(curselect=song_list.curselection()[0], player=player)

    except IndexError:
        idx = 0
        song_list.selection_clear(0, 'end')
        song_list.selection_set(idx)
        song_list.activate(idx)

        try:
            play(curselect=idx)
        except KeyError:
            pass


def rewind():
    pygame.mixer.music.rewind()


def check_event():
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            next_prev_song('next')
    root.after(100, check_event)


def ret_event():
    try:
        idx = song_list.curselection()[0]
        play(idx)

    except IndexError:
        pass


def reset():
    init_player.config(track='-', album='-', art=[], artist='-')


def empty():
    global song_info, count

    song_list.delete(0, 'end')
    pygame.mixer.music.pause()
    song_info = {}
    searchbar.delete(0, 'end')
    count = 0
    status_bar.config(text=f'Current song count: {song_list.size()}')
    reset()


def about():
    # Defining Urls
    url_2 = "https://github.com/delrius-euphoria/MusicTk"

    # Define about section
    about = tk.Toplevel(root)
    about.resizable(False, False)
    about.title('About')
    about.focus_force()
    # about.iconbitmap('images/about.ico')

    # Making frames
    frame = tk.LabelFrame(about, text='About this program:', padx=5, pady=5)

    # Making frame items
    l_name = tk.Label(frame, text='Created by Delrius Euphoria')
    l_ver = tk.Label(frame, text=f'Ver: {VERSION}')
    l_lic = tk.Label(frame, text='Licensed under MIT')
    btn_cod = ttk.Button(frame, text='Source Code!',
                         command=lambda: webbrowser.open(url_2, new=1))
    btn_cls = ttk.Button(frame, text='Close', command=about.destroy)

    # Placing in screen
    frame.grid(row=0, column=0, padx=100, pady=100)
    l_name.grid(row=0, column=0)
    l_ver.grid(row=1, column=0)
    l_lic.grid(row=2, column=0)
    btn_cod.grid(row=3, column=0, sticky='ew', pady=10)
    btn_cls.grid(row=4, column=0, sticky='ew')


def change_theme(player, file_menu):
    if player.tk.call("ttk::style", "theme", "use") == "sun-valley-light":
        theme = 'dark'
        file_menu['bg'] = 'black'
    else:
        theme = 'light'
        file_menu['bg'] = 'white'

    player.switch_images(theme)
    player.tk.call("set_theme", theme)


def show_mini():
    global ismini

    def show_main(btn):
        global ismini

        left_frame.grid(row=1, column=0, padx=(100, 10))
        heading_label.grid(row=0, column=0, columnspan=2, pady=15)
        status_bar.grid(row=2, column=0, columnspan=2, sticky='ew')
        btn.grid_forget()
        right_frame.grid_configure(padx=100)
        file_menu.entryconfig(2, label='Switch to mini player',
                              command=show_mini)

        ismini = False

    if song_list.size() == 0 and not once:
        messagebox.showerror('Choose song',
                             'Play a song from main player first and then '
                             'switch to mini-player')
        return

    right_frame.grid_configure(padx=20)
    left_frame.grid_forget()
    heading_label.grid_forget()
    status_bar.grid_forget()

    btn = ttk.Button(right_frame, text='Switch to main player')
    btn.grid(row=1, column=0, sticky='ew', pady=(20, 0))
    btn['command'] = lambda: show_main(btn)
    file_menu.entryconfig(2, label='Switch to main player',
                          command=lambda: show_main(btn))

    ismini = True


def check_and_load():
    global theme, path, idx, sng_name, ismini

    dir_path = create()

    if not os.path.exists(dir_path + '/settings.toml'):
        write()

    theme, path, idx, sng_name, ismini = read()


def is_dir_file(path):
    if os.path.isdir(path):
        return 'dir'
    elif os.path.isfile(path):
        return 'file'


def restore_settings():
    global idx

    if ismini:
        path_type = is_dir_file(path)
        load_songs(path, path_type)
        try:
            idx = name_to_idx(sng_name)
        except:
            write()
            return

        song_list.selection_clear(0, 'end')
        song_list.selection_set(idx)
        song_list.activate(idx)
        song_list.see(idx)
        play(idx, init_player, True)

        show_mini()

    if theme == 'dark':
        change_theme(init_player, file_menu)


def save_settings():
    theme = root.tk.call('ttk::style', 'theme', 'use').split('-')[-1]
    name = song_list.get('active')
    try:
        idx = song_list.curselection()[0]
    except IndexError:
        idx = 0

    save(theme, path, idx, name, ismini)
    root.destroy()


def path_exists(path):
    return os.path.exists(path)


def name_to_idx(name):
    values = list(song_list.get(0, 'end'))
    idx = values.index(name)

    return idx


logo = ImageTk.PhotoImage(
    Image.open('images/logo.png').resize((100, 100), Image.ANTIALIAS)
    )
heading_label = tk.Label(root, text='MusicTk', font=font_title, image=logo,
                         compound='left')
heading_label.grid(row=0, column=0, columnspan=2, pady=15)

left_frame = tk.Frame(root)
left_frame.grid(row=1, column=0, padx=(100, 10))  # padx=10

search_label = tk.Label(left_frame, text='Search song from your list:',
                        font=font_headers)
search_label.grid(row=0, column=0, columnspan=2, sticky='w')

song_list_label = tk.Label(left_frame, text='Song list:', font=font_headers)
song_list_label.grid(row=2, column=0, sticky='w', columnspan=2,
                     pady=(15, 5))  # pady=15,5

search = tk.StringVar()
searchbar = ttk.Entry(left_frame, font=(0, 15), textvariable=search)
searchbar.grid(row=1, column=0, sticky='ew', columnspan=3)

song_list_frame = tk.Frame(left_frame)
song_list_frame.grid(row=3, column=0, columnspan=3)

song_list = tk.Listbox(song_list_frame, width=35, font=(0, 15), takefocus=0,
                       highlightthickness=0, selectborderwidth=0,
                       activestyle='dotbox', relief='flat')
song_list.pack()

sb_v = tk.Scrollbar(song_list_frame)
sb_v.pack(side='right', fill='y', before=song_list)

sb_h = tk.Scrollbar(song_list_frame, orient='horizontal')
sb_h.pack(fill='x')

song_list.config(yscrollcommand=sb_v.set)
song_list.config(xscrollcommand=sb_h.set)
sb_v.config(command=song_list.yview)
sb_h.config(command=song_list.xview)

ttk.Button(left_frame, text='Add a song directory', command=directory).grid(
    row=4, column=0, ipady=5, pady=5
    )
ttk.Button(left_frame, text='Add a song file', command=file).grid(
    row=4, column=1, ipady=5, pady=5
    )
ttk.Button(left_frame, text='Empty the list', command=empty).grid(
    row=4, column=2, ipady=5, pady=5
    )

song_list.bind('<Double-Button-1>', lambda e: play(
    curselect=song_list.curselection()[0], player=init_player
    ))
search.trace('w', callback)

right_frame = tk.Frame(root)
right_frame.grid(row=1, column=1, padx=100, pady=10)

init_player = Player(right_frame, artist='-', album='-', track='-',
                     playfunc=lambda: play_song(),
                     previousfunc=lambda: next_prev_song('prev', init_player),
                     nextfunc=lambda: next_prev_song('next', init_player),
                     stopfunc=lambda: rewind(), theme='light')
init_player.grid(row=0, column=0)

status_bar = tk.Label(root, text='Current song count: 0', relief='sunken',
                      anchor='w')
status_bar.grid(row=2, column=0, columnspan=2, sticky='ew')

MUSIC_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END)

root.bind('<Left>', lambda e: next_prev_song('prev'))
root.bind('<space>', lambda e: play_song())
root.bind('<Right>', lambda e: next_prev_song('next'))

try:
    root.bind('<Return>', lambda e: play(song_list.curselection()[0],
                                         player=init_player))
except IndexError:
    pass

my_menu = tk.Menu(root)
file_menu = tk.Menu(my_menu, tearoff=0)
root.config(menu=my_menu)
my_menu.add_cascade(label='Menu', menu=file_menu)
file_menu.add_separator()
file_menu.add_command(label='Switch theme',
                      command=lambda: change_theme(init_player, file_menu))
file_menu.add_command(label='Switch to mini player', command=show_mini)
file_menu.add_command(label='About', command=about)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=save_settings)

check_and_load()
restore_settings()

root.protocol('WM_DELETE_WINDOW', save_settings)

root.mainloop()
