import os
import time
from datetime import datetime
from pathlib import Path
import json
import logging
from bs4 import BeautifulSoup

class PageAnalyzer:
    def __init__(self, driver, output_dir="page_analysis"):
        """
        初始化页面分析器
        :param driver: WebDriver实例
        :param output_dir: 输出目录
        """
        self.driver = driver
        self.output_dir = Path(output_dir)
        self.setup_directories()
        
    def setup_directories(self):
        """创建必要的目录结构"""
        directories = [
            self.output_dir,
            self.output_dir / "screenshots",
            self.output_dir / "source",
            self.output_dir / "elements"
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def capture_page_state(self, description=""):
        """
        捕获页面状态，包括截图、源代码和元素信息
        :param description: 状态描述
        :return: 保存的文件路径字典
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if description:
            timestamp = f"{timestamp}_{description}"
            
        try:
            # 保存截图
            screenshot_path = self.output_dir / "screenshots" / f"{timestamp}.png"
            self.driver.save_screenshot(str(screenshot_path))
            
            # 保存页面源代码
            source_path = self.output_dir / "source" / f"{timestamp}.html"
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
                
            # 分析并保存元素信息
            elements_info = self._analyze_elements()
            elements_path = self.output_dir / "elements" / f"{timestamp}.json"
            with open(elements_path, "w", encoding="utf-8") as f:
                json.dump(elements_info, f, ensure_ascii=False, indent=2)
                
            logging.info(f"页面状态已保存：{timestamp}")
            return {
                "screenshot": str(screenshot_path),
                "source": str(source_path),
                "elements": str(elements_path)
            }
            
        except Exception as e:
            logging.error(f"保存页面状态失败: {str(e)}")
            return None
            
    def _analyze_elements(self):
        """
        分析页面元素，返回可能的可交互元素信息
        :return: 元素信息字典
        """
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        elements_info = {
            "buttons": [],
            "inputs": [],
            "links": [],
            "forms": []
        }
        
        # 分析按钮
        buttons = soup.find_all(['button', 'input[type="button"]', 'input[type="submit"]'])
        for button in buttons:
            elements_info["buttons"].append({
                "text": button.get_text(strip=True),
                "type": button.name,
                "id": button.get("id", ""),
                "class": button.get("class", []),
                "name": button.get("name", "")
            })
            
        # 分析输入框
        inputs = soup.find_all(['input[type="text"]', 'input[type="email"]', 'input[type="password"]'])
        for input_elem in inputs:
            elements_info["inputs"].append({
                "type": input_elem.get("type", ""),
                "id": input_elem.get("id", ""),
                "class": input_elem.get("class", []),
                "name": input_elem.get("name", ""),
                "placeholder": input_elem.get("placeholder", "")
            })
            
        # 分析链接
        links = soup.find_all('a')
        for link in links:
            elements_info["links"].append({
                "text": link.get_text(strip=True),
                "href": link.get("href", ""),
                "id": link.get("id", ""),
                "class": link.get("class", [])
            })
            
        # 分析表单
        forms = soup.find_all('form')
        for form in forms:
            elements_info["forms"].append({
                "id": form.get("id", ""),
                "class": form.get("class", []),
                "action": form.get("action", ""),
                "method": form.get("method", "")
            })
            
        return elements_info
        
    def suggest_selectors(self, element_text):
        """
        根据元素文本建议可能的选择器
        :param element_text: 元素文本
        :return: 建议的选择器列表
        """
        suggestions = []
        
        # 遍历所有已保存的元素信息
        elements_dir = self.output_dir / "elements"
        for json_file in elements_dir.glob("*.json"):
            with open(json_file, "r", encoding="utf-8") as f:
                elements_info = json.load(f)
                
            # 在按钮中查找
            for button in elements_info["buttons"]:
                if element_text.lower() in button["text"].lower():
                    if button["id"]:
                        suggestions.append(f"ID选择器: #{button['id']}")
                    if button["class"]:
                        suggestions.append(f"类选择器: .{'.'.join(button['class'])}")
                    if button["name"]:
                        suggestions.append(f"名称选择器: [name='{button['name']}']")
                        
            # 在输入框中查找
            for input_elem in elements_info["inputs"]:
                if input_elem["placeholder"] and element_text.lower() in input_elem["placeholder"].lower():
                    if input_elem["id"]:
                        suggestions.append(f"ID选择器: #{input_elem['id']}")
                    if input_elem["name"]:
                        suggestions.append(f"名称选择器: [name='{input_elem['name']}']")
                        
            # 在链接中查找
            for link in elements_info["links"]:
                if element_text.lower() in link["text"].lower():
                    if link["id"]:
                        suggestions.append(f"ID选择器: #{link['id']}")
                    if link["class"]:
                        suggestions.append(f"类选择器: .{'.'.join(link['class'])}")
                    suggestions.append(f"文本选择器: a:contains('{link['text']}')")
                    
        return list(set(suggestions))  # 去重 