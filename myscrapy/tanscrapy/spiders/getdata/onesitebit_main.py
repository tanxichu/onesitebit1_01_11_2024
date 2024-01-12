#只能用这个方法：：：：   uvicorn app:app --host 0.0.0.0 --port 8000


import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
from pydantic import BaseModel
import uuid
import asyncio
import asyncio
import time
import os
import sys

'''
因下面的，cwd=os.path.dirname(os.path.abspath(__file__)),会修改
这行代码的作用是设置启动子进程时的当前工作目录。这里的 __file__ 是一个特殊变量，它包含了当前执行文件的完整路径。
os.path.abspath(__file__) 返回当前执行文件的绝对路径。
os.path.dirname() 获取该路径的目录部分，即去掉文件名后的路径。
这条代码相当于在当前目录下建立一个虚拟的环境用于子进程中。所以他会影响
from WebSocket_Client import WebSocketClient，会提示找不到模块。为解决这个问题，
获取当前工作目录并添加到sys.path：：sys.path.append(os.getcwd())
同时还要放在import之前
'''
sys.path.append(os.getcwd())
from WebSocket_Client import WebSocketClient




app = FastAPI()

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class ScrapyProcess:
    def __init__(self,forwardurl):
        self.process = None
        self.forwardurl = forwardurl

    async def create_and_start_process(self):
        scrapy_command = [
            'scrapy', 'crawl', 'uniswap',
            '-a', 'forwardurl=' + self.forwardurl,
        ]

    
        self.process = await asyncio.create_subprocess_exec(   # 打开默认首页
            *scrapy_command,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        

    async def startwebsocket(self):
        newSocketClient = WebSocketClient(self.forwardurl)      
        await newSocketClient.connect()   # 这个WebSocketClient就是websocket对象 ,已连接好了
        return newSocketClient


async def initialize_processes():
    for i in range(2):
        forwardurl = str(uuid.uuid4())
        process = ScrapyProcess(forwardurl)          
        await process.create_and_start_process()  # 打开一个scrapy爬虫  
        websocketclient = await process.startwebsocket()   # 打开一个webscocket专用通道对应这个进程
        process_pool.append( {forwardurl:websocketclient} )

process_pool = []

#这个是fastapi特定的，一打开就运行了
@app.on_event("startup")
async def startup_event():
    global process_pool
    await initialize_processes()

class ScrapyData(BaseModel):
    website: str
    coina: str = ''
    coinb: str = ''
    amount: str = ''


@app.post("/process-data")
async def process_data(data: ScrapyData):
    try:
        json_data = json.dumps(dict(data))  #注意：收到的是ScrapyData(BaseModel)型数据，所以一定要dict变成字典
        processwebsocket = process_pool.pop()
        forwardurl, websocketclient = processwebsocket.popitem() 
        await websocketclient.send_message(json_data)
        data = await websocketclient.receive_message()
        process_pool.append({forwardurl:websocketclient})
        return data
                
    except Exception as e:
        error_message = f"An error occurred: {e}"
        return {"message": error_message}
     
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
