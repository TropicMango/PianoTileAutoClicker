from mss import mss
from PIL import Image
import time
import pyscreenshot as image_grab
from pynput import keyboard, mouse


mControl = mouse.Controller()


def on_press(key):
    print('{0} pressed'.format(
        key))
    if key == keyboard.Key.shift_r:
        print(mControl.position)


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        stop = True
        sys.exit()
        return False


if __name__ == '__main__':
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()