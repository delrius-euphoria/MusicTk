import tkinter as tk
import pyglet
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageFont


class Player(tk.Frame):
    def __init__(self,root,track='',backup_track='',artist='',album=None,art=None,playfunc=None,stopfunc=None,nextfunc=None,previousfunc=None,backfunc=None,forwardfunc=None,bindfunc=None,**kwargs):
        tk.Frame.__init__(self,root,**kwargs)

        pyglet.font.add_file("fonts/Montserrat-SemiBold.ttf")
        pyglet.font.add_file('fonts/Poppins-SemiBold.ttf')
        
        self.art          = art
        self.playfunc     = playfunc
        self.stopfunc     = stopfunc
        self.nextfunc     = nextfunc
        self.previousfunc = previousfunc
        self.backfunc     = backfunc
        self.forwardfunc  = forwardfunc
        self.bindfunc     = bindfunc
        self.track        = track
        self.backup_track = backup_track
        self.artist       = artist
        self.album        = album
        self.count        = 0
        self.font_headers = ('Poppins SemiBold',15)

        self.h,self.w       = self.winfo_screenheight(),self.winfo_screenwidth()
        self.dy_w,self.dy_h = int(self.w/38.4),int(self.h/21.6)
        self.five00_w = self.w/3.84
        self.five00_h = self.h/2.16
        self.padx_5   = self.w/384
        self.padx_10  = self.w/192
        self.padx_100 = self.w/19.2
        self.pady_5   = self.h/216
        self.pady_10  = self.h/108
        self.pady_15  = self.h/72
        self.rf_w     = self.w/3.80
        self.rf_h     = self.h/1.44

        self.previous  = ImageTk.PhotoImage(Image.open('images/previous.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.backwards = ImageTk.PhotoImage(Image.open('images/backwards.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.forwards  = ImageTk.PhotoImage(Image.open('images/forwards.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.next      = ImageTk.PhotoImage(Image.open('images/next.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.notfound  = ImageTk.PhotoImage(Image.open('images/notfound.png').resize((int(self.five00_w),int(self.five00_h)),Image.ANTIALIAS))
        self.playpause = ImageTk.PhotoImage(Image.open('images/play pause.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))
        self.stop      = ImageTk.PhotoImage(Image.open('images/rewind.png').resize((self.dy_w,self.dy_h),Image.ANTIALIAS))

        self.img_label = tk.Label(self)
        self.img_label.grid(row=0,column=0,columnspan=4,pady=self.pady_10)

        self.title_label = tk.Label(self,text=self.track,font=self.font_headers)
        self.title_label.grid(row=1,column=0,columnspan=4,pady=self.pady_5)

        self.artist_label = tk.Label(self,text=self.artist,font=self.font_headers)
        self.artist_label.grid(row=2,column=0,columnspan=4,pady=self.pady_5)

        self.album_label = tk.Label(self,text=self.album,font=self.font_headers)
        self.album_label.grid(row=3,column=0,columnspan=4,pady=self.pady_5)

        self.previous_button = ttk.Button(self,image=self.previous,command=self._previous)
        self.previous_button.grid(row=4,column=0)

        self.playpause_button = ttk.Button(self,image=self.playpause,command=self._play)
        self.playpause_button.grid(row=4,column=1)

        self.next_button = ttk.Button(self,image=self.next,command=self._next)
        self.next_button.grid(row=4,column=2)

        self.rewind_button = ttk.Button(self,image=self.stop,command=self._stop)
        self.rewind_button.grid(row=4,column=3)

        if not art:
            self.img_label.config(image=self.notfound)

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
        
    def config(self,track='',album='',art=None,artist='',backup_track=''):
        if not art:
            self.img_label.config(image=self.notfound)
        else:
            self.im_tk = ImageTk.PhotoImage(art)
            self.img_label.config(image=self.im_tk)
        
        if track is None:
            track = self._resize(30,str(backup_track))
            self.title_label.config(text=track)
        else:
            track = self._resize(30,str(track))
            self.title_label.config(text=track)
        
        if album is None:
            self.album_label.config(text='-')
        else:
            album = self._resize(30,str(album))
            self.album_label.config(text=album)
        
        if artist is None:
            self.artist_label.config(text='-')
        else:
            artist = self._resize(30,str(artist))
            self.artist_label.config(text=artist)

        self.blur_im_lst = self.__create_hover_lst(art,track) if art else None
        self.ublr_im_lst = self.blur_im_lst[::-1] if self.blur_im_lst is not None else None
        self.art = art

        self.img_label.bind('<Enter>',lambda e: self.enter())
        self.img_label.bind('<Leave>',lambda e: self.leave())

    def enter(self):
        if self.art:
            if self.count < len(self.blur_im_lst):
                self.img_label.config(image=self.blur_im_lst[self.count])
                self.count += 1
                self.after(15,self.enter)
            else:
                self.count = 0
        else:
            self.img_label.config(image=self.notfound)

    def leave(self):
        if not self.art:
            self.img_label.config(image=self.notfound)
        else:
            if self.count < len(self.ublr_im_lst):
                self.img_label.config(image=self.ublr_im_lst[self.count])
                self.count += 1
                self.after(15,self.leave)
            else:
                self.img_label.config(image=self.im_tk)
                self.count = 0

    def drawer(self,img,text,W,H):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font='fonts/Poppins-SemiBold.ttf',size=25)
        if len(text) > 30:
            text = text[:30] + '...'
        w, h = draw.textsize(text,font=font)
        draw.text(((W-w)/2,(H-h)/2), text, font=font,fill="white",align='left')
        return img

    def __create_hover_lst(self,art,title):
        im_lst = []
        black = Image.new('RGBA',(500,500),(0,0,0,50))
        art.paste(black,mask=black)

        for i in range(1,9):
            num      = i/2
            blur_img = art.filter(ImageFilter.GaussianBlur(num))
            art_blur = ImageTk.PhotoImage(blur_img)
            if i == 8:
                draw     = self.drawer(blur_img.resize((500,499),Image.ANTIALIAS),str(title),H=500,W=500)
                art_blur = ImageTk.PhotoImage(draw)
            
            im_lst.append(art_blur)
        
        return im_lst

steps = '''Step 1: Make sure your songs files are in the form of Artist - Song Name.
Step 2: Make a folder for the output of new song files.
Step 3: Wait while the label says processing.
Step 4: You are good to go once the label says Done.
If it takes long time for single file close the main app and try again.
Keep in mind the app is still in beta and data might be inaccurate.'''

if __name__ == "__main__":
    root = tk.Tk()
    
    a = Player(root,track='Hello',album='Get lost',playfunc=lambda: print('PLAYING'),stopfunc=lambda: print('STOPPING'))
    a.pack()

    root.mainloop()
