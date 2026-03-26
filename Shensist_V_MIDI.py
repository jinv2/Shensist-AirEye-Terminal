import rtmidi, time
from flask import Flask, request

# 初始化虚拟 MIDI 端口 - 这会被 Pro Tools/Cubase 识别为真实的硬件控制器 
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
midiout.open_virtual_port("Shensist_AirEye_Control")

app = Flask(__name__)

# 指令映射：将文字直接转化为标准 MIDI CC 指令 
# 这是 2026 年最稳定的专业软件控制方式，不依赖系统快捷键
COMMAND_MAP = {
    "播放": [0xB0, 118, 127], # CC 118: Play
    "停止": [0xB0, 117, 127], # CC 117: Stop
    "录音": [0xB0, 119, 127], # CC 119: Record
    "复制": [0xB0, 102, 127], # 自定义映射至软件内 Skills
    "粘贴": [0xB0, 103, 127],
    "play": [0xB0, 118, 127],
    "stop": [0xB0, 117, 127],
    "record": [0xB0, 119, 127]
}

@app.route('/exec')
def execute():
    msg = request.args.get('msg', '')
    print(f"🎙️ 收到指令: {msg}")
    for k, v in COMMAND_MAP.items():
        if k in msg:
            midiout.send_message(v)
            return f"SENT MIDI: {k}"
    return "NO MATCH"

if __name__ == '__main__':
    print("🏛️ [Shensist-AirEye] 虚拟硬件代理已上线。")
    print("🔗 请在 Pro Tools/Cubase 的 MIDI 设置中将 'Shensist_AirEye_Control' 选为输入设备。")
    app.run(host='0.0.0.0', port=5000)
