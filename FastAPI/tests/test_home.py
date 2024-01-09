# -*- coding: utf-8 -*-

# @Project : fastapiDemo
# @File    : test_home.py
# @Date    : 2020-11-16
# @Author  : hutong
# @Describe: 微信公众： 大话性能



"""
测试首页接口数据
"""

from api import create_app
from fastapi.testclient import TestClient

app = create_app()

client = TestClient(app)


def test_banner():
    response = client.get("/api/shopdemo/home/banner")
    assert response.status_code == 200
    assert response.json().get("code") == 200


def test_features():
    response = client.get("/api/shopdemo/home/features")
    assert response.status_code == 200
    assert response.json().get("code") == 200


def test_recommends():
    response = client.get("/api/shopdemo/home/recommends")
    assert response.status_code == 200
    assert response.json().get("code") == 200


def test_tab():
    response = client.get("/api/shopdemo/home/tab")
    assert response.status_code == 200
    assert response.json().get("code") == 200


def test_goods():
    response = client.get(
        "/api/shopdemo/home/goods",
        params={
            "tabId": 0,
            "page": 1,
            "pageSize": 10
        }
    )
    assert response.status_code == 200
    assert response.json().get("code") == 200


if __name__ == '__main__':
    test_banner()
    test_features()
    test_recommends()
    test_tab()
    test_goods()
