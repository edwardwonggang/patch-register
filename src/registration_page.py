from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .mouse_controller import MouseController
from .image_recognizer import ImageRecognizer
from config.config import WAIT_TIME
import time

class RegistrationPage:
    def __init__(self, browser_manager):
        self.browser = browser_manager
        self.mouse = MouseController()
        self.image_recognizer = ImageRecognizer()
        
    def navigate_to_signup(self):
        """导航到注册页面"""
        # 首先等待页面加载完成
        time.sleep(2)
        
        # 尝试多种方式定位注册按钮
        selectors = [
            (By.LINK_TEXT, "Sign up"),
            (By.PARTIAL_LINK_TEXT, "Sign"),
            (By.XPATH, "//a[contains(text(), 'Sign up')]"),
            (By.XPATH, "//button[contains(text(), 'Sign up')]"),
            (By.CSS_SELECTOR, "[href*='signup']"),
            (By.CSS_SELECTOR, "[href*='register']")
        ]
        
        signup_button = None
        for selector in selectors:
            try:
                signup_button = self.browser.wait_for_element(selector)
                if signup_button and signup_button.is_displayed():
                    break
            except:
                continue
                
        if not signup_button:
            raise Exception("无法找到注册按钮")
            
        self.mouse.move_to_element(signup_button)
        self.mouse.click_element()
        
    def fill_registration_form(self, first_name, last_name, email):
        """填写注册表单"""
        # 等待表单加载
        time.sleep(2)
        
        # 填写名字
        first_name_input = self.browser.wait_for_element(
            (By.CSS_SELECTOR, "input[name='firstName'], input[placeholder*='First']")
        )
        self.mouse.move_to_element(first_name_input)
        self.mouse.click_element()
        self.mouse.type_text(first_name)
        
        # 填写姓氏
        last_name_input = self.browser.wait_for_element(
            (By.CSS_SELECTOR, "input[name='lastName'], input[placeholder*='Last']")
        )
        self.mouse.move_to_element(last_name_input)
        self.mouse.click_element()
        self.mouse.type_text(last_name)
        
        # 填写邮箱
        email_input = self.browser.wait_for_element(
            (By.CSS_SELECTOR, "input[type='email'], input[name='email']")
        )
        self.mouse.move_to_element(email_input)
        self.mouse.click_element()
        self.mouse.type_text(email)
        
    def click_continue(self):
        """点击继续按钮"""
        # 尝试多种方式定位继续按钮
        selectors = [
            (By.XPATH, "//button[contains(text(), '继续')]"),
            (By.XPATH, "//button[contains(text(), 'Continue')]"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, ".submit-button, .continue-button")
        ]
        
        continue_button = None
        for selector in selectors:
            try:
                continue_button = self.browser.wait_for_element(selector)
                if continue_button and continue_button.is_displayed():
                    break
            except:
                continue
                
        if not continue_button:
            raise Exception("无法找到继续按钮")
            
        self.mouse.move_to_element(continue_button)
        self.mouse.click_element()
        
    def handle_captcha(self):
        """处理验证码"""
        # 等待验证码加载
        time.sleep(2)
        
        captcha_box = self.image_recognizer.find_element_by_image("captcha_box.png")
        if captcha_box:
            self.mouse.move_to_element(captcha_box)
            self.mouse.click_element() 