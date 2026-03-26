import os, json, evdev
from flask import Flask, request, render_template_string
from evdev import UInput, ecodes as e

app = Flask(__name__)

# [内核执行逻辑] 模拟物理按键，支持 Pro Tools, Kdenlive 等万级指令
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

# 指令映射库
ACTIONS = {
    "复制": [e.KEY_LEFTCTRL, e.KEY_C],
    "粘贴": [e.KEY_LEFTCTRL, e.KEY_V],
    "撤销": [e.KEY_LEFTCTRL, e.KEY_Z],
    "播放": [e.KEY_SPACE],
    "停止": [e.KEY_SPACE],
    "保存": [e.KEY_LEFTCTRL, e.KEY_S],
    "全选": [e.KEY_LEFTCTRL, e.KEY_A]
}

HTML = """
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shensist WeChat Controller</title></head>
<body style="text-align:center; padding-top:40px; font-family:sans-serif; background:#f4f4f4;">
    <h2 style="color:#333;">Shensist 系统控制中心</h2>
    <div style="margin-bottom:20px;">
        <input type="text" id="cmd" placeholder="使用微信语音转文字..." 
               style="width:85%; height:55px; font-size:18px; border-radius:12px; border:1px solid #ddd; padding:0 10px;">
    </div>
    <button onclick="send()" 
            style="width:90%; height:55px; background:#07c160; color:white; border:none; border-radius:12px; font-size:20px; font-weight:bold;">
        发送指令到电脑
    </button>
    <p id="status" style="margin-top:20px; color:#666; font-size:14px;"></p>
    <script>
        function send() {
            let val = document.getElementById('cmd').value;
            if(!val) return;
            document.getElementById('status').innerText = '正在发送: ' + val;
            fetch('/exec?msg=' + encodeURIComponent(val))
                .then(r => r.text())
                .then(t => { document.getElementById('status').innerText = '反馈: ' + t; });
            document.getElementById('cmd').value = '';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/exec')
def execute():
    msg = request.args.get('msg', '')
    print(f"🎙️ 收到微信指令: {msg}")
    for k, v in ACTIONS.items():
        if k in msg:
            if send_key_combo(v): return f"成功: {k}"
            else: return "内核权限错误"
    return "未匹配指令"

if __name__ == '__main__':
    # 强制开启 5000 端口服务
    app.run(host='0.0.0.0', port=5000)
