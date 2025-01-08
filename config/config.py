from pathlib import Path
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 基础URL配置
BASE_URL = "https://www.cusror.com/"

# 页面元素等待时间配置
WAIT_TIME = 20
CLICK_DELAY = 2

# 图像识别配置
CONFIDENCE_LEVEL = 0.8

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# 资源目录
RESOURCES_DIR = ROOT_DIR / "resources"
IMAGES_DIR = RESOURCES_DIR / "images" 