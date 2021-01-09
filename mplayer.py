import tkinter as tk
from player import Player
from glob import glob
from tkinter import ttk
import os
import pygame
from mutagen.id3 import ID3
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont
from io import BytesIO
import pyglet
from tkinter import filedialog

root = tk.Tk()
root.title('MPlayer')
root.iconbitmap('images/logo.ico')
pygame.init()
font_headers = ('kenyan coffee rg',25) 
font_title = ('kenyan coffee rg',45) 
font_hover = ('Poppins SemiBold',15)
song_info = {}
count = 0
updated_info = {}
updated_count = 0
searched = False
started = False
once = False
VERSION = 'Beta 1.00'

h,w = root.winfo_screenheight(),root.winfo_screenwidth()
five00_w = w/3.84
five00_h = h/2.16
fifty_w = w/38.4
padx_5 = w/384
padx_10 = w/192
padx_100 = w/19.2
pady_5 = h/216
pady_10 = h/108
pady_15 = h/72
rf_w = w/3.80
rf_h = h/1.44
displaced_w,displaced_h = int(w/12.97),int(h/23.47)
root.geometry(f'+{displaced_w}+{displaced_h}')

def drawer(img,text,W,H):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font='fonts/Poppins-SemiBold.ttf',size=25)
    if len(text) > 30:
        text = text[:30] + '...'
    w, h = draw.textsize(text,font=font)
    draw.text(((W-w)/2,(H-h)/2), text, font=font,fill="white",align='left',stroke_fill='black',stroke_width=2)
    # draw.text(tup,text,font=font,align='center')
    return img

def play(curselect):
    global started, once
    if searched:
        # print(song_list.curselection())
        # print(updated_info)
        song = updated_info[curselect]
        pygame.mixer.music.load(song[1])
        pygame.mixer.music.play()
        started = True
        tag = ID3(song[1])
        # print(tag.get('TIT2'))
        title = tag.get('TIT2')
        album = tag.get('TALB')
        artist = tag.get('TPE1')
        try:
            art = tag.getall('APIC')[0].data
            artwork = ImageTk.PhotoImage(Image.open(BytesIO(art)).resize((int(five00_w),int(five00_h)),Image.ANTIALIAS))
            artwork_blur = ImageTk.PhotoImage(drawer(Image.open(BytesIO(art)).resize((int(five00_w),int(five00_h)),Image.ANTIALIAS).filter(ImageFilter.GaussianBlur(2)),str(title),H=int(five00_h),W=int(five00_w)))
            init_player._config(track=title,album=album,artist=artist,art=artwork,backup_track=song[0],hoverimg=artwork_blur)
            init_player.img = artwork
            init_player.img = artwork_blur
        
        except IndexError:
            init_player._config(track=title,album=album,art=[],backup_track=song[0])

    else:
        # print('else')
        # print(song_list.curselection())
        song = song_info[curselect]
        pygame.mixer.music.load(song[1])
        pygame.mixer.music.play()
        started = True
        tag = ID3(song[1])
        title = tag.get('TIT2')
        album = tag.get('TALB')
        artist = tag.get('TPE1')
        try:
            art = tag.getall('APIC')[0].data
            im = Image.open(BytesIO(art)).resize((int(five00_w),int(five00_h)),Image.ANTIALIAS).convert('RGB')
            artwork = ImageTk.PhotoImage(im)  
            artwork_blur = ImageTk.PhotoImage(drawer(im.filter(ImageFilter.GaussianBlur(5)),str(title),W=int(five00_w),H=int(five00_h)))
            init_player._config(track=title,album=album,art=artwork,artist=artist,backup_track=song[0],hoverimg=artwork_blur)
            init_player.img = artwork
            init_player.img = artwork_blur
        
        except IndexError:
            init_player._config(track=title,album=album,artist=artist,art=[],backup_track=song[0])

    if started and not once:
        check_event()
        once = True

def directory():
    global count
    path = filedialog.askdirectory(title='Choose a directory with songs')
    song_paths = glob(path+'/*.mp3')

    for song_path in song_paths:
        song = os.path.basename(song_path).split('.')[0]
        song_list.insert('end', song)
        song_info[count] = [song, song_path]
        count += 1
    status_bar.config(text=f'Current song count: {song_list.size()}')

def file():
    global count
    
    path = filedialog.askopenfilenames(title='Choose song files',filetypes=(('MP3 files','*.mp3'),))
    for song_path in path:
        song = os.path.basename(song_path).split('.')[0]
        song_list.insert('end', song)
        song_info[count] = [song, song_path]
        count += 1

    status_bar.config(text=f'Current song count: {song_list.size()}')

def callback(*args):
    global updated_count, updated_info, searched
    # print(searchbar.acquire())
    if searchbar.get() != '':
        song_list.delete(0,'end')
        for item in song_info.values():
            if searchbar.get().lower() in item[0].lower():
                updated_info[updated_count] = [item[0], item[1]]
                song_list.insert('end', item[0])
                # print(updated_info)
                updated_count += 1
                searched = True

        else:
            updated_count = 0
        status_bar.config(text=f'Current song count: {song_list.size()}')

    else:
        song_list.delete(0,'end')
        searched = False
        for item in song_info.values():
            song_list.insert('end', item[0])

def play_song():
    global started

    if not started:
        pygame.mixer.music.unpause()
        started = True
    else:
        pygame.mixer.music.pause()
        started = False

def next_song():
    try:
        idx = song_list.curselection()[0]
        song_list.selection_clear(0,'end')
        song_list.selection_set(idx+1)
        song_list.activate(idx+1)
        play(curselect=song_list.curselection()[0])
    
    except IndexError:
        idx = 0
        song_list.selection_clear(0,'end')
        song_list.selection_set(idx)
        song_list.activate(idx)
        try:
            play(curselect=idx)
        except KeyError:
            pass
    
def prev_song():
    try:
        idx = song_list.curselection()[0]
        song_list.selection_clear(0,'end')
        song_list.selection_set(idx-1)
        song_list.activate(idx-1)
        play(curselect=song_list.curselection()[0])
    except IndexError:
        idx = 0
        song_list.selection_clear(0,'end')
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
            next_song()
    root.after(100,check_event)

def ret_event():
    try:
        idx = song_list.curselection()[0]
        play(idx)
    except IndexError:
        pass

def empty():
    global song_info, count
    song_list.delete(0,'end')
    pygame.mixer.music.pause()
    song_info = {}
    searchbar.delete(0,'end')
    count = 0
    status_bar.config(text=f'Current song count: {song_list.size()}')
    reset()

def reset():
    init_player._config(track='-',album='-',art=[],artist='-')

heading_label = tk.Label(root,text='Mplayer',font=font_title)
heading_label.grid(row=0,column=0,columnspan=2,pady=pady_15)

left_frame = tk.Frame(root)
left_frame.grid(row=1,column=0,padx=(padx_100,padx_10)) #padx=10

search_label = tk.Label(left_frame,text='Search song from your list:',font=font_headers)
search_label.grid(row=0,column=0,columnspan=2,sticky='w')

song_list_label = tk.Label(left_frame,text='Song list:',font=font_headers)
song_list_label.grid(row=2,column=0,sticky='w',columnspan=2,pady=(pady_15,pady_5)) #pady=15,5

search = tk.StringVar()
searchbar = ttk.Entry(left_frame, font=(0, 15), textvariable=search)
searchbar.grid(row=1, column=0, sticky='ew', columnspan=3)

song_list_frame = tk.Frame(left_frame)
song_list_frame.grid(row=3, column=0, columnspan=3)

song_list = tk.Listbox(song_list_frame, width=int(fifty_w), font=(0, 15),takefocus=0,
                        highlightthickness=0,selectborderwidth=0,activestyle='dotbox',
                        relief='flat')
song_list.pack()

sb_v = tk.Scrollbar(song_list_frame)
sb_v.pack(side='right', fill='y', before=song_list)

sb_h = tk.Scrollbar(song_list_frame, orient='horizontal')
sb_h.pack(fill='x')

song_list.config(yscrollcommand=sb_v.set)
song_list.config(xscrollcommand=sb_h.set)
sb_v.config(command=song_list.yview)
sb_h.config(command=song_list.xview)

ttk.Button(left_frame, text='Add a song directory',command=directory).grid(row=4, column=0,ipady=pady_5,pady=pady_5)
ttk.Button(left_frame, text='Add a song file', command=file).grid(row=4, column=1,ipady=pady_5,pady=pady_5)
ttk.Button(left_frame, text='Empty the list', command=empty).grid(row=4, column=2,ipady=pady_5,pady=pady_5)

song_list.bind('<Double-Button-1>', lambda e: play(curselect=song_list.curselection()[0]))
search.trace('w', callback)

right_frame = tk.Frame(root)
right_frame.grid(row=1,column=1,padx=int(padx_100),pady=pady_10)

init_player = Player(right_frame,artist='-',album='-',track='-',
                        playfunc=lambda: play_song(),previousfunc=lambda :prev_song()
                        ,nextfunc=lambda: next_song(),stopfunc=lambda: rewind())
init_player.grid(row=0,column=0)

status_bar = tk.Label(root,text='Current song count: 0',relief='sunken',anchor='w')
status_bar.grid(row=2,column=0,columnspan=2,sticky='ew')

MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)

root.bind('<Left>',lambda e:prev_song())
root.bind('<space>',lambda e:play_song())
root.bind('<Right>',lambda e:next_song())
try:
    root.bind('<Return>',lambda e:play(song_list.curselection()[0]))
except IndexError:
    pass


root.mainloop()