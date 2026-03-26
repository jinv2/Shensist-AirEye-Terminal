import vosk
import pyaudio
import json
import pyautogui
import os
import cv2
import numpy as np

class ShensistAgent:
    def __init__(self, skills_path="./skills"):
        self.skills_path = skills_path
        self.skills = self.load_skills()
        print("🚀 Shensist-Agent 已启动，正在扫描工程...")

    def load_skills(self):
        # 扫描子文件夹，实现无缝接轨制作 [cite: 7]
        if not os.path.exists(self.skills_path):
            os.makedirs(self.skills_path)
        return [d for d in os.listdir(self.skills_path) if os.path.isdir(os.path.join(self.skills_path, d))]

    def execute_skill(self, skill_name):
        skill_dir = os.path.join(self.skills_path, skill_name)
        anchor_path = f"{skill_dir}/anchor.png"
        if not os.path.exists(anchor_path):
            print(f"❌ 技能 {skill_name} 缺少 anchor.png")
            return
            
        anchor = cv2.imread(anchor_path)
        # 屏幕匹配逻辑 [cite: 10]
        screen = pyautogui.screenshot()
        screen_np = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(screen_np, anchor, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.8:
            pyautogui.moveTo(max_loc[0], max_loc[1])
            pyautogui.click()
            print(f"✅ 执行成功: {skill_name}")
        else:
            print(f"❌ 未在当前屏幕找到 {skill_name} 的操作锚点")

# 初始化语音监听与技能匹配逻辑...
def main():
    agent = ShensistAgent("./skills")
    print(f"当前识别到的技能: {agent.skills}")

if __name__ == "__main__":
    main()
