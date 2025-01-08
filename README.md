# 自动化注册测试项目

这是一个用于测试网站注册功能的自动化测试项目。该项目模拟真实用户的行为，包括鼠标移动、点击和输入文字等操作。

## 项目结构

```
.
├── config/             # 配置文件目录
├── src/               # 源代码目录
├── tests/             # 测试用例目录
├── utils/             # 工具函数目录
├── resources/         # 资源文件目录
│   └── images/        # 图片资源目录
├── requirements.txt   # 项目依赖
└── README.md         # 项目说明文档
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行测试

```bash
pytest tests/test_registration.py
```

## 主要功能

- 自动打开Chrome浏览器并访问目标网站
- 模拟真实用户的鼠标移动和点击行为
- 自动填写注册表单
- 处理验证码页面
- 支持批量测试注册功能

## 注意事项

1. 运行测试前请确保已安装Chrome浏览器
2. 确保网络连接正常
3. 需要在resources/images目录下放置验证码框的参考图片 