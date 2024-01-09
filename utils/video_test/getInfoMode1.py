# -*- coding: utf-8 -*-

# @Time : 2022/4/24 9:17 下午
# @Project : videoDetectDemo
# @File : getInfoMode1.py
# @Author : hutong
# @Describe: 微信公众： 大话性能
# @Version: Python3.9.8


#通过读取二进制文件的方式，获取mp3和wav的属性信息
#mp3Demo

# MP3 文件大体分为三部分：TAG_V2（ID3V2）、Frame、TAG_V1（ID3V1）
# ID3V2

from collections import namedtuple
import struct

# mp3音频文件，MP3 文件的前 10 个字节便是 ID3V2的标签头
ID3V2TagHeader = namedtuple("ID3V2TagFrame",
							["Header", "Ver", "Revision", "Flag", "Size"])
# 二进制的方式打开mp3音频文件
with  open("阿炳-二泉映月.mp3", "rb") as fr_mp3:
	data_mp3 = fr_mp3.read()
	# 通过struck进行字节解码,mp3文件的前10个字节便是ID3V2的标签头
	values = struct.unpack("3s b b b 4s", data_mp3[:10])

mp3Header = ID3V2TagHeader(*values)
print(f'mp3 header: {mp3Header}')


# wavDemo
# wav音频文件
# wav文件头是前面的44个字节数据
WavHeader = namedtuple("WavHeader",
					   ["ChunkID", "ChunkSize", "Format", "Subchunk1ID", "Subchunk1Size",
						"AudioFormat", "NumChannels", "SampleRate", "ByteRate", "BlockAlign",
						"BitsPerSample", "Subchunk2ID", "Subchunk2Size"])
# 二进制的方式打开wav音频文件
with open("二泉映月.wav", "rb") as fr_wav:
	data_wave = fr_wav.read()
	# 通过struck进行字节解码,wav文件头是前面的44个字节数据
	values = struct.unpack("4s I 4s 4s I H H I I H H 4s I", data_wave[:44])

wavHeader = WavHeader(*values)
print(f"wav header: {wavHeader}")
'''
print(f"采样率: {wavHeader.SampleRate}")  # 采样率: 44100
print(f"声道数量: {wavHeader.NumChannels}")  # 声道数量: 2
# 文件的总字节数, 除以每一帧的大小, 再除以采样率, 便可以得到时长
print(f"音频总时长: {len(data_wave) / wavHeader.BlockAlign / wavHeader.SampleRate}")  # 总时长: 356.7735827664399
'''




# 封装mp3文件ID3V1的信息解码
# mp3Util
import chardet


# 二进制方式打开音视频文件，并获取mp3音频文件尾部的128个字节
def getFile(fileName):
	with open(fileName, 'rb') as f:
		# 2代表从文件尾开始偏移
		f.seek(0, 2)
		#print('f current tell() :{}'.format(f.tell()))
		# tell() 函数用于判断文件指针当前所处的位置
		if (f.tell() < 128):
			return None
		# -128代表向文件头方向移动的字节数
		f.seek(-128, 2)
		data_bin = f.read()
		print(f'读取mp3文件中ID3V1标签的字节长度为：{len(data_bin)} 具体内容为：{data_bin}，')
		return data_bin


# 字节转换为字符
def changeDecode(binStr):
	# enType = chardet.detect(binStr)['encoding']
	enType = 'GB2312'
	# print('当前字节编码方式为：{}'.format(enType))
	'''
	if enType == None:
		return binStr.decode('GB2312',errors = 'ignore')
	else:
		data_str = binStr.decode(enType, errors='ignore')
		print('字节转换为字符后为：{}'.format(data_str))
	'''
	data_str = binStr.decode(enType, errors='ignore')
	# print('字节转换为字符后为：{}'.format(data_str))
	return data_str


# 按照mp3音视频文件结构格式，针对ID3V1标签，逐个解析字节为字符
def getInfor(binInfo):
	# 待移除的字节
	rmbin = b"\x00"
	info = {}
	if binInfo[0:3] != b'TAG':
		print('读取到的前3个字节数据为：{}'.format(binInfo[0:3]))
		return '获取失败，检查类型'
	# print(binInfo[3:33])
	info['title'] = binInfo[3:33].strip(rmbin)
	# print('info title : {}'.format(info['title']))
	if info['title']:
		info['title'] = changeDecode(info['title'])

	info['artist'] = binInfo[33:63].strip(rmbin)
	if info['artist']:
		info['artist'] = changeDecode(info['artist'])

	info['album'] = binInfo[63:93].strip(rmbin)
	if info['album']:
		info['album'] = changeDecode(info['album'])

	info['year'] = binInfo[93:97].strip(rmbin)
	if not info['year']:
		info['year'] = '未指定年份'

	info['comment'] = binInfo[98:127].strip(rmbin)
	if info['comment']:
		info['comment'] = changeDecode(info['comment'])

	info['genre'] = ord(binInfo[127:128])

	return info


if __name__ == '__main__':

	binData = getFile('阿炳-二泉映月.mp3')
	changeDecode(binData)
	print(f'解析出来的mp3音频文件ID3V1标签信息为：{getInfor(binData)}')
