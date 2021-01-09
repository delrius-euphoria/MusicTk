import tkinter as tk
from PIL import Image, ImageTk
import pyglet

class Player(tk.Frame):
    def __init__(self,root,track='',backup_track='',artist='',album=None,art=None,playfunc=None,stopfunc=None,nextfunc=None,previousfunc=None,backfunc=None,forwardfunc=None,bindfunc=None,**kwargs):
        tk.Frame.__init__(self,root,**kwargs)

        self.art = art
        self.playfunc = playfunc
        self.stopfunc = stopfunc
        self.nextfunc = nextfunc
        self.previousfunc = previousfunc
        self.backfunc = backfunc
        self.forwardfunc = forwardfunc
        self.bindfunc = bindfunc
        self.track = track
        self.backup_track = backup_track
        self.artist = artist
        self.album = album
        
        pyglet.font.add_file('fonts/kenyan coffee rg.ttf')
        pyglet.font.add_file('fonts/Poppins-SemiBold.ttf')
        self.font_headers = ('kenyan coffee rg',20)
        self.font_hover = ('Poppins SemiBold',15)

        self.h,self.w = self.winfo_screenheight(),self.winfo_screenwidth()
        self.dy_w,self.dy_h = int(self.w/38.4),int(self.h/21.6)
        five00_w = self.w/3.84
        five00_h = self.h/2.16
        padx_5 = self.w/384
        padx_10 = self.w/192
        padx_100 = self.w/19.2
        pady_5 = self.h/216
        pady_10 = self.h/108
        pady_15 = self.h/72
        rf_w = self.w/3.80
        rf_h = self.h/1.44

        self.previous = ImageTk.PhotoImage(Image.open('images/previous.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.backwards = ImageTk.PhotoImage(Image.open('images/backwards.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.forwards = ImageTk.PhotoImage(Image.open('images/forwards.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.next = ImageTk.PhotoImage(Image.open('images/next.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.notfound = ImageTk.PhotoImage(Image.open('images/notfound.png').resize((int(five00_w),int(five00_h)),Image.ANTIALIAS))
        self.playpause = ImageTk.PhotoImage(Image.open('images/play pause.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.stop = ImageTk.PhotoImage(Image.open('images/rewind.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))

        self.img_label = tk.Label(self)
        self.img_label.grid(row=0,column=0,columnspan=4,pady=pady_10)

        self.title_label = tk.Label(self,text=self.track,font=self.font_headers)
        self.title_label.grid(row=1,column=0,columnspan=4,pady=pady_5)

        self.artist_label = tk.Label(self,text=self.artist,font=self.font_headers)
        self.artist_label.grid(row=2,column=0,columnspan=4,pady=pady_5)

        self.album_label = tk.Label(self,text=self.album,font=self.font_headers)
        self.album_label.grid(row=3,column=0,columnspan=4,pady=pady_5)

        self.previous_button = tk.Button(self,image=self.previous,relief='flat',command=self._previous)
        self.previous_button.grid(row=4,column=0)

        self.playpause_button = tk.Button(self,image=self.playpause,relief='flat',command=self._play)
        self.playpause_button.grid(row=4,column=1)

        self.next_button = tk.Button(self,image=self.next,relief='flat',command=self._next)
        self.next_button.grid(row=4,column=2)

        self.rewind_button = tk.Button(self,image=self.stop,relief='flat',command=self._stop)
        self.rewind_button.grid(row=4,column=3)

        if not art:
            self.img_label.config(image=self.notfound)
        
        # self.grid_propagate(0)

    def _play(self):
        if self.playfunc:
            self.playfunc()

    def _stop(self):
        if self.stopfunc:
            self.stopfunc()

    def _previous(self):
        if self.previousfunc:
            self.previousfunc()
    
    def _next(self):
        if self.nextfunc:
            self.nextfunc()
    
    def _backwards(self):
        if self.backfunc:
            self.backfunc()    
    
    def _forwards(self):
        if self.forwardfunc:
            self.forwardfunc()
    
    def _resize(self,lim,text=''):
        if len(text) > lim:
            new_text = text[:lim] + '...'
            return new_text
        else:
            return text
        
    def _config(self,track='',album='',art=None,artist='',backup_track='',hoverimg=None):
    
        if art == []:
            self.img_label.config(image=self.notfound)
        else:
            self.img_label.config(image=art)
        if track == None:
            backup_track = self._resize(30,str(backup_track))
            self.title_label.config(text=backup_track)
        else:
            track = self._resize(30,str(track))
            self.title_label.config(text=track)
        if album == None:
            self.album_label.config(text='-')
        else:
            album = self._resize(30,str(album))
            self.album_label.config(text=album)
        if artist == None:
            self.artist_label.config(text='-')
        else:
            artist = self._resize(30,str(artist))
            self.artist_label.config(text=artist)
        # if track != None or album != None or art != [] or artist != None:
        #     lim = 30
        #     print(len(str(track)))
        #     if len(str(track)) > lim:
        #         track = str(track)[:lim] + '...'
        #         self.title_label.config(text=track)
        #     if len(str(album)) > lim:
        #         album = str(album)[:lim] + '...'
        #         self.album_label.config(text=album)
        #     if len(str(artist)) > lim:
        #         artist = str(artist)[:lim] + '...'
        #         self.artist_label.config(text=artist)
        #     if art != []:
        #         self.img_label.config(image=art)

        self.img_label.bind('<Enter>',lambda e:self.enter(hoverimg=hoverimg))
        self.img_label.bind('<Leave>',lambda e:self.leave(normalimg=art))

    def enter(self,hoverimg):
        # print(hoverimg)
        self.img_label.config(image=hoverimg)
        # print('YES')
        # self.img_label.img = hoverimg
    
    def leave(self,normalimg):
        if not normalimg:
            self.img_label.config(image=self.notfound)
        else:
            self.img_label.config(image=normalimg)
        # print('nO')
        # self.img_label.img = normalimg

if __name__ == "__main__":
    root = tk.Tk()
    
    a = Player(root,track='Hello',album='Get lost',playfunc=lambda: print('PLAYING'),stopfunc=lambda: print('STOPPING'))
    a.pack()

    root.mainloop()
