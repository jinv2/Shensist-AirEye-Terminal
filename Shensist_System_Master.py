import os, json, time, pyautogui, cv2, numpy as np
from vosk import Model, KaldiRecognizer
import pyaudio

# 路径配置
BASE_PATH = "/home/mmm/桌面/Shensist_Matrix/Shensist_AirEye/"
MODEL_PATH = os.path.join(BASE_PATH, "models/cn-model")

# 顶级系统控制映射：将语音直接映射为系统级动作或图像匹配
# 无需逐个教，这里直接定义常用系统行为和软件通用逻辑
SYSTEM_COMMANDS = {
    "复制": lambda: pyautogui.hotkey('ctrl', 'c'),
    "粘贴": lambda: pyautogui.hotkey('ctrl', 'v'),
    "全选": lambda: pyautogui.hotkey('ctrl', 'a'),
    "撤销": lambda: pyautogui.hotkey('ctrl', 'z'),
    "保存": lambda: pyautogui.hotkey('ctrl', 's'),
    "切换": lambda: pyautogui.hotkey('alt', 'tab'),
    "关闭": lambda: pyautogui.hotkey('alt', 'f4'),
    "搜索": lambda: pyautogui.hotkey('ctrl', 'f'),
}

class SystemMasterAgent:
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
            print("🏛️ [Shensist-AirEye] 系统级智能体已就绪。正在全局监听...")
        except Exception as e:
            print(f"❌ 麦克风初始化失败: {e}")
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
                    print(f"🎙️ 系统指令: {text}")
                    
                    # 1. 优先执行系统级快捷键
                    executed = False
                    for cmd, func in SYSTEM_COMMANDS.items():
                        if cmd in text:
                            func()
                            print(f"⚡ 执行系统动作: {cmd}")
                            executed = True
                            break
                    
                    # 2. 若非快捷键，尝试在 system_skills 目录下进行图像匹配（控制任意软件GUI）
                    if not executed:
                        self.auto_match_and_click(text)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️ 系统核心错误: {e}")

    def auto_match_and_click(self, text):
        # 扫描 system_skills 目录，寻找与语音匹配的截图锚点
        skill_dir = os.path.join(BASE_PATH, "system_skills")
        if not os.path.exists(skill_dir):
            return
            
        for skill_name in os.listdir(skill_dir):
            if skill_name in text:
                anchor_path = os.path.join(skill_dir, skill_name, "anchor.png")
                if os.path.exists(anchor_path):
                    template = cv2.imread(anchor_path)
                    screen = cv2.cvtColor(np.array(pyautogui.screenshot()), cv2.COLOR_RGB2BGR)
                    res = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, max_loc = cv2.minMaxLoc(res)
                    if max_val > 0.7:
                        pyautogui.click(max_loc[0] + 30, max_loc[1] + 30)
                        print(f"🎯 视觉匹配成功: {skill_name}")

if __name__ == "__main__":
    SystemMasterAgent().run()
