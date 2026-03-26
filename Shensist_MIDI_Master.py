import rtmidi, time, os
from flask import Flask, request

# 初始化虚拟 MIDI 端口
midiout = rtmidi.MidiOut()
# 在系统层注册名为 "Shensist_AirEye_Control" 的硬件设备
midiout.open_virtual_port("Shensist_AirEye_Control")

app = Flask(__name__)

# 指令映射：将文字转化为标准 MIDI CC 指令 (音频软件通用语言)
COMMAND_MAP = {
    "播放": [0xB0, 118, 127], # CC 118: Play
    "停止": [0xB0, 117, 127], # CC 117: Stop
    "录音": [0xB0, 119, 127], # CC 119: Record
    "复制": [0xB0, 102, 127], 
    "粘贴": [0xB0, 103, 127],
    "play": [0xB0, 118, 127],
    "stop": [0xB0, 117, 127],
    "record": [0xB0, 119, 127]
}

@app.route('/exec')
def execute():
    msg = request.args.get('msg', '')
    print(f"🎙️ 接收到文字指令: {msg}")
    for k, v in COMMAND_MAP.items():
        if k in msg:
            midiout.send_message(v)
            print(f"⚡ [MIDI 注入成功] 已模拟硬件按下: {k}")
            return f"SENT: {k}"
    return "NO MATCH"

if __name__ == '__main__':
    # 强制开放 5000 端口，供手机访问
    print("🏛️ [Shensist-AirEye] 虚拟 MIDI 硬件已挂载。")
    print("🔗 手机请访问 http://192.168.1.9:5000/exec?msg=播放")
    app.run(host='0.0.0.0', port=5000)
