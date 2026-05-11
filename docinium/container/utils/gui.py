import time
import loguru
import pyautogui
from utils.logger_config import logger

class ScreenController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()

    # Mouse control methods
    def move_mouse(self, x, y):
        pyautogui.moveTo(x, y)

    def click_mouse(self, x, y):
        self.move_mouse(x,y)
        pyautogui.click(x, y)
        logger.debug("Executed click successfully")

    def click_based_on_image(self, image_base64):
        location = pyautogui.locateOnScreen(image_base64, confidence=0.8)
        if location:
            pyautogui.click(location)
        else:
            logger.warning(f"Image '{image_base64}' not found on the screen.")

    # Keyboard control methods
    def type_text(self, text):
        pyautogui.typewrite(text)

    def press_key(self, key):
        pyautogui.press(key)

    # Screen information method
    def get_screen_size(self):
        return self.screen_width, self.screen_height