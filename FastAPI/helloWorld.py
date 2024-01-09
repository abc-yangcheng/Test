# -*- coding: utf-8 -*-

# @Time : 2022/4/4 9:00 下午
# @Project : myFastAPI
# @File : helloWorld.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


from fastapi import FastAPI
#创建一个实例
app = FastAPI()

#添加路径操作装饰器和路径操作函数
@app.get("/")
async def demo():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    # 启动服务
    uvicorn.run(app='helloWorld:app', host="127.0.0.1", port=8010, reload=True, debug=True)
