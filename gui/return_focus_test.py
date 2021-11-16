import win32api, win32com.client, win32gui, time


# this_handle = win32gui.GetForegroundWindow()
# print('start this_handle', this_handle, type(this_handle))
# win32gui.SetActiveWindow(197222)
# time.sleep(2)
# print('slept')
# print('current forground', win32gui.GetForegroundWindow(), 'this_handle', this_handle)
# shell = win32com.client.Dispatch("WScript.Shell")
# shell.SendKeys('%')
# win32gui.SetActiveWindow(this_handle)

for i, j in zip(range(3), range(3)):
    print(i, j)