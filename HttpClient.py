#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
@author: nl8590687
asrserver测试专用客户端

'''

import requests
from general_function.file_wav import *

url = 'http://121.5.66.137:20000/'

token = 'qwertasd'

wavsignal,fs=read_wav_data('test.wav')

#print(wavsignal,fs)

datas={'token':token, 'fs':fs, 'wavs':wavsignal}

r = requests.post(url, datas)

r.encoding='utf-8'

print(r.text)