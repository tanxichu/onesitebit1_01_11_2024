import asyncio
import websockets
import time

class WebSocketClient:

    def __init__(self, inputurl):
        self.uri = "ws://localhost:8001/" + inputurl  
        self.websocket = None
        self.connected = False 
        self.inputurl = inputurl

    async def connect(self):
        retry_count = 0
        start_time = time.time()
        while not self.connected and time.time() - start_time < 60:  # 1分钟超时
            try:
                self.websocket = await websockets.connect(self.uri)
                self.connected = True
                print("WebSocket 连接成功")
                break
            except Exception as e:
                retry_count += 1
                if retry_count >= 10000:  # 最多重试5次
                    print(f"尝试重新连接次数达到限制: {e}")
                    break
                print(f"连接失败, 将在5秒后重试: {e}")
                await asyncio.sleep(1)  # 等待5秒再重试
        print("connect方法运行完了")

    async def send_message(self, message):
        if not self.connected:
            print("WebSocket 未连接")
            await self.connect()

        if self.connected :  # 检查是否已连接
            try:
                await self.websocket.send("CAN_I_SEND")
                respond = await self.websocket.recv()
                if respond == "cansend":
                    await self.websocket.send(message)

            except websockets.ConnectionClosed as e:
                print(f"连接断开，send_messagesend_messagesend_messagesend_message: {e}")
                self.connected = False
                await self.connect()
                print("已连接上了")
                if self.connected:
                    print("已接上，现在要发的数据是：", message)
                    await self.send_message("断开后重新发送的：" + message)


    async def receive_message(self):
        if not self.websocket:
            print("WebSocket 未连接")
            return

        if self.connected:  # 检查是否已连接
            try:
                message = await self.websocket.recv()
                
                print("接收到消息:", message)
                return message
            except websockets.ConnectionClosed as e:
                print(f"连接断开，正在尝试重新连接... 错误详情: {e}")
                self.connected = False
                await self.connect()
                if self.connected:        # 一定要加这个，否则会出错
                    print("我是断开后接收数据的部份")
                    message = await self.receive_message()
                    print("断开后现在重新接收到消息:"+message)
                    return message




'''
import asyncio
import time
from WebSocketClient import WebSocketClient

    

async def main():
    url = "chatroom"
    client = WebSocketClient(url)      
    await client.connect()
    await client.send_message("1111")
    re = await client.receive_message()
    print("a1::::::::::", re)
    

    await client.send_message("2222")
    re = await client.receive_message()
    print("a1::::::::::", re)
    
    #await asyncio.sleep(10)
    
    await client.send_message("333")
    #await asyncio.sleep(10)

    
    re = await client.receive_message()
    print("a1::::::::::", re)
    #await asyncio.sleep(60)

    await client.send_message("4444")
    re = await client.receive_message()
    print("a1::::::::::", re)
    #await asyncio.sleep(80)

    await client.send_message("555")
    re = await client.receive_message()
    print("a1::::::::::", re)
    #await asyncio.sleep(120)


   

if __name__ == "__main__":
    asyncio.run(main())

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


import time
from WebSocketClient import WebSocketClient
import asyncio


async def ab(data):
    url = "chatroom"
    websocket_client = WebSocketClient(url)
    await websocket_client.connect()


 

  
    while True:
        time.sleep(15)
        re = await websocket_client.receive_message()
        if re:
            print("a2 接收到消息:", re)
            
            await websocket_client.send_message(data + re)
            #print("a2 have sent after shut down:::::::,",data + re)

if __name__ == "__main__":
    asyncio.run(ab("A2 接收到::::"))


    '''