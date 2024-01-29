import asyncio
import websockets

# connections = {}    
class WebSocketServer:
    def __init__(self):
        self.requested_url=""    
        self.connections = {}

    # 客户端传入这个：self.uri = "ws://localhost:8001/" + inputurl，这个的path会接收 “/”+ inputurl 
    # websocket 就是 websocket.serve 传入的实时连接对象。
    async def handler(self, websocket, path):
        requested_url = path.strip("/")
        self.connections[websocket] = requested_url

        try:
            async for message in websocket: 
                if message == "CAN_I_SEND":    #由客户端发来，可以保证二个终端都上线时才发信息
                    can_send = await self.checkcansend(requested_url)  #等到最小二个才下一步
                    for connection, url in self.connections.items():
                        #返回给发件方，通知可发
                        if url == requested_url and connection == websocket:  
                            await connection.send(can_send)

                else:     #这个是平常的信息，要给通道的另一方发送的
                    for connection, url in self.connections.items():
                        if url == requested_url and connection != websocket:
                            print("i will send to others")
                            await connection.send(message)
                            print("server have sent to others")

        # 这个是一个清理内容的代码，即若系统检测到与这个url相关的客户端全不在线时才从list中将它删除。可以不定，但写了更好
        finally:
            del self.connections[websocket]   

    '''服务器启动先启动这个，with是python的用法，能让系统不用显示处理关闭事项。和tensorflow一样。
    websockets.serve是固定写法，启动websocket服务器。self.handler 是指定为处理 WebSocket 连接的函数或协程。
    当有客户端连接到由 websockets.serve 创建的 WebSocket 服务器时，由这个self.handler的内容处理函数。
    await asyncio.get_event_loop().run_in_executor(None, input) 这个只是一个晃子，让服务器能在ctrl+c时能退出'''
    async def start(self, host, port):
        async with websockets.serve(self.handler, host, port):
            await asyncio.get_event_loop().run_in_executor(None, input)

    async def checkcansend(self, targeturl):
        while True: 
            #统计同一个url即通道的客户端个数 
            url_count = sum(url == targeturl for url in self.connections.values())

            if url_count >= 2:
                print("找到两个或更多相同的 requested_url")
                return "cansend"

            await asyncio.sleep(0.1)  # 短暂等待后再次检查

        
if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start("localhost", 8001))

