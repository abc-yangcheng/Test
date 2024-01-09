# -*- coding: utf-8 -*-

# @Project : fastapiDemo
# @File    : chat.py
# @Date    : 2020-12-15
# @Author  : hutong
# @Describe: 微信公众： 大话性能


# 分组发送json数据

from typing import Set, Dict, List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
	def __init__(self):
		# 存放激活的链接
		# self.active_connections: Set[Dict[str, WebSocket]] = set()
		self.active_connections: List[Dict[str, WebSocket]] = []

	async def connect(self, user: str, ws: WebSocket):
		# 链接
		await ws.accept()

		self.active_connections.append({"user": user, "ws": ws})

	def disconnect(self, user: str, ws: WebSocket):
		# 关闭时 移除ws对象
		self.active_connections.remove({"user": user, "ws": ws})

	@staticmethod
	async def send_personal_message(message: dict, ws: WebSocket):
		# 发送个人消息

		await ws.send_json(message)

	async def send_other_message(self, message: dict, user: str):
		# 发送个人消息
		for connection in self.active_connections:
			if connection["user"] == user:
				await connection['ws'].send_json(message)

	async def broadcast(self, data: dict):
		# 广播消息
		for connection in self.active_connections:
			await connection['ws'].send_json(data)


manager = ConnectionManager()


@app.websocket("/ws/{user}")
async def websocket_endpoint(ws: WebSocket, user: str):
	await manager.connect(user, ws)

	await manager.broadcast({"user": user, "message": "进入聊天"})

	try:
		while True:
			data = await ws.receive_json()
			print(data, type(data))

			send_user = data.get("send_user")
			if send_user:
				await manager.send_personal_message(data, ws)
				await manager.send_other_message(data, send_user)
			else:
				await manager.broadcast({"user": user, "message": data['message']})

	except WebSocketDisconnect:
		manager.disconnect(user, ws)
		await manager.broadcast({"user": user, "message": "离开"})


if __name__ == "__main__":
	import uvicorn

	# 官方推荐是用命令后启动 uvicorn main:app --host=127.0.0.1 --port=8010 --reload
	uvicorn.run(app='chat2:app', host="127.0.0.1", port=8010, reload=True, debug=True)
