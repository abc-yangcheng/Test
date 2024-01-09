# -*- coding: utf-8 -*-

# @Project : fastapiDemo
# @File    : response_code.py
# @Date    : 2020-11-16
# @Author  : hutong
# @Describe: 微信公众： 大话性能

"""
定义返回的状态
"""


from fastapi import status
from fastapi.responses import JSONResponse, Response, ORJSONResponse

from typing import Union


def resp_200(data: Union[list, dict, str]=None, *, message: str="Success") -> dict:
    return {
            'code': 200,
            'message': message,
            'data': data,
        }


def resp_403(data: str = None) -> Response:
    return ORJSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            'code': 403,
            'message': "Forbidden",
            'data': data,
        }
    )


def resp_404(data: str = None) -> Response:
    return ORJSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'code': 404,
            'message': "Page Not Found",
            'data': data,
        }
    )


def resp_500(data: str = None) -> Response:
    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'code': "500",
            'message': "Server internal error",
            'data': data,
        }
    )


# 自定义
def resp_5000(data: Union[list, dict, str]) -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': 5000,
            'message': "Token failure",
            'data': data,
        }
    )

if __name__ == "__main__":
    pass
