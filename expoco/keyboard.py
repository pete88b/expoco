# AUTOGENERATED! DO NOT EDIT! File to edit: 30_keyboard.ipynb (unless otherwise specified).

__all__ = ['KeyboardABC', 'new_windows_keyboard']

# Cell
import time
from abc import ABC,abstractmethod

# Cell
class KeyboardABC(ABC):
    @abstractmethod
    def was_key_pressed(self, character):
        "Return `True` if the key for `character` was pressed"

    def which_key_was_pressed(self, characters='0123456789'):
        result = None
        for c in characters:
            if self.was_key_pressed(c):
                assert result is None, 'Expected a single key press but multiple keys were pressed'
                result = c
        return result

    def after_key_press(self, callback_fn, characters='0123456789'):
        # "flush" old key presses
        self.was_key_pressed('ESC')
        for c in characters: self.was_key_pressed(c)
        # now we can start listening
        while True:
            if self.was_key_pressed('ESC'):
                print('Quitting')
                break
            key_pressed = self.which_key_was_pressed(characters)
            if key_pressed is not None:
                callback_fn(key_pressed)
            time.sleep(.1)

# Cell
def new_windows_keyboard():
    import win32api, win32con
    class WindowsKeyboard(KeyboardABC):
        def was_key_pressed(self, character):
            v_key = win32con.VK_ESCAPE if character=='ESC' else ord(character)
            return True if win32api.GetAsyncKeyState(v_key) else False
    return WindowsKeyboard()