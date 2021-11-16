# cd github/pete88b/expoco/gui
# https://tkdocs.com/tutorial/intro.html
from tkinter import *
from tkinter import ttk
import win32api, win32con, win32gui, time
from PIL import Image, ImageTk

time.sleep(1)
print('get on with it')

print(Tcl().eval('info patchlevel'))

# 1st test
# tkinter._test()

# 2nd test
# root = Tk()
# Button(root, text='not again!').grid()
# root.mainloop()

# "real" app - see https://tkdocs.com/tutorial/firstexample.html
root = Tk()
# root.overrideredirect(True) # hide title bar

key_position = 'left'
if key_position == 'left':
    mainframe_sticky = E
    key_column = 0
    img_column = 1
else:
    mainframe_sticky = W
    key_column = 1
    img_column = 0

mainframe = ttk.Frame(root, padding=5)
mainframe.grid(column=0, row=0, sticky=mainframe_sticky) # (N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(mainframe, padding=5)
frame.grid(column=key_column, row=0)
ttk.Label(frame, text="L: Left Click").grid(column=0, row=0, sticky=W)
ttk.Label(frame, text="R: Right Click").grid(column=0, row=1, sticky=W)
ttk.Label(frame, text="D: Double Click").grid(column=0, row=2, sticky=W)
image = ImageTk.PhotoImage(Image.new('1', (1000,500), color = 'white'))
w = ttk.Label(mainframe, image=image)
w.grid(column=img_column, row=0)
# image = PhotoImage(file='img.png')
# def _w(c, r):
#     t=f"{c}, {r}"
#     w = ttk.Label(mainframe, image=image)
#     w.grid(column=c, row=r)
#     w.bind('<Enter>', lambda _event: print(f"enter {t}"))
#     w.bind('<Leave>', lambda _event: print(f"leave {t}"))
# for c in range(3):
#     for r in range(3):
#         _w(c, r)

# for child in mainframe.winfo_children():
#     child.grid_configure(padx=5, pady=5)

root.bind("<Return>", lambda _event: print('return pressed - might be useful'))

root.attributes('-alpha', 0.9) # we can easily make the whole thing semi-transparent
root.attributes('-transparentcolor', 'white')
root.bind("<Escape>", lambda _event: root.destroy())
root.bind("<FocusOut>", lambda _event: root.destroy())
root.attributes('-toolwindow', True)

print('win32api.GetCursorPos()', win32api.GetCursorPos(), 'root.winfo_id()', root.winfo_id())

# cursor_pos = win32api.GetCursorPos()
# root.geometry(f"300x200+{cursor_pos[0]}+{cursor_pos[1]}")
# root.geometry(f"+{cursor_pos[0]}+{cursor_pos[1]}")
root.attributes("-topmost", True)
root.attributes('-fullscreen', True)
def _click():
    print('click')
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,10,10)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,10,10)

root.after(10, _click)
# root.focus() # no good
# root.update() # no good
# win32gui.SetForegroundWindow(root.winfo_id()) # no good

root.bind('a', lambda _: print('a pressed'))

root.mainloop()