import pynput.keyboard as kb

def on_press(key):
    print(key)
    if key == kb.Key.esc:
        return False
    
def on_release(key):
    print(key)
    if key == kb.Key.esc:
        return False

def press_key(key):
    with kb.press(key):
        pass
    
with kb.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    