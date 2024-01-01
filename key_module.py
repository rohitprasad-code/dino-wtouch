import pynput.keyboard as kb

def on_press(key):
    # print(key)
    if key == kb.Key.esc:
        return False

def on_release(key):
    print(key)
    if key == kb.Key.esc:
        return False

def press_key(key):
    controller = kb.Controller()
    controller.press(key)

def release_key(key):
    controller = kb.Controller()
    controller.release(key)

# with kb.Listener(on_press=on_press, on_release=on_release) as listener:
#     listener.join()