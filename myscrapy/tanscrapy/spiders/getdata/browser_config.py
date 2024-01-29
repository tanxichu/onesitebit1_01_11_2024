from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def create_firefox_driver():
    options = Options()

    # 设置无头模式   options.headless = True   这个在win中不行，下面的才可以
    options.add_argument("--headless")

    # 设置首选项
    options.set_preference("permissions.default.image", 2)  # 禁用图片
    options.set_preference("dom.ipc.plugins.enabled", False)  # 禁用 Flash 和其他插件
    options.set_preference("browser.display.use_document_fonts", 0)  # 禁用字体
    options.set_preference("permissions.default.stylesheet", 2)  # 禁用 CSS
    options.set_preference("browser.cache.disk.enable", True)  # 启用磁盘缓存
    options.set_preference("browser.cache.memory.enable", True)  # 启用内存缓存
    options.set_preference("webdriver.load.strategy", "unstable")  # 设置页面加载策略
    options.set_preference("dom.disable_window_open_feature", "all")  # 禁用页面弹出窗口
    options.set_preference("dom.webnotifications.enabled", False)  # 禁用浏览器通知弹窗

    # 使用修改后的 options 创建 WebDriver 实例
    driver = webdriver.Firefox(options=options)
    return driver




