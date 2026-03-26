# =================================================================
# 🏛️ 项目名称：神思庭控制终端 (Shensist-AirEye Terminal)
# 🎨 创作者：神思庭艺术智能工作室 (Shensist Art Intelligence Studio)
# 📜 版权所有：© 2025-2026 Shensist (AIS). All Rights Reserved.
# 🌐 官方网站：https://shensist.top/
# ⚠️ 法律声明：本软件及其核心 Skills 逻辑受版权法保护。
# =================================================================
import os
import sys
import threading
import subprocess

# 🏛️ 神思庭 (AIS) 核心组件导入
# 启动时自动校检依赖环境
try:
    import mido
except ImportError:
    print("📦 [Shensist-AIS] 正在补全 MIDI 驱动组件...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "mido", "python-rtmidi"])
        import mido
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")
        mido = None

def run_midi_engine():
    """后台 MIDI 监听线程：将物理按键转化为语义指令"""
    if not mido:
        print("⚠️ MIDI 核心库未载入，硬件监听已禁用。")
        return

    print("🎹 [神思庭-AIS] 硬件 MIDI 引擎初始化中...")
    # 映射字典与 skills_map.json 保持逻辑对齐
    MIDI_MAP = {60: "播放", 62: "剃刀", 64: "撤销"} 
    
    try:
        # 自动寻找第一个可用的 MIDI 输入端口
        input_names = mido.get_input_names()
        if not input_names:
            print("⚠️ 未发现物理 MIDI 设备，硬件监听挂起。")
            return

        print(f"✅ 已成功挂载 MIDI 硬件: {input_names[0]}")
        with mido.open_input(input_names[0]) as inport:
            from Shensist_Web_Master import do_action
            for msg in inport:
                # velocity > 0 表示按下动作
                if msg.type == 'note_on' and msg.velocity > 0:
                    if msg.note in MIDI_MAP:
                        skill = MIDI_MAP[msg.note]
                        # 内部闭环调用，绕过网络延迟
                        do_action(skill)
                        print(f"⚡ [硬件触发] MIDI {msg.note} -> 执行: {skill}")
    except Exception as e:
        print(f"❌ MIDI 引擎异常: {e}")

def run_web_master():
    """主线程 Web 服务：处理远程 iPhone 13 指令"""
    print("🏛️ [神思庭-AIS] 正在挂载 Web 控制中枢...")
    if sys.platform == "linux":
        # 自动提权处理内核 HID 权限
        os.system('sudo chmod 666 /dev/uinput')
    
    # 动态导入 Web Master 核心
    from Shensist_Web_Master import app
    app.run(host='0.0.0.0', port=5000, use_reloader=False)

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🏛️  SHENSIST-AIREYE TERMINAL v2.5 OFFICIAL")
    print("🎨 神思庭艺术智能工作室 (AIS) | shensist.top")
    print("="*50 + "\n")

    # 1. 启动并联 MIDI 监听线程
    midi_thread = threading.Thread(target=run_midi_engine, daemon=True)
    midi_thread.start()

    # 2. 启动主 Web 服务 (阻塞)
    run_web_master()
