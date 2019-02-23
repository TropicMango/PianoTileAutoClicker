from pynput import keyboard, mouse
from mss import mss
from PIL import Image
import sys
import time

kControl = keyboard.Controller()
mControl = mouse.Controller()
up = 190
down = 960
left = 1680
right = 2185
stop = False


def on_press(key):
    print('{0} pressed'.format(
        key))
    if key == keyboard.Key.shift_r:
        mControl.click(mouse.Button.left)
        scan()


def scan():
    latest = -1
    score = 0
    while True:
        start_time = time.time()
        found = False
        im = capture_screenshot()
        i = down - 10
        while i > 250 and not found:
            y_cord = i
            for x in range(4):
                # print(left + 63 + 126*x, i)
                val = im.getpixel((left + 63 + 126*x, i))
                if val == (0, 0, 0):
                    x_cord = left + 63 + 126*x
                    found = True
                    # print('black! at {}, {}'.format(x_cord, y_cord))
                    break
            i -= 1
        if mControl.position[1] < 20:
            print('terminate')
            return
        if found and latest != x_cord:
            mControl.position = (x_cord, y_cord + score*100/1420 - 30)
            mControl.click(mouse.Button.left)
            latest = x_cord
            score += 1
            print('none')
        else:
            print('none')
        im.close()
        # print('run time: {}'.format(time.time() - start_time))
        # time.sleep(0)


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        stop = True
        sys.exit()
        return False


def capture_screenshot():
    # Capture entire screen
    with mss() as sct:
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


if __name__ == '__main__':
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()
