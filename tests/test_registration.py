import os
import sys
import pytest

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.browser_manager import BrowserManager
from src.registration_page import RegistrationPage
from config.config import BASE_URL

class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试设置"""
        self.browser_manager = BrowserManager()
        self.driver = self.browser_manager.init_browser()
        self.registration_page = RegistrationPage(self.browser_manager)
        yield
        self.browser_manager.close_browser()
        
    def test_registration_flow(self):
        """测试注册流程"""
        # 访问主页
        self.driver.get(BASE_URL)
        
        # 导航到注册页面
        self.registration_page.navigate_to_signup()
        
        # 填写注册表单
        self.registration_page.fill_registration_form(
            first_name="Test",
            last_name="User",
            email="test.user@example.com"
        )
        
        # 点击继续
        self.registration_page.click_continue()
        
        # 处理验证码（如果出现）
        self.registration_page.handle_captcha() 