import os
import requests
import zipfile
import io

def download_chromedriver():
    # 创建 drivers 目录
    if not os.path.exists('drivers'):
        os.makedirs('drivers')
    
    # ChromeDriver下载URL
    url = "https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.265/win64/chromedriver-win64.zip"
    
    try:
        print("正在下载ChromeDriver...")
        response = requests.get(url)
        response.raise_for_status()
        
        # 解压ZIP文件
        print("正在解压文件...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            # 提取chromedriver.exe
            for file in zip_ref.namelist():
                if file.endswith('chromedriver.exe'):
                    with zip_ref.open(file) as source, open('drivers/chromedriver.exe', 'wb') as target:
                        target.write(source.read())
        
        print("ChromeDriver下载完成！")
        
    except Exception as e:
        print(f"下载失败: {str(e)}")
        raise

if __name__ == "__main__":
    download_chromedriver() 