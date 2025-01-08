import os
import sys
import pytest
import logging
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.browser_manager import BrowserManager
from src.registration_page import RegistrationPage
from src.page_analyzer import PageAnalyzer
from config.config import BASE_URL

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_registration.log'),
        logging.StreamHandler()
    ]
)

class TestRegistration:
    @pytest.fixture(autouse=True)
    def setup(self):
        """测试设置"""
        try:
            logging.info("开始初始化测试环境")
            self.browser_manager = BrowserManager()
            self.driver = self.browser_manager.init_browser()
            self.registration_page = RegistrationPage(self.browser_manager)
            self.page_analyzer = PageAnalyzer(self.driver)
            logging.info("测试环境初始化完成")
            yield
        except Exception as e:
            logging.error(f"测试环境初始化失败: {str(e)}")
            raise
        finally:
            logging.info("清理测试环境")
            self.browser_manager.close_browser()
            
    def generate_test_email(self):
        """生成测试邮箱"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"test.user{timestamp}@example.com"
        
    def test_registration_flow(self):
        """测试注册流程"""
        try:
            # 访问主页
            logging.info(f"访问网站: {BASE_URL}")
            self.driver.get(BASE_URL)
            
            # 分析主页
            logging.info("分析主页元素")
            self.page_analyzer.capture_page_state("homepage")
            signup_selectors = self.page_analyzer.suggest_selectors("Sign up")
            logging.info(f"找到的注册按钮选择器: {signup_selectors}")
            
            # 导航到注册页面
            logging.info("点击注册按钮")
            self.registration_page.navigate_to_signup()
            
            # 分析注册页面
            logging.info("分析注册页面元素")
            self.page_analyzer.capture_page_state("registration_page")
            
            # 填写注册表单
            test_email = self.generate_test_email()
            logging.info(f"填写注册表单，使用邮箱: {test_email}")
            self.registration_page.fill_registration_form(
                first_name="Test",
                last_name="User",
                email=test_email
            )
            
            # 分析填写后的表单
            logging.info("分析填写后的表单")
            self.page_analyzer.capture_page_state("filled_form")
            continue_selectors = self.page_analyzer.suggest_selectors("Continue")
            logging.info(f"找到的继续按钮选择器: {continue_selectors}")
            
            # 点击继续
            logging.info("点击继续按钮")
            self.registration_page.click_continue()
            
            # 分析验证码页面
            logging.info("分析验证码页面")
            self.page_analyzer.capture_page_state("captcha_page")
            
            # 处理验证码
            logging.info("处理验证码")
            self.registration_page.handle_captcha()
            
            # 验证注册结果
            logging.info("验证注册结果")
            current_url = self.driver.current_url
            assert "signup" not in current_url.lower(), "注册未完成"
            
            # 分析最终页面
            logging.info("分析最终页面")
            self.page_analyzer.capture_page_state("final_page")
            logging.info("注册流程测试完成")
            
        except Exception as e:
            logging.error(f"测试过程中出现错误: {str(e)}")
            # 保存当前页面状态
            self.page_analyzer.capture_page_state("error_state")
            raise 