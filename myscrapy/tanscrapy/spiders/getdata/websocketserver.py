import asyncio
import websockets
import asyncio

# connections = {}    
class WebSocketServer:
    def __init__(self):
        self.requested_url=""
        self.connections = {}
        print("websocket server started")

    async def handler(self, websocket, path):
        requested_url = path.strip("/")
        print(requested_url)

        self.connections[websocket] = requested_url

        try:
            async for message in websocket:    # 注意，若是二个不同的终端运行代码的，全局变量不能共享
                
                print(f"Received from {requested_url}: {message}")
                if message == "CAN_I_SEND":
                    can_send = await self.checkcansend(requested_url)  # 假设这是一个检查函数
                    for connection, url in self.connections.items():
                        if url == requested_url and connection == websocket:
                            await connection.send(can_send)


                else:
                    for connection, url in self.connections.items():
                        print("requested_url and connection != websocket::::::::", url == requested_url ,connection != websocket)
                        if url == requested_url and connection != websocket:
                            print("i will send to others")
                            await connection.send(message)
                            print("server have sent to others")
        
        except websockets.ConnectionClosedError:
            pass
        finally:
            del self.connections[websocket]

    async def start(self, host, port):
        async with websockets.serve(self.handler, host, port):
            await asyncio.Future()  # 保持服务器运行

    async def checkcansend(self, targeturl):
       
        while True:  
            url_count = sum(url == targeturl for url in self.connections.values())

            if url_count >= 2:
                print("找到两个或更多相同的 requested_url")
                return "cansend"

            await asyncio.sleep(0.1)  # 短暂等待后再次检查

        
if __name__ == "__main__":
    server = WebSocketServer()
    asyncio.run(server.start("localhost", 8001))
