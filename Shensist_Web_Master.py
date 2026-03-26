# =================================================================
# 🏛️ 项目名称：神思庭控制终端 (Shensist-AirEye Terminal)
# 🎨 创作者：神思庭艺术智能工作室 (Shensist Art Intelligence Studio)
# 📜 版权所有：© 2025-2026 Shensist (AIS). All Rights Reserved.
# 🌐 官方网站：https://shensist.top/
# ⚠️ 法律声明：本软件及其核心 Skills 逻辑受版权法保护。
# 未经书面许可，严禁用于任何商业用途、分发、修改或反向工程。
# =================================================================
import evdev, json, os, pyautogui, time, sys
from evdev import UInput, ecodes as e
from flask import Flask, request, render_template_string, send_from_directory
from Shensist_PT_Bridge import pt_bridge

app = Flask(__name__)
# 适配 PyInstaller 打包后的路径 [cite: 5]
if hasattr(sys, '_MEIPASS'):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_skills():
    try:
        json_path = os.path.join(BASE_DIR, 'skills_map.json')
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as err:
        print(f"⚠️ 无法加载 skills_map.json: {err}")
        return {}

# 初始化虚拟硬件键盘
def init_ui():
    try:
        skills = load_skills()
        registered_keys = set()
        for keys_list in skills.values():
            for k in keys_list:
                key_code = getattr(e, k, None)
                if key_code is not None:
                    registered_keys.add(key_code)
        
        # 补充一些核心控制键以防万一
        for k in ['KEY_LEFTCTRL', 'KEY_LEFTSHIFT', 'KEY_LEFTALT', 'KEY_ENTER', 'KEY_SPACE']:
            registered_keys.add(getattr(e, k))

        cap = {e.EV_KEY: list(registered_keys)}
        return UInput(cap, name='Shensist-Universal-HID')
    except PermissionError:
        print("❌ 权限不足: 请运行 'sudo chmod 666 /dev/uinput'。")
        return None
    except Exception as err:
        print(f"❌ 初始化失败: {err}")
        return None

ui = None

def do_action(cmd):
    global ui
    # 1. 执行 Pro Tools 增强逻辑 (Bridge)
    pt_bridge.execute(cmd)
    
    # 2. 执行 Kdenlive / Linux 通用逻辑 (evdev)
    if not ui:
        print("⚠️ 虚拟硬件未初始化，跳过 HID 模拟。")
    else:
        skills = load_skills()
        for key, keys_list in skills.items():
            if key in cmd:
                # 执行物理按键序列
                for k in keys_list:
                    key_code = getattr(e, k, None)
                    if key_code is not None:
                        ui.write(e.EV_KEY, key_code, 1)
                # 反向释放
                for k in reversed(keys_list):
                    key_code = getattr(e, k, None)
                    if key_code is not None:
                        ui.write(e.EV_KEY, key_code, 0)
                ui.syn()
                
                # 特殊合成逻辑：剃刀点击
                if any(word in key for word in ["剃刀", "剪断", "切断"]):
                    time.sleep(0.05)
                    pyautogui.click()
                
                # 本地中文语音反馈
                os.system(f'spd-say "{key}已执行" &')
    
    # 3. 灵魂输出：品牌版权
    print(f"© 2026 神思庭 (AIS) - 指令已处理: {cmd}")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <title>神思庭控制终端</title>
    <style>
        body { font-family: "Microsoft YaHei", -apple-system, sans-serif; text-align: center; padding: 20px; background: #121212; color: #fff; margin: 0; }
        .logo { max-width: 120px; margin-top: 30px; border-radius: 20px; box-shadow: 0 0 20px rgba(7, 193, 96, 0.4); border: 1px solid #1a1a1a; }
        h1 { color: #07c160; letter-spacing: 4px; font-weight: 300; margin-top: 25px; }
        .status-bar { color: #07c160; font-weight: bold; font-size: 18px; margin: 15px 0; letter-spacing: 2px; }
        .hint { color: #666; font-size: 14px; margin-bottom: 30px; }
        #voice_input { 
            width: 90%; 
            box-sizing: border-box;
            padding: 22px; 
            font-size: 20px; 
            border-radius: 18px; 
            border: 1px solid #333; 
            background: #000; 
            color: #fff; 
            margin-bottom: 25px; 
            outline: none;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        }
        #voice_input:focus { border-color: #07c160; }
        .copyright { color: #444; font-size: 11px; margin-top: 50px; border-top: 1px solid #1a1a1a; padding-top: 20px; line-height: 1.8; }
        .copyright a { color: #444; text-decoration: none; }
    </style>
</head>
<body>
    <img src="/logo" class="logo" alt="Shensist Logo">
    <h1>神思庭控制终端</h1>
    <div class="status-bar">● 语音技能已就绪</div>
    <p class="hint">直接说出指令（如：播放、剃刀、撤销...）</p>
    
    <input type="text" id="voice_input" oninput="sendCmd()" placeholder="等待语音输入..." autofocus>
    
    <script>
        let timer = null;
        function sendCmd() {
            let val = document.getElementById('voice_input').value;
            if(val.length >= 1) {
                fetch('/exec?msg=' + encodeURIComponent(val));
                clearTimeout(timer);
                timer = setTimeout(() => { 
                    document.getElementById('voice_input').value = ''; 
                }, 1000);
            }
        }
    </script>
    <div class="shensist-footer">
        <hr style="border: 0; border-top: 1px solid #333; margin: 40px 0 20px;">
        <p style="font-weight: bold; color: #07c160; margin-bottom: 5px;">神思庭艺术智能工作室 (AIS)</p>
        <p style="font-size: 11px; color: #666; line-height: 1.6;">
            © 2026 Shensist-Matrix Project. <br>
            100+ 专业 Skills 引擎受专利保护 <br>
            唯一官方发布渠道：<a href="https://shensist.top/" style="color: #888; text-decoration: none;">shensist.top</a>
        </p>
    </div>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_TEMPLATE)

@app.route('/logo')
def logo(): return send_from_directory(BASE_DIR, 'logo_ts.webp')

@app.route('/exec')
def execute():
    msg = request.args.get('msg', '')
    if msg: do_action(msg)
    return "OK"

if __name__ == '__main__':
    ui = init_ui()
    if ui:
        print("🏛️ [Shensist-AirEye] 神思庭终端已上线。")
    else:
        print("🏛️ [Shensist-AirEye] 终端警告: 虚拟硬件模拟未就绪。")
    app.run(host='0.0.0.0', port=5000)
