import os, time, evdev
from evdev import UInput, ecodes as e

# 内核按键模拟
def send_key_combo(keys):
    try:
        with UInput() as ui:
            for key in keys: ui.write(e.EV_KEY, key, 1)
            for key in reversed(keys): ui.write(e.EV_KEY, key, 0)
            ui.syn()
        return True
    except Exception as err:
        print(f"❌ 模拟失败: {err}")
        return False

ACTIONS = {
    "复制": [e.KEY_LEFTCTRL, e.KEY_C],
    "粘贴": [e.KEY_LEFTCTRL, e.KEY_V],
    "撤销": [e.KEY_LEFTCTRL, e.KEY_Z],
    "播放": [e.KEY_SPACE],
    "停止": [e.KEY_SPACE],
    "保存": [e.KEY_LEFTCTRL, e.KEY_S]
}

CMD_FILE = "/home/mmm/桌面/Shensist_Matrix/Shensist_AirEye/cmd.txt"

print("🏛️ [Shensist-File-Agent] 文件指令监听已启动。")
print(f"📄 请在 {CMD_FILE} 中输入指令并保存。")

# 确保文件存在
if not os.path.exists(CMD_FILE):
    with open(CMD_FILE, 'w') as f: f.write("")

while True:
    try:
        # 如果文件不存在则说明被删除，重新创建
        if not os.path.exists(CMD_FILE):
             with open(CMD_FILE, 'w') as f: f.write("")
        
        with open(CMD_FILE, 'r+') as f:
            content = f.read().strip()
            if content:
                print(f"📥 收到文件指令: {content}")
                executed = False
                for k, v in ACTIONS.items():
                    if k in content:
                        if send_key_combo(v):
                            print(f"⚡ [执行成功] 物理按键: {k}")
                            executed = True
                        break
                if not executed:
                    print(f"❓ 未匹配指令: {content}")
                
                # 执行完清空文件，等待下次指令
                f.seek(0)
                f.truncate()
        time.sleep(0.5) # 每0.5秒扫描一次
    except KeyboardInterrupt:
        break
    except Exception as err:
        print(f"❌ 运行异常: {err}")
        time.sleep(1)
