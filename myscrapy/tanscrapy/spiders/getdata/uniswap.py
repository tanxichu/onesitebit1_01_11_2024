import scrapy
from .browser_config import create_firefox_driver 
from .action  import perform_action
import time
from .browser_config import create_firefox_driver 
from .action  import perform_action
import json
import asyncio
from .WebSocket_Client import WebSocketClient


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
            perform_action(self.driver, "selector", ".SwapCurrencyInputPanel__StyledDropDown-sc-d5f18f1c-8","click",time=3,index=0)
            perform_action(self.driver, "id", "token-search-input","input",input_text=data["coina"],time=10)
            perform_action(self.driver, "id", "token-search-input","enter",time=10,secondcss="class",second_identifier="css-1guhfcl")
            perform_action(self.driver, "class", "bfOBHG","click",time=10)
            perform_action(self.driver, "id", "token-search-input","input",input_text=data["coinb"],time=10)
            perform_action(self.driver, "id", "token-search-input","enter",time=10,secondcss="class",second_identifier="css-1guhfcl")
        
            perform_action(self.driver, "class", "token-amount-input","input",input_text=data["amount"],time=10)
                
                
            price = perform_action(self.driver, "class", "token-amount-input","getprice",time=10,index=1)
            #print("price:::",price)

            perform_action(self.driver, "selector", "div.ivUDSY","click",time=10)

            slope = perform_action(self.driver, "selector", "div.kdYshN","gettext",time=10, index= 2)
            #print("slope:", slope)

            uniswapfee = perform_action(self.driver, "selector", "div.bRZFqu","gettext",time=10, index= 2)
            #print("uniswapfee:", uniswapfee)

                
            # 以下这个采集不是很理想。可以先不管，毕竟用处不大
            # route = perform_action(self.driver, "selector", "div.efjYeS", "gettext", time=10, index=0)

            #print("route:", route)

            networkfee = perform_action(self.driver, "selector", "div.bRZFqu","gettext",time=10, index= 3)
            #print("networkfee:", networkfee)
            result= { "price":price, "slope:": slope, "uniswapfee:":uniswapfee, "networkfee:": networkfee}   

            #print(result)
            result = json.dumps(result)  #websocket 不能直接发送字典，要换成JSON
            loop.run_until_complete(self.websocket_client.send_message(result))
            self.driver.get("https://app.uniswap.org/swap")

