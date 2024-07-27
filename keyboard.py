import pyautogui
import time

def hold_key(key, duration):
    print(f"Holding '{key}' key for {duration} seconds...")
    pyautogui.keyDown(key)  # Press the key down
    time.sleep(duration)    # Hold the key down for the specified duration
    pyautogui.keyUp(key)    # Release the key
    print(f"Released '{key}' key.")
#TODO - investigate this a bit more 

if __name__ == "__main__":
    key_to_hold = 'up'
    while True: 
        hold_duration = 5  # duration in seconds
        hold_key(key_to_hold, hold_duration)

