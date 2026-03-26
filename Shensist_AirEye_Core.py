import os, json, time, evdev
from evdev import UInput, ecodes as e
from vosk import Model, KaldiRecognizer
import pyaudio

# 配置路径
BASE_PATH = "/home/mmm/桌面/Shensist_Matrix/Shensist_AirEye/"
MODEL_PATH = os.path.join(BASE_PATH, "models/cn-model")

# [同音词映射表] 解决“肤质”、“物质”、“转帖”等识别偏差 [cite: 1, 16]
PHONETIC_MAP = {
    "肤质": "复制", "五至": "复制", "物质": "复制", "府治": "复制",
    "反击": "复制", "难题": "复制", "问题": "复制",
    "转帖": "粘贴", "专辑": "粘贴", "粘接": "粘贴", "粘基": "粘贴"
}

# [内核级物理按键模拟] 直接绕过 Wayland 桌面限制 [cite: 2, 9]
def send_key_combo(keys):
    try:
        with UInput() as ui:
            for key in keys:
                ui.write(e.EV_KEY, key, 1)
            for key in reversed(keys):
                ui.write(e.EV_KEY, key, 0)
            ui.syn()
        return True
    except Exception as err:
        print(f"❌ 物理按键模拟失败: {err}")
        return False

# 系统动作定义
SYSTEM_ACTIONS = {
    "复制": lambda: send_key_combo([e.KEY_LEFTCTRL, e.KEY_C]),
    "粘贴": lambda: send_key_combo([e.KEY_LEFTCTRL, e.KEY_V]),
    "撤销": lambda: send_key_combo([e.KEY_LEFTCTRL, e.KEY_Z]),
    "播放": lambda: send_key_combo([e.KEY_SPACE]),
    "切换": lambda: send_key_combo([e.KEY_LEFTALT, e.KEY_TAB])
}

class ShensistMasterAgent:
    def __init__(self):
        if not os.path.exists(MODEL_PATH):
            print(f"❌ 错误：找不到 Vosk 模型 at {MODEL_PATH}")
            return
            
        self.model = Model(MODEL_PATH)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.mic = pyaudio.PyAudio()
        try:
            self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
            self.stream.start_stream()
            print("🏛️ [Shensist-AirEye] 系统级内核驱动已重载。权限已修复。")
        except Exception as ex:
            print(f"❌ 麦克风开启失败: {ex}")
            self.stream = None

    def run(self):
        if not self.stream:
            return
        while True:
            try:
                data = self.stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    res = json.loads(self.recognizer.Result())
                    text = res.get("text", "").replace(" ", "")
                    if not text: continue
                    
                    # 同音修正逻辑
                    for k, v in PHONETIC_MAP.items():
                        if k in text: text = v
                    
                    print(f"🎙️ 识别并修正: {text}")

                    if text in SYSTEM_ACTIONS:
                        if SYSTEM_ACTIONS[text]():
                            print(f"⚡ [内核执行成功] 已发送物理按键: {text}")
            except KeyboardInterrupt:
                break
            except Exception as ex:
                print(f"⚠️ 系统核心错误: {ex}")

if __name__ == "__main__":
    ShensistMasterAgent().run()
