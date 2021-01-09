import tkinter as tk
from tkinter import ttk

class PlaceholderEntry(ttk.Entry):
    '''
    Custom modern Placeholder Entry box, takes positional argument master and placeholder\n
    Use acquire() for getting output from entry widget\n
    Use shove() for inserting into entry widget\n
    Use remove() for deleting from entry widget\n
    Use length() for getting the length of text in the widget\n
    BUG 1: Possible bugs with binding to this class\n
    BUG 2: Anomalous behaviour with config or configure method
    '''

    def __init__(self, master, placeholder, **kwargs):
        # style for ttk widget
        self.s = ttk.Style()
        self.s.configure('my.TEntry', foreground='black', font=(0, 0, 'normal'))
        self.s.configure('placeholder.TEntry', foreground='grey', font=(0, 0, 'bold'))

        # init entry box
        ttk.Entry.__init__(self, master,style='my.TEntry', **kwargs)
        self.text = placeholder
        self.__has_placeholder = False  # placeholder flag

        # add placeholder if box empty
        self._add()

        # bindings of the widget
        self.bind('<FocusIn>', self._clear)
        self.bind('<FocusOut>', self._add)
        self.bind('<KeyRelease>',self._normal)

    def _clear(self, *args):  # method to remove the placeholder
        if self.get() == self.text and self.__has_placeholder:  # remove placeholder when focus gain
            self.delete(0, tk.END)
            self.configure(style='my.TEntry')
            self.__has_placeholder = False  # set flag to false

    def _add(self, *args):  # method to add placeholder
        if self.get() == '' and not self.__has_placeholder:  # if no text add placeholder
            self.configure(style='placeholder.TEntry')
            self.insert(0, self.text)  # insert placeholder
            self.icursor(0)  # move insertion cursor to start of entrybox
            self.__has_placeholder = True  # set flag to true

    def _normal(self, *args):  # method to set the text to normal properties
        self._add()  # if empty add placeholder
        if self.get() == self.text and self.__has_placeholder:  # clear the placeholder if starts typing
            self.bind('<Key>', self._clear)
            self.icursor(-1)  # keep insertion cursor to the end
        else:
            self.configure(style='my.TEntry')  # set normal font

    def acquire(self):  # custom method to get the text
        if self.get() == self.text and self.__has_placeholder:
            return 'None'
        else:
            return self.get()

    def shove(self, index, string):  # custom method to insert into entry
        self._clear()
        self.insert(index, string)

    def remove(self, first, last):  # custom method to remove from entry
        if self.get() != self.text:
            self.delete(first, last)
            self._add()
        elif self.acquire() == self.text and not self.__has_placeholder:
            self.delete(first, last)
            self._add()

    def length(self):
        if self.get() == self.text and self.__has_placeholder:
            return 0
        else:
            return len(self.get())

class ToolTip():
    '''
    Custom Tooltips, easy to use, specify widget and text as positional arguments\n
    Additional Arguments:\n
    triggerkey - Which key triggers the placeholder\n
    releasekey - Which key hides the placeholder\n
    bg - Background color of tooltip window(default-yellow-ish), accepts hex and standard colors\n
    fg - Foreground color/Font color of the text, accepts hex and standard colors\n
    fadeout - Default set to 'enabled', set to 'disabled' to disable fadeout of tooltip\n
    ISSUE: What if user want it on left side?
    '''

    def __init__(self, widget, text, triggerkey='<Enter>', releasekey='<Leave>', bg='#ffffe0', fg='black', side='Right', fadeout='enabled'):
        # basic widget attributes
        self.widget = widget
        self.text = text
        self.bg = bg
        self.side = side
        self.fg = fg
        self.fadeout = fadeout

        # making the tooltip
        self.master = tk.Toplevel(bg=self.bg)
        self.master.attributes('-alpha', 0)  # hide the window
        self.master.overrideredirect(1)
        self.master.attributes('-topmost', True)
        self.frame = tk.Frame(self.master, bg=self.bg, highlightbackground="black",
                              highlightcolor="black", highlightthickness=1)
        self.frame.pack(expand=1, fill='x')
        self.label = tk.Label(self.frame, text=self.text,
                              bg=self.bg, justify=tk.LEFT, fg=self.fg)
        self.label.grid(row=0, column=0)

        # widget binding
        self.widget.bind(triggerkey, self.add)
        self.widget.bind(releasekey, self.remove)
        self.widget.bind('<ButtonPress>', self.remove)

        # reference to window status
        self.hidden = True

    def add(self, event):
        if self.side == 'Right':
            # calculating offset
            offset_x = event.widget.winfo_width() + 2
            offset_y = int((event.widget.winfo_height() -
                            self.widget.winfo_height())/2)
            # get geometry
            w = self.label.winfo_width() + 10
            h = self.label.winfo_height() + 2
            self.x = event.widget.winfo_rootx() + offset_x
            self.y = event.widget.winfo_rooty() + offset_y
            # apply geometry
            self.master.geometry(f'{w}x{h}+{self.x}+{self.y}')
            # bringing the visibility of the window back
            self.master.attributes('-alpha', 1)
            self.hidden = False  # setting status to false

        else:
            offset_x = event.widget.winfo_width() - int(event.widget.winfo_width()*2.5)
            offset_y = int((event.widget.winfo_height() +
                            self.widget.winfo_height())/2)
            w = self.label.winfo_width() + 10
            h = self.label.winfo_height()
            self.x = event.widget.winfo_rootx() + offset_x
            self.y = event.widget.winfo_rooty()
            # apply geometry
            self.master.geometry(f'{w}x{h}+{self.x}+{self.y}')
            # bringing the visibility of the window back
            self.master.attributes('-alpha', 1)
            self.hidden = False  # setting status to false

    def remove(self, *args):
        if self.fadeout == 'enabled':  # if fadeout enabled

            if not self.hidden:  # if window is not hidden
                alpha = self.master.attributes('-alpha')
                if alpha > 0:
                    alpha -= 0.10
                    self.master.attributes('-alpha', alpha)
                    self.master.after(25, self.remove)

            else:
                self.master.attributes('-alpha', 0)  # hide the window

        elif self.fadeout == 'disabled':  # if fadeout disabled
            if not self.hidden:
                self.master.attributes('-alpha', 0)
                self.hidden = True

        else:
            raise tk.TclError('Unknown value for option -fadeout')

    def clear(self):
        self.master.destroy()