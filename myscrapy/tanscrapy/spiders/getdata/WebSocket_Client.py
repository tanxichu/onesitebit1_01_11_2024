import asyncio
import websockets
import time

class WebSocketClient:

    def __init__(self, inputurl):
        self.uri = "ws://localhost:8001/" + inputurl  #实例时传入
        self.websocket = None
        self.connected = False 
        self.inputurl = inputurl

    async def connect(self):
        start_time = time.time()
        #当他连接后会修改self.connected = True，在此再次检测，同时for不超60秒
        while not self.connected and time.time() - start_time < 60:  
            try:
                self.websocket = await websockets.connect(self.uri)
                self.connected = True
                print("WebSocket 连接成功")
                break
            except Exception as e:
                #返回while
                await asyncio.sleep(1)  # 等待1秒再重试
        print("connect方法运行完了")

    async def send_message(self, message):
        if not self.connected:
            print("WebSocket 未连接")
            await self.connect()

        else : 
            try:
                #发前检测对方是否在线时再发
                await self.websocket.send("CAN_I_SEND")
                respond = await self.websocket.recv()
                if respond == "cansend":
                    await self.websocket.send(message)

            #以下是防向scrapy发送时，刚开始是通的，此时connected = ture，但后来不知为何断了，现在再次连接多一次
            except websockets.ConnectionClosed as e:
                print(f"连接断开，send_message: {e}")
                self.connected = False
                await self.connect()
                print("已连接上了")
                print("已接上，现在要发的数据是：", message)
                #再调本地的方法，相当于一个for
                if self.connected:        # 一定要加这个，否则会出错，原因不明
                    message = await self.send_message()
                    print("断开后现在重新发送的消息:"+message)

    async def receive_message(self):
        if not self.connected :
            print("WebSocket 未连接")
            await self.connect()

        else:
            try:
                message = await self.websocket.recv()
                print("接收到消息:", message)
                return message
            except websockets.ConnectionClosed as e:
                print(f"连接断开，正在尝试重新连接... 错误详情: {e}")
                self.connected = False
                await self.connect()
                if self.connected:        # 一定要加这个，否则会出错，原因不明
                    print("我是断开后接收数据的部份")
                    message = await self.receive_message()
                    print("断开后现在重新接收到消息:"+message)
                    return message