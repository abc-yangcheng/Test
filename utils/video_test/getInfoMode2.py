# -*- coding: utf-8 -*-

# @Time : 2022/4/23 5:56 下午
# @Project : videoDetectDemo
# @File : getInfoMode2.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8

import os
#设置ffmpeg的安装路径到全局路径
def add_usr_local_bin():
    ffmpeg_path = "/usr/local/bin"
    os.environ["PATH"] += os.pathsep + ffmpeg_path
add_usr_local_bin()
print(os.environ['PATH'])
# 通过第三方库的方式获取或设置音频文件属性

# pymediainfo库，只能获取信息，无法重新设置更新
from pymediainfo import MediaInfo

media_info = MediaInfo.parse(r'阿炳-二泉映月.mp3')
data = media_info.to_json()

print(f'通过pymediainfo库，获取mp3音频信息为：{data}')

# pydub库，除了可以获取信息，还支持设置，保存
import pydub

song = pydub.AudioSegment.from_mp3("阿炳-二泉映月.mp3")
# 返回的是一个 AudioSegment 对象，它就是音频读取之后的结果，通过该对象我们可以对音频进行各种操作
print(f'通过pydub库，读取音频文件后返回值为：{song}')

# 获取属性
# 声道数, 1 表示单声道, 2 表示双声道
print(f'通过pydub库，获取的声道数为：{song.channels}')  # 2

# 采样宽度乘以 8 就是采样位数
print(f'通过pydub库，获取的采样位数为：{song.sample_width * 8}')  # 16

# 采样频率, 采样频率等于帧速率
print(f'通过pydub库，获取的采样频率为：{song.frame_rate}')  # 44100

# 时长(单位秒)
print(f'通过pydub库，获取的音频时长为：{song.duration_seconds}')  # 258.97600907029477

# 设置属性
# 我们可以更改设置采样频率
'''
print('原来的采样频率：{}'.format(song.frame_rate))  # 44100

# 更改采样频率, 一般都是 44100, 我们可以修改为其它的值
# 注意: 并不是任意值都可以, 只能是 8000 12000 16000 24000 32000 44100 48000 之一
# 如果不是这些值当中的一个, 那么会当中选择与设置的值最接近的一个
# 比如我们设置 18000, 那么会自动变成 16000
song.set_frame_rate(16000).export("newSong.mp3", "mp3",bitrate="320k")
print('更改后的采样频率：{}'.format(pydub.AudioSegment.from_mp3("newSong.mp3").frame_rate))  # 16000
'''

# 保存文件
# 指定文件名和保存的类型即可，注意：第二个参数表示保存的音频的类型，如果不指定那么默认是 mp3

song.export("二泉映月.wav", "wav",tags=
					{"title":"二泉映月",
						"artist": "阿炳",
                  "comments": "soul singer"})

# 读取之后查看前 4 个字节, 发现是 b"RIFF", 证明确实是 wav 格式
data = open("二泉映月.wav", "rb").read(4)
import struct
header = struct.unpack("4s", data)[0]
print(header)  # b'RIFF' 证明是wav格式




if __name__ == '__main__':
	pass
