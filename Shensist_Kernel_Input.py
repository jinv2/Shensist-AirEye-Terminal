import evdev
from evdev import UInput, ecodes as e
from flask import Flask, request
import os

# 定义虚拟硬件具备的按键能力 (模拟物理键盘)
capabilities = {
    e.EV_KEY: [e.KEY_C, e.KEY_V, e.KEY_SPACE, e.KEY_LEFTCTRL, e.KEY_LEFTALT, e.KEY_Z]
}

app = Flask(__name__)

class ShensistInputEngine:
    def __init__(self):
        # 注册一个名为 "Shensist-Virtual-HID" 的真实硬件设备
        try:
            self.ui = UInput(capabilities, name='Shensist-Virtual-HID')
        except PermissionError:
            print("❌ Permission Error: Please run 'sudo chmod 666 /dev/uinput' first.")
            raise

    def tap_hotkey(self, modifier, key):
        self.ui.write(e.EV_KEY, modifier, 1)
        self.ui.write(e.EV_KEY, key, 1)
        self.ui.write(e.EV_KEY, key, 0)
        self.ui.write(e.EV_KEY, modifier, 0)
        self.ui.syn()

    def tap_key(self, key):
        self.ui.write(e.EV_KEY, key, 1)
        self.ui.write(e.EV_KEY, key, 0)
        self.ui.syn()

engine = None

@app.route('/exec')
def execute():
    global engine
    if engine is None:
        try:
            engine = ShensistInputEngine()
        except Exception as e:
            return f"Error initializing HID engine: {str(e)}", 500

    msg = request.args.get('msg', '')
    print(f"🎙️ 接收指令: {msg}")
    
    # 映射表：手机文字 -> 硬件按键动作
    if "复制" in msg:
        engine.tap_hotkey(e.KEY_LEFTCTRL, e.KEY_C)
    elif "粘贴" in msg:
        engine.tap_hotkey(e.KEY_LEFTCTRL, e.KEY_V)
    elif "播放" in msg or "停止" in msg:
        engine.tap_key(e.KEY_SPACE)
    elif "撤销" in msg:
        engine.tap_hotkey(e.KEY_LEFTCTRL, e.KEY_Z)
        
    return f"Executed: {msg}"

if __name__ == '__main__':
    print("🏛️ [Shensist-AirEye] 虚拟 HID 硬件助手等待上线。")
    print("⚠️ 注意: 该脚本需要 /dev/uinput 的读写权限。")
    app.run(host='0.0.0.0', port=5000)
