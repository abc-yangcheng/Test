# -*- coding: utf-8 -*-

# @Project : fastapiDemo
# @File    : __init__.py.py
# @Date    : 2020-11-16
# @Author  : hutong
# @Describe: 微信公众： 大话性能

"""
路由汇总
"""

from fastapi import APIRouter
from api.shopdemo.home import home


api_v1 = APIRouter()

api_v1.include_router(home.router, tags=["首页API"])
api_v1.include_router(goods.router, tags=["商品API"])
api_v1.include_router(category.router, tags=["分类API"])
api_v1.include_router(profile.router, tags=["个人信息"])





if __name__ == "__main__":
    pass
