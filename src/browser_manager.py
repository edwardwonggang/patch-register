from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import WAIT_TIME
import os

class BrowserManager:
    def __init__(self):
        self.driver = None
        
    def init_browser(self):
        """初始化Chrome浏览器"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")
        chrome_options.add_argument("--allow-insecure-localhost")
        chrome_options.add_argument("--disable-web-security")
        
        try:
            # 使用本地的ChromeDriver
            driver_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'drivers', 'chromedriver.exe')
            if not os.path.exists(driver_path):
                raise FileNotFoundError(f"ChromeDriver not found at {driver_path}")
                
            self.driver = webdriver.Chrome(
                service=Service(driver_path),
                options=chrome_options
            )
            self.driver.maximize_window()
            
            # 设置页面加载超时
            self.driver.set_page_load_timeout(30)
            # 设置脚本执行超时
            self.driver.set_script_timeout(30)
            
        except Exception as e:
            print(f"初始化浏览器失败: {str(e)}")
            raise
            
        return self.driver
        
    def wait_for_element(self, locator):
        """等待元素出现"""
        return WebDriverWait(self.driver, WAIT_TIME).until(
            EC.presence_of_element_located(locator)
        )
        
    def close_browser(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None 