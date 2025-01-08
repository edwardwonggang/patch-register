import cv2
import numpy as np
import pyautogui
from config.config import CONFIDENCE_LEVEL, IMAGES_DIR

class ImageRecognizer:
    @staticmethod
    def find_element_by_image(image_name):
        """通过图像模板匹配找到元素"""
        image_path = IMAGES_DIR / image_name
        try:
            location = pyautogui.locateOnScreen(
                str(image_path),
                confidence=CONFIDENCE_LEVEL
            )
            return location
        except pyautogui.ImageNotFoundException:
            return None
            
    @staticmethod
    def is_captcha_page(screenshot):
        """判断是否是验证码页面"""
        # 这里可以添加更复杂的图像识别逻辑
        return "captcha" in screenshot.lower()
        
    @staticmethod
    def is_password_page(screenshot):
        """判断是否是密码输入页面"""
        return "password" in screenshot.lower() 