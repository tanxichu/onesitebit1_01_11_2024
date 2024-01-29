import scrapy
from .browser_config import create_firefox_driver 
from .action  import perform_action
import time
from .action  import perform_action
import json
import asyncio
from .WebSocket_Client import WebSocketClient
from PIL import Image
import io
import os
from time import sleep



#curl --proxy socks5://127.0.0.1:9150 https://www.baidu.com
# 以上用于测试tor代理是否正常运行，主要是tor端口的确认测试
# scrapy crawl baidu_tor 命令会自动启动一个Scrapy爬虫，并根据Spider名称 "baidu_tor" 去查找与该名称匹配的Spider类，
# 然后执行该Spider类中的相关代码。
# 操作执行方法：scrapy crawl baidu_tor
# class BaiduTorSpider1(scrapy.Spider) 表示 BaiduTorSpider1111111 类继承了Scrapy框架中的 scrapy.Spider 类
# 这个类下的声明全是给主类使用的。name与start_urls 不能修改
    #parse 方法是Scrapy爬虫中的入口方法,这个parse在scrapy.Spider已定义好了。不能修改
    # self是指这个爬虫的实例，不能修改。respose1是返回的实例，是个变量，可另起名。

class TestSpider(scrapy.Spider):
    start_time = time.time()
    name = 'uniswap'
    start_urls = ['https://app.uniswap.org/swap']
    driver = create_firefox_driver()

    def __init__(self, forwardurl= None):
        super().__init__()
        self.forwardurl = forwardurl

    async def startwebsocket(self):
        self.websocket_client = WebSocketClient(self.forwardurl)
        await self.websocket_client.connect()

    
    async def receive_data(self):
        data = await self.websocket_client.receive_message()
        return data


    def parse(self, response):
   
        self.driver.get(response.url)
        loop = asyncio.get_event_loop()   # 在同步用运行异步用一种特定的方法
        loop.run_until_complete(self.startwebsocket())
        
        

    
        while True:            
            data = loop.run_until_complete(self.receive_data())
            # 将字符串转换为字典
            data = json.loads(data)
            
            #一定要传入self.driver，否则会被当成是不同的上下文，因self.driver.get(response.url)，已传入属性了。
            #(driver, locator_type="", element_identifier="", action="", input_text="", time=10, index=0, search_text=""):
            perform_action(self.driver, "find_element_by_xpath", action="click",search_text = "//span[contains(text(), 'ETH')]")
            print("已点首页的下拉")
            search_text = "//input[@placeholder='Search name or paste address']"
            perform_action(self.driver, "find_element_by_xpath", action="input",input_text=data["coina"], search_text = search_text)
            print("已输入coina")
            perform_action(self.driver, "selector", "#token-search-input","enter",time=10)
            print("已回车")

            perform_action(self.driver, "find_element_by_xpath",action="click", search_text="//span[contains(text(), 'Select token')]")
            print("第二个标签conib首页已按下了")

            search_text = "//input[@placeholder='Search name or paste address']"
            perform_action(self.driver, "find_element_by_xpath", action="input",input_text=data["coinb"], search_text = search_text)
            
            print("已输入coinb")

            perform_action(self.driver, "selector", "#token-search-input","enter",time=10)
            print("已输入coinb后回车")

            perform_action(self.driver, "selector", ".token-amount-input","input",input_text=data["amount"],time=10)
            print("已输入兑换数量") 

            price = perform_action(self.driver, "selector", ".token-amount-input","getprice",time=10,index=1)
            print("price:::::",price)

            perform_action(self.driver, "selector", "div.ivUDSY","click",time=10)
            print("已点扩展下拉")

            slope = perform_action(self.driver, "selector", action="find_element_with_text", search_text = "//div[contains(text(), 'slippage')]" )
            print("slope:",slope)

            uniswapfee = perform_action(self.driver, "selector", action="find_element_with_text", search_text = "//div[contains(text(), 'Fee')]" )
            print("uniswapfee:",uniswapfee)


            Networkcost = perform_action(self.driver, "selector", action="find_element_with_text", search_text = "//div[contains(text(), 'Network cost')]" )
            print("Networkcost:",Networkcost)

            routing = perform_action(self.driver, "selector", action="find_element_with_text", search_text = "//div[contains(text(), 'routing')]" )
            print("routing:",routing)


            result= { "price":price, "slope:": slope, "uniswapfee":uniswapfee, "Networkcost": Networkcost, "routing":routing}
   

            print(result)
            result = json.dumps(result)  #websocket 不能直接发送字典，要换成JSON
            loop.run_until_complete(self.websocket_client.send_message(result))    #这个是在同步中实现异步

            
            



            # 获取截图
            screenshot = self.driver.get_screenshot_as_png()
            screenshot = Image.open(io.BytesIO(screenshot))


            # 裁剪图片的尺寸，注与服务器的屏幕有关的
            width, height = screenshot.size
            # screenshot.crop((left_margin, navbar_height, width - right_margin, height))
            cropped_screenshot = screenshot.crop((500, 100, width-500, height+200))

            # 设置保存到桌面的路径（适用于Windows用户）
            desktop = "D:/"
            save_path = os.path.join(desktop, 'cropped_screenshot.png')
            # 保存裁剪后的图片
            cropped_screenshot.save(save_path)



            self.driver.get("https://app.uniswap.org/swap")
   

