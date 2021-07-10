import wave
from pyaudio import PyAudio,paInt16
import threading

framerate=16000     # 16000帧/s
NUM_SAMPLES=8000    # 2000帧
channels=1
sampwidth=2
def save_wave_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()


def my_record():
    wsFunction = True
    if wsFunction:
        # ibingli server address :  "wss://vt.ibingli.cn/recognize"
        ws_client = WSClient("ws://localhost:8888", lambda message: print("call_back message:", message))
        ws_client.run()

    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)


    while True:
        # 每8000帧传输一次,0.5s
        string_audio_data = stream.read(NUM_SAMPLES)
        # my_buf.append(string_audio_data)
        if wsFunction:
            ws_client.send_message(string_audio_data)

        # count+=1
        print('.')
        time.sleep(0.04)
    # save_wave_file('01.wav',my_buf)
    # stream.close()
    # pa.terminate()

chunk=2000
def play():
    wf=wave.open(r"01.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        print(data)
        if data=="":break
        stream.write(data)
    wf.close()
    stream.close()
    p.terminate()

class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print ("开始线程：" + self.name)
        # function
        print ("退出线程：" + self.name)

import websocket
import time
import threading


class WebsocketClient(object):
    """docstring for WebsocketClient"""

    def __init__(self, address, message_callback=None):
        super(WebsocketClient, self).__init__()
        self.address = address
        self.message_callback = message_callback

    def on_message(self, ws, message):
        # message = json.loads(message)
        print("on_client_message:", message)
        if self.message_callback:
            self.message_callback(message)

    def on_error(self, ws, error):
        print("client error:", error)

    def on_close(self, ws):
        print("### client closed ###")
        self.ws.close()
        self.is_running = False

    def on_open(self, ws):
        self.is_running = True
        print("on open")

    def close_connect(self):
        self.ws.close()

    def send_message(self, message):
        try:
            self.ws.send(message, opcode=0x2)
        except BaseException as err:
            pass

    def run(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.address,
                                         on_message=lambda ws, message: self.on_message(ws, message),
                                         on_error=lambda ws, error: self.on_error(ws, error),
                                         on_close=lambda ws: self.on_close(ws))
        self.ws.on_open = lambda ws: self.on_open(ws)
        self.is_running = False
        while True:
            print(self.is_running)
            if not self.is_running:
                self.ws.run_forever()
            time.sleep(3)


class WSClient(object):
    def __init__(self, address, call_back):
        super(WSClient, self).__init__()
        self.client = WebsocketClient(address, call_back)
        self.client_thread = None

    def run(self):
        self.client_thread = threading.Thread(target=self.run_client)
        self.client_thread.start()

    def run_client(self):
        self.client.run()

    def send_message(self, message):
        self.client.send_message(message)

if __name__ == '__main__':
    my_record()
    print('Over!')
    # play()