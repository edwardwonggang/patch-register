import pyautogui
import random
import time
from config.config import CLICK_DELAY

class MouseController:
    @staticmethod
    def move_to_element(element):
        """模拟人类移动鼠标到元素位置"""
        location = element.location
        size = element.size
        target_x = location['x'] + size['width'] // 2
        target_y = location['y'] + size['height'] // 2
        
        # 添加随机偏移
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
        
        pyautogui.moveTo(
            target_x + offset_x,
            target_y + offset_y,
            duration=random.uniform(0.5, 1.5)
        )
        
    @staticmethod
    def click_element():
        """模拟人类点击动作"""
        time.sleep(random.uniform(0.1, 0.3))
        pyautogui.click()
        time.sleep(CLICK_DELAY)
        
    @staticmethod
    def type_text(text):
        """模拟人类输入文字"""
        for char in text:
            pyautogui.typewrite(char)
            time.sleep(random.uniform(0.1, 0.3)) 