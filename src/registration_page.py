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
            (By.CSS_SELECTOR, "[href*='register']"),
            # 添加基于分析结果的新选择器
            (By.CSS_SELECTOR, "a.group.relative.rounded-xl"),
            (By.CSS_SELECTOR, "button.group.relative.rounded-xl"),
            (By.CSS_SELECTOR, "a[href='/signup']"),
            (By.CSS_SELECTOR, "a[href='/register']")
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
        first_name_selectors = [
            (By.CSS_SELECTOR, "input[name='firstName'], input[placeholder*='First']"),
            (By.CSS_SELECTOR, "input[type='text']:first-child"),
            (By.CSS_SELECTOR, "input.form-input:first-of-type")
        ]
        
        first_name_input = None
        for selector in first_name_selectors:
            try:
                first_name_input = self.browser.wait_for_element(selector)
                if first_name_input and first_name_input.is_displayed():
                    break
            except:
                continue
                
        if not first_name_input:
            raise Exception("无法找到名字输入框")
            
        self.mouse.move_to_element(first_name_input)
        self.mouse.click_element()
        self.mouse.type_text(first_name)
        
        # 填写姓氏
        last_name_selectors = [
            (By.CSS_SELECTOR, "input[name='lastName'], input[placeholder*='Last']"),
            (By.CSS_SELECTOR, "input[type='text']:nth-child(2)"),
            (By.CSS_SELECTOR, "input.form-input:nth-of-type(2)")
        ]
        
        last_name_input = None
        for selector in last_name_selectors:
            try:
                last_name_input = self.browser.wait_for_element(selector)
                if last_name_input and last_name_input.is_displayed():
                    break
            except:
                continue
                
        if not last_name_input:
            raise Exception("无法找到姓氏输入框")
            
        self.mouse.move_to_element(last_name_input)
        self.mouse.click_element()
        self.mouse.type_text(last_name)
        
        # 填写邮箱
        email_selectors = [
            (By.CSS_SELECTOR, "input[type='email'], input[name='email']"),
            (By.CSS_SELECTOR, "input[placeholder*='email']"),
            (By.CSS_SELECTOR, "input.form-input[type='email']")
        ]
        
        email_input = None
        for selector in email_selectors:
            try:
                email_input = self.browser.wait_for_element(selector)
                if email_input and email_input.is_displayed():
                    break
            except:
                continue
                
        if not email_input:
            raise Exception("无法找到邮箱输入框")
            
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
            (By.CSS_SELECTOR, ".submit-button, .continue-button"),
            # 添加基于分析结果的新选择器
            (By.CSS_SELECTOR, "button.group.relative.rounded-xl"),
            (By.CSS_SELECTOR, "button[type='submit'].primary-button")
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
        
        # 尝试通过多种方式定位验证码框
        selectors = [
            (By.CSS_SELECTOR, "iframe[title*='reCAPTCHA']"),
            (By.CSS_SELECTOR, "iframe[src*='recaptcha']"),
            (By.CSS_SELECTOR, ".g-recaptcha iframe")
        ]
        
        captcha_frame = None
        for selector in selectors:
            try:
                captcha_frame = self.browser.wait_for_element(selector)
                if captcha_frame and captcha_frame.is_displayed():
                    break
            except:
                continue
                
        if captcha_frame:
            # 切换到验证码框架
            self.driver.switch_to.frame(captcha_frame)
            
            # 尝试点击复选框
            checkbox_selectors = [
                (By.CSS_SELECTOR, ".recaptcha-checkbox-border"),
                (By.ID, "recaptcha-anchor")
            ]
            
            for selector in checkbox_selectors:
                try:
                    checkbox = self.browser.wait_for_element(selector)
                    if checkbox and checkbox.is_displayed():
                        self.mouse.move_to_element(checkbox)
                        self.mouse.click_element()
                        break
                except:
                    continue
                    
            # 切回主框架
            self.driver.switch_to.default_content()
        else:
            # 如果找不到reCAPTCHA，尝试使用图像识别
            captcha_box = self.image_recognizer.find_element_by_image("captcha_box.png")
            if captcha_box:
                self.mouse.move_to_element(captcha_box)
                self.mouse.click_element() 