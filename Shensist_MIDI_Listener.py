# =================================================================
# 🏛️ 项目名称：神思庭控制终端 (Shensist-AirEye Terminal)
# 🎨 创作者：神思庭艺术智能工作室 (Shensist Art Intelligence Studio)
# 📜 版权所有：© 2025-2026 Shensist (AIS). All Rights Reserved.
# 🌐 官方网站：https://shensist.top/
# ⚠️ 法律声明：本软件及其核心 Skills 逻辑受版权法保护。
# =================================================================
import mido
import os
import requests

# 映射：MIDI 键号 -> 语义指令
# 例如：按下 C3 (60) 触发“播放”，按下 D3 (62) 触发“剃刀”
MIDI_SKILLS = {
    60: "播放",
    62: "剃刀",
    64: "撤销"
}

def midi_listener():
    print("🎹 [神思庭-AIS] MIDI 监听引擎已启动...")
    print("📡 正在探测物理 MIDI 设备...")
    
    # 自动探测第一个可用的 MIDI 输入端口
    try:
        # 获取所有输入端口列表
        input_names = mido.get_input_names()
        if not input_names:
            print("⚠️ 未检测到任何 MIDI 输入设备。")
            return

        print(f"✅ 已检测到设备: {input_names[0]}")
        with mido.open_input(input_names[0]) as inport:
            for msg in inport:
                # 仅处理 note_on 且 velocity > 0 (按下键)
                if msg.type == 'note_on' and msg.velocity > 0:
                    if msg.note in MIDI_SKILLS:
                        skill = MIDI_SKILLS[msg.note]
                        # 联动 Web Master 执行逻辑
                        try:
                            # 优先尝试本地 127.0.0.1 端口触发
                            url = f"http://127.0.0.1:5000/exec?msg={skill}"
                            requests.get(url, timeout=1)
                            print(f"⚡ [MIDI 触发] 键号 {msg.note} -> 执行技能: {skill}")
                        except Exception as e:
                            print(f"❌ 触发失败: Web Master 未启动或连接超时 ({e})")
                    else:
                        print(f"🔍 [MIDI 监听] 未定义键号: {msg.note}")
                        
    except Exception as err:
        print(f"❌ MIDI 引擎错误: {err}")

if __name__ == "__main__":
    midi_listener()
